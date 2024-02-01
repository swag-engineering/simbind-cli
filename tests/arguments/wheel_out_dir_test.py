import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_wheel_dir_transmission(assemble_func_mock, random_file, random_empty_dir):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--wheel-out-dir={random_empty_dir}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 3,
        random_empty_dir,
        *[pytest.any] * 3
    )
