import os  # noqa
import logging
import pytest
from page_loader import download

logging.getLogger('PIL').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def dir_for_tests(tmp_path):
    directory = tmp_path / "dir"
    directory.mkdir()
    return f"{tmp_path}/dir"


def test_page_loader_check_return_string(dir_for_tests, requests_mock):
    tmp_path = dir_for_tests

    requests_mock.get("https://ru.hexlet.io/courses", text="data")
    file_path = download("https://ru.hexlet.io/courses", tmp_path)

    assert file_path == f"{tmp_path}/ru-hexlet-io-courses.html"


def test_page_loader_check_requests_count(dir_for_tests, requests_mock):
    tmp_path = dir_for_tests

    requests_mock.get("https://some_page.com", text="data")
    download("https://some_page.com", tmp_path)

    assert requests_mock.call_count == 1


def test_page_loader_download_files(dir_for_tests, requests_mock, main, css, png, js, all_fixtures, html_after):  # noqa E501
    tmp_path = dir_for_tests

    with open(main) as main, open(png, "br",) as image, open(
        css  # noqa E501
    ) as css, open(
        js
    ) as js:

        requests_mock.get("https://ru.hexlet.io/courses", text=main.read())
        requests_mock.get(
            "https://ru.hexlet.io/assets/application.css", text=css.read()
        )
        requests_mock.get(
            "https://ru.hexlet.io/assets/professions/python.png",
            content=image.read(),
        )
        requests_mock.get(
            "https://ru.hexlet.io/packs/js/runtime.js", text=js.read()
        )

        download("https://ru.hexlet.io/courses", tmp_path)
        directory = os.path.join(tmp_path, "ru-hexlet-io-courses_files")
        for f in os.listdir(directory):
            file_path = os.path.join(directory, f)
            fixture_path = os.path.join(
                all_fixtures, f
            )

            with open(file_path, "rb") as file, open(
                fixture_path, "rb"
            ) as fixture:
                if f == "ru-hexlet-io-assets-professions-python.png":
                    continue
                assert file.read() == fixture.read()

        main_path = os.path.join(tmp_path, "ru-hexlet-io-courses.html")
    with open(main_path) as main, open(
        html_after, "r"
            ) as fixture:
        assert main.read() == fixture.read()
