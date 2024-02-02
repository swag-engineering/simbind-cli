import os
import random
import string
import sys
import tempfile

import pytest


def pytest_configure():
    class Any:
        def __eq__(self, other):
            return True

    pytest.any = Any()


@pytest.fixture(scope="function")
def assemble_func_mock(mocker):
    return mocker.patch('simbind.__main__.assemble')


@pytest.fixture(scope="function")
def random_file() -> str:
    with tempfile.NamedTemporaryFile() as temp_file:
        yield temp_file.name


@pytest.fixture(scope="function")
def random_empty_dir() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(scope="function")
def random_dir_with_files() -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        for _ in range(5):
            file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            file_path = os.path.join(temp_dir, file_name)
            open(file_path, 'w').close()
        yield temp_dir


@pytest.fixture(scope="function", autouse=True)
def secure_argv():
    original_argv = sys.argv
    yield
    sys.argv = original_argv
