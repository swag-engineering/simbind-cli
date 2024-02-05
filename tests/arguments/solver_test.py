import os
import sys

import pytest

from simbind.__main__ import async_main


@pytest.mark.asyncio
async def test_invalid_solver(capfd, assemble_func_mock, random_file):
    sys.argv = [
        "prog",
        f"--slx-path={random_file}",
        "--solver=random_string"
    ]
    with pytest.raises(SystemExit) as exc_info:
        await async_main()
        assert exc_info.value.code != 0

    _, err = capfd.readouterr()
    assert "--solver" in err


@pytest.mark.asyncio
async def test_exporter_dir_without_overwrite(mocker, random_file):
    possible_solvers = ['ode1', 'ode2', 'ode3', 'ode4', 'ode5', 'ode8', 'ode14x', 'ode1be']
    for solver in possible_solvers:
        assemble_mock = mocker.patch('simbind.__main__.assemble')
        sys.argv = [
            "prog",
            f"--slx-path={random_file}",
            f"--solver={solver}"
        ]
        await async_main()
        assemble_mock.assert_called_once_with(
            random_file,
            *[pytest.any] * 4,
            solver,
            *[pytest.any] * 2
        )
