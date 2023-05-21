import pytest

pytest_plugins = [
    "tests.fixtures.test_files",
]


@pytest.fixture
def all_fixtures():
    return "tests/fixtures/fixtures_for_complex"  # noqa E501


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
