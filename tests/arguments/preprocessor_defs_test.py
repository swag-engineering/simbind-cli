import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_preprocessor_defs_empty(assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 9,
        []
    )


@pytest.mark.asyncio
async def test_preprocessor_defs_single(assemble_func_mock, random_file, random_string):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--preprocessor-def={random_string}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 9,
        [random_string]
    )



@pytest.mark.asyncio
async def test_preprocessor_defs_multiple(assemble_func_mock, random_file, random_string):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--preprocessor-def={random_string}",
        f"--preprocessor-def={random_string}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 9,
        [random_string, random_string]
    )
