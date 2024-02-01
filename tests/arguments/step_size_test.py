import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_invalid_step_size(capfd, random_file):
    invalid_step_sizes = ["", "string"]
    for step_size in invalid_step_sizes:
        sys.argv = [
            "prog",
            f"--slx-path={random_file}",
            f"--step={step_size}"
        ]
        with pytest.raises(SystemExit) as exc_info:
            await async_main()
            assert exc_info.value.code != 0

        _, err = capfd.readouterr()
        assert "--step" in err


@pytest.mark.asyncio
async def test_valid_step_size(mocker, random_file):
    valid_step_sizes = [1, 0.01, 1e10]
    for step_size in valid_step_sizes:
        sys.argv = [
            "prog",
            f"--slx-path={random_file}",
            f"--step={step_size}"
        ]
        assemble_mock = mocker.patch('simbind.__main__.assemble')
        await async_main()
        assemble_mock.assert_called_once_with(
            random_file,
            *[pytest.any] * 5,
            step_size,
            pytest.any
        )
