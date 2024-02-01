import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_default_license(assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}"
    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 6,
        ""
    )


@pytest.mark.asyncio
async def test_default_license(assemble_func_mock, random_file):
    license_text = "some text"
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        f"--license={license_text}"

    ]
    await async_main()
    assemble_func_mock.assert_called_once_with(
        random_file,
        *[pytest.any] * 6,
        license_text
    )
