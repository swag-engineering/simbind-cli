import asyncio
import os
import argparse
import logging
import re
import shutil
import sys

from .architect import Collector, MockDriver, SiLDriver, test_model_integrity
from .matlab_exporter import export_model, FixedStepSolver


def dir_has_files(path: str) -> bool:
    if not os.path.isdir(path):
        raise RuntimeError(f"'{path}' is not a directory")
    return len(os.listdir(path)) != 0


def delete_dir_internals(path: str):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                pass
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


async def main(
        slx_path: str,
        package_name: str,
        exporter_out_dir: str,
        models_out_dir: str,
        wheel_out_dir: str,
        solver: str,
        time_step: float
):
    await asyncio.to_thread(
        export_model,
        slx_path,
        exporter_out_dir,
        time_step,
        FixedStepSolver(solver)
    )
    collector = await Collector.create(exporter_out_dir, package_name, time_step)

    mock_dir = os.path.join(models_out_dir, "mock")
    os.mkdir(mock_dir)
    mock_pkg_name, mock_cls_name = await MockDriver.compose(collector, mock_dir, "")

    sil_dir = os.path.join(models_out_dir, "sil")
    os.mkdir(sil_dir)
    sil_pkg_name, sil_cls_name = await SiLDriver.compose(collector, sil_dir, "")

    await test_model_integrity(
        mock_dir,
        mock_pkg_name,
        mock_cls_name,
        collector,
    )

    await test_model_integrity(
        sil_dir,
        sil_pkg_name,
        sil_cls_name,
        collector
    )

    await test_model_integrity(
        sil_dir,
        sil_pkg_name,
        sil_cls_name,
        collector,
        True
    )

    pip_proc = await asyncio.create_subprocess_shell(
        f"{sys.executable} -m pip wheel --no-deps {sil_dir} -w {wheel_out_dir}",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await pip_proc.communicate()
    if pip_proc.returncode:
        logging.error(stderr)
        raise RuntimeError("stderr")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--slx-path',
        dest='slx_path',
        help='path to simulink model',
        required=True,
        type=os.path.abspath
    )
    parser.add_argument(
        '--pkg-name',
        dest='pkg_name',
        help='Name of the output Python package',
        type=str,
        default='model'
    )
    parser.add_argument(
        '--exporter-out-dir',
        dest='exporter_out_dir',
        help='path to output folder',
        required=True,
        type=os.path.abspath
    )
    # parser.add_argument(
    #     '--architect-out-dir',
    #     dest='architect_out_path',
    #     help='path to output folder',
    #     required=True
    # )
    parser.add_argument(
        '--models-out-dir',
        dest='models_out_dir',
        help='path to output folder',
        required=True,
        type=os.path.abspath
    )
    parser.add_argument(
        '--wheel-out-dir',
        dest='wheel_out_dir',
        help='path to output folder',
        required=True,
        type=os.path.abspath
    )
    parser.add_argument(
        '--overwrite',
        dest='overwrite',
        help='flag to overwrite output folder if it is not empty',
        action='store_true'
    )
    # parser.add_argument(
    #     '--no_tests',
    #     dest='no_tests',
    #     help='disables integrity tests of resulting packages',
    #     action='store_true'
    # )
    # parser.add_argument(
    #     '--tmp_dir',
    #     dest='tmp_dir',
    #     help='Output to temporary folder. Should be used for debug only'
    # )
    parser.add_argument(
        '--solver',
        dest='solver',
        choices=['ode1', 'ode2', 'ode3', 'ode4', 'ode5'],
        help='matlab fixed step solver',
        type=str,
        default='ode5'
    )
    parser.add_argument(
        '--step',
        dest='step_size',
        help='step_size',
        type=float,
        default=0.0004
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-v',
        dest='verbosity',
        default=1,
        help='Specifies the level of verbosity. Example: -vvv',
        action='count'
    )
    group.add_argument(
        '--quiet',
        '-q',
        dest='no_logs',
        help='Do not print logs to stdout',
        action='store_true'
    )

    args = parser.parse_args()

    verbosity2lvl = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    args.verbosity = 3 if args.verbosity > 3 else args.verbosity
    logger = logging.getLogger()
    logger.setLevel(level=verbosity2lvl[args.verbosity])
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(levelname)-8s :: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if not os.path.isfile(args.slx_path):
        raise RuntimeError(f"File {args.slx_path} does not exist.")

    if not re.match(r"^[a-z][a-z0-9_]+$", args.pkg_name):
        raise RuntimeError(f"File {args.slx_path} does not exist.")

    for dir_path in [args.exporter_out_dir, args.models_out_dir, args.wheel_out_dir]:
        if dir_has_files(dir_path):
            if not args.overwrite:
                raise RuntimeError(f"Directory {dir_path} not empty. Consider using --overwrite.")
            delete_dir_internals(dir_path)

    asyncio.run(
        main(
            args.slx_path,
            args.pkg_name,
            args.exporter_out_dir,
            args.models_out_dir,
            args.wheel_out_dir,
            args.solver,
            args.step_size
        )
    )
