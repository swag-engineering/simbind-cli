import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_invalid_package_names(assemble_func_mock, random_file):
    package_names = [
        "a" * 4,
        "a" * 51,
        "Aabcd",
        "_abcd",
        "abcd$",
        "abc@def",
        "1bcde",
        "ab cd"
    ]
    for name in package_names:
        sys.argv = [
            "prog",
            f"--slx-path={random_file}",
            f"--pkg-name={name}"
        ]
        with pytest.raises(ValueError) as _:
            await async_main()


@pytest.mark.asyncio
async def test_valid_package_names(mocker, random_file):
    package_names = [
        "a" * 5,
        "a" * 50,
        "a1bc_"
    ]
    for name in package_names:
        sys.argv = [
            "prog",
            f"--slx-path={random_file}",
            f"--pkg-name={name}"
        ]
        mock_assemble = mocker.patch('simbind.__main__.assemble')
        await async_main()
        mock_assemble.assert_called_once_with(
            random_file,
            name,
            *[pytest.any] * 6
        )
