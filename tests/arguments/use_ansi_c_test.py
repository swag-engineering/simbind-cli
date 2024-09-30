import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_use_ansi_c_omitted(assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 8,
        False,
        pytest.any
    )


@pytest.mark.asyncio
async def test_use_ansi_c_included(assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        "--use-ansi-c"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 8,
        True,
        pytest.any
    )
