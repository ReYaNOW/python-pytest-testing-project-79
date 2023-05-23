import os
import pytest
pytest_plugins = [
    "tests.fixtures.test_files",
]


def file_fixtures(file):
    if 'code' in os.listdir(os.getcwd()):
        file_path = os.path.join('code', 'tests/fixtures', file)
    else:
        file_path = os.path.join('tests/fixtures', file)
    return file_path


@pytest.fixture
def main():
    return "tests/fixtures/some-complex-page-com.html"  # noqa E501


@pytest.fixture
def css():
    return "tests/fixtures/fixtures_for_complex/ru-hexlet-io-assets-application.css"  # noqa E501


@pytest.fixture
def png():
    return "tests/fixtures/fixtures_for_complex/ru-hexlet-io-assets-professions-python.png"  # noqa E501


@pytest.fixture
def html_after():
    return "tests/fixtures/some-complex-page-com-after.html"  # noqa E501


@pytest.fixture
def js():
    return "tests/fixtures/fixtures_for_complex/ru-hexlet-io-packs-js-runtime.js"  # noqa E501
