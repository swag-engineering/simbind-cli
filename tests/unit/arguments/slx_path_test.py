import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_mandatory_slx_path(capfd):
    sys.argv = [
        "prog"
    ]
    with pytest.raises(SystemExit) as exc_info:
        await async_main()
        assert exc_info.value.code != 0

    _, err = capfd.readouterr()
    assert err.endswith("the following arguments are required: --slx-path\n")


@pytest.mark.asyncio
async def test_slx_path_doesnt_exist(mocker):
    mocker.patch('simbind.__main__.assemble')
    sys.argv = [
        "prog",
        "--slx-path=/doesnt/exist"
    ]
    with pytest.raises(FileNotFoundError) as _:
        await async_main()


@pytest.mark.asyncio
async def test_slx_path_transmission(mocker, random_file):
    mock_assemble = mocker.patch('simbind.__main__.assemble')
    sys.argv = [
        "prog",
        f"--slx-path={random_file}"
    ]
    await async_main()
    mock_assemble.assert_called_once_with(
        random_file,
        *[pytest.any] * 7
    )
