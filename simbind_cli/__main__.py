import asyncio
import os
import argparse
import logging
import shutil

from .architect import Collector, MockDriver, SiLDriver, test_model_integrity
from .matlab_exporter import export_model


def dir_has_files(path: str) -> bool:
    if not os.path.isdir(path):
        raise RuntimeError(f"'{path}' is not a directory")
    return not os.listdir(path)


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


async def main(slx_path: str, exporter_out_path: str, models_out_path: str, time_step: float):
    await asyncio.to_thread(
        export_model,
        slx_path,
        exporter_out_path,
        time_step
    )
    collector = await Collector.create(exporter_out_path, time_step)

    mock_dir = os.path.join(models_out_path, "mock")
    os.mkdir(mock_dir)
    mock_pkg_name, mock_mdl_name, mock_cls_name = await MockDriver.compose(collector, mock_dir)

    sil_dir = os.path.join(models_out_path, "sil")
    os.mkdir(sil_dir)
    sil_pkg_name, sil_mdl_name, sil_cls_name = await SiLDriver.compose(collector, sil_dir)

    await test_model_integrity(
        mock_dir,
        mock_pkg_name,
        mock_mdl_name,
        mock_cls_name,
        collector,
    )

    await test_model_integrity(
        sil_dir,
        sil_pkg_name,
        sil_mdl_name,
        sil_cls_name,
        collector
    )

    await test_model_integrity(
        sil_dir,
        sil_pkg_name,
        sil_mdl_name,
        sil_cls_name,
        collector,
        True
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--slx-path',
        dest='slx_path',
        help='path to simulink model',
        required=True
    )
    parser.add_argument(
        '--exporter-out-path',
        dest='exporter_out_path',
        help='path to output folder',
        required=True
    )
    parser.add_argument(
        '--architect-out-path',
        dest='architect_out_path',
        help='path to output folder',
        required=True
    )
    parser.add_argument(
        '--models-out-path',
        dest='models_out_path',
        help='path to output folder',
        required=True
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
    parser.add_argument(
        '--tmp_dir',
        dest='tmp_dir',
        help='Output to temporary folder. Should be used for debug only'
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

    for dir_path in [args.exporter_out_path, args.architect_out_path, args.models_out_path]:
        if dir_has_files(dir_path):
            if not args.overwrite:
                raise RuntimeError(f"Directory {dir_path} not empty. Consider using --overwrite.")
            delete_dir_internals(dir_path)

    asyncio.run(main(args.slx_path, args.exporter_out_path, args.models_out_path, 0.004))
