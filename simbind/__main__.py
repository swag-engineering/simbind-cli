import os
import re
import sys
import shutil
import logging
import asyncio
import argparse
import tempfile

from simbind.architect.simbind_architect import Collector, MockDriver, SiLDriver, test_model_integrity
from simbind.exporter.simulink_exporter import export_model, FixedStepSolver


def dir_has_files(path: str) -> bool:
    if not os.path.isdir(path):
        raise RuntimeError(f"'{path}' is not a directory")
    return len(os.listdir(path)) != 0


def delete_dir_internals(path: str):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def prepare_dir(path: str, overwrite: bool):
    if dir_has_files(path):
        if not overwrite:
            raise ValueError(f"Directory {path} not empty. Consider using --overwrite.")
        delete_dir_internals(path)


async def assemble(
        slx_path: str,
        package_name: str,
        exporter_out_dir: str,
        models_out_dir: str,
        wheel_out_dir: str,
        solver: str,
        time_step: float,
        license_text: str
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
    mock_pkg_name, mock_cls_name = await MockDriver.compose(collector, mock_dir, license_text)

    sil_dir = os.path.join(models_out_dir, "sil")
    os.mkdir(sil_dir)
    sil_pkg_name, sil_cls_name = await SiLDriver.compose(collector, sil_dir, license_text)

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
        raise RuntimeError(stderr)


async def async_main():
    parser = argparse.ArgumentParser(
        prog='simbind',
        description='Tool to generate Python wheel package from Simulink model.',
    )
    parser.add_argument(
        '--slx-path',
        dest='slx_path',
        help='Path to Simulink .slx file.',
        required=True,
        type=os.path.abspath
    )
    parser.add_argument(
        '--pkg-name',
        dest='pkg_name',
        help='Name of the output Python package. (default: \'%(default)s\')',
        type=str,
        default='model'
    )
    parser.add_argument(
        '--wheel-out-dir',
        dest='wheel_out_dir',
        help='Path to folder where wheel package will be stored. (default: \'%(default)s\')',
        default='.',
        type=os.path.abspath
    )
    parser.add_argument(
        '--solver',
        dest='solver',
        choices=['ode1', 'ode2', 'ode3', 'ode4', 'ode5', 'ode8', 'ode14x', 'ode1be'],
        help='Fixed-step solver. (default: \'%(default)s\')',
        type=str,
        default='ode5'
    )
    parser.add_argument(
        '--step',
        dest='step_size',
        help='Fixed step size in seconds. (default: \'%(default)s\')',
        type=float,
        default=0.001
    )
    parser.add_argument(
        '--license-text',
        dest='license_text',
        help='License text that will be included in output Python wheel package. (default: \'%(default)s\')',
        type=str,
        default=""
    )
    parser.add_argument(
        '-v',
        dest='verbosity',
        default=0,
        help='Specifies the level of verbosity. Example: -vvv',
        action='count'
    )
    # [DEBUG] Path to directory that will be used to store .c and .h files exported by Simulink
    parser.add_argument(
        '--exporter-out-dir',
        dest='exporter_out_dir',
        help=argparse.SUPPRESS,
        type=os.path.abspath
    )
    # [DEBUG] Directory where output Python model will be stored
    parser.add_argument(
        '--models-out-dir',
        dest='models_out_dir',
        help=argparse.SUPPRESS,
        type=os.path.abspath
    )
    # [DEBUG] Flag to delete models-out-dir and exporter-out-dir folders' content if they are not empty
    parser.add_argument(
        '--overwrite',
        dest='overwrite',
        help=argparse.SUPPRESS,
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

    exporter_out_tmp_dir: tempfile.TemporaryDirectory | None = None
    models_out_tmp_dir: tempfile.TemporaryDirectory | None = None

    if not os.path.isfile(args.slx_path):
        raise FileNotFoundError(f"File '{args.slx_path}' does not exist.")

    if not os.path.isdir(args.wheel_out_dir):
        raise FileNotFoundError(f"Directory '{args.wheel_out_dir}' does not exist.")

    if not re.match(r"^[a-z][a-z0-9_]{4,29}$", args.pkg_name):
        raise ValueError(
            f"Invalid package name '{args.pkg_name}'."
            "Only lowercase letters, numbers and underscores are acceptable. Should start with lowercase letter and "
            "have length between 5 and 50 characters."
        )

    try:
        if args.exporter_out_dir:
            prepare_dir(args.exporter_out_dir, args.overwrite)
        else:
            exporter_out_tmp_dir = tempfile.TemporaryDirectory()

        if args.models_out_dir:
            prepare_dir(args.models_out_dir, args.overwrite)
        else:
            models_out_tmp_dir = tempfile.TemporaryDirectory()

        await assemble(
            args.slx_path,
            args.pkg_name,
            args.exporter_out_dir or exporter_out_tmp_dir.name,
            args.models_out_dir or models_out_tmp_dir.name,
            args.wheel_out_dir,
            args.solver,
            args.step_size,
            args.license_text
        )
    finally:
        if exporter_out_tmp_dir:
            exporter_out_tmp_dir.cleanup()
        if models_out_tmp_dir:
            models_out_tmp_dir.cleanup()


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
