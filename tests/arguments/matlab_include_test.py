import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_matlab_include_empty(assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 7,
        [],
        *[pytest.any] * 2
    )


@pytest.mark.asyncio
async def test_matlab_include_single(assemble_func_mock, random_file, random_empty_dir):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--matlab-include={random_empty_dir}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 7,
        [random_empty_dir],
        *[pytest.any] * 2
    )



@pytest.mark.asyncio
async def test_matlab_include_multiple(assemble_func_mock, random_file, random_empty_dir):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--matlab-include={random_empty_dir}",
        f"--matlab-include={random_empty_dir}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 7,
        [random_empty_dir, random_empty_dir],
        *[pytest.any] * 2
    )
