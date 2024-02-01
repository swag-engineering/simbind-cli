import os
import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_models_dir_transmission(assemble_func_mock, random_file, random_empty_dir):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--models-out-dir={random_empty_dir}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        pytest.any,
        pytest.any,
        random_empty_dir,
        *[pytest.any] * 4
    )


@pytest.mark.asyncio
async def test_models_dir_without_overwrite(capfd, assemble_func_mock, random_file, random_dir_with_files):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--models-out-dir={random_dir_with_files}"
    ]
    with pytest.raises(ValueError) as exc_info:
        await async_main()
        assert "--overwrite" in str(exc_info.value)


@pytest.mark.asyncio
async def test_models_dir_cleanup(assemble_func_mock, random_file, random_dir_with_files):
    num_files = len(os.listdir(random_dir_with_files))
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--models-out-dir={random_dir_with_files}",
        "--overwrite"
    ]
    await async_main()
    num_files_after_cleanup = len(os.listdir(random_dir_with_files))
    assert num_files_after_cleanup == 0 and num_files_after_cleanup != num_files
