import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def url_to_filename(url: str, type=".html"):
    new_url = url.replace("https://", "").replace("http://", "")
    result = ""
    for char in new_url:
        if not char.isdigit() and not char.isalpha():
            result += "-"
        else:
            result += char

    return result + type


def get_images(request_text, path, new_dir_name, hostname):
    soup = BeautifulSoup(request_text, "html.parser")
    object = soup.find_all(["img", "link", "script"])

    for object in object:
        match object.attrs:
            case {'href': _}:
                obj_download_tag = 'href'
            case {'src': _}:
                obj_download_tag = 'src'
            case _:
                continue
        obj_link = object.attrs[obj_download_tag]
        if urlparse(obj_link).netloc != hostname:
            continue
        image = requests.get(obj_link).content

        splited_link = os.path.splitext(obj_link)
        if splited_link[-1] == '':
            img_url, type = splited_link
            type = '.html'
        else:
            img_url, type = os.path.splitext(obj_link)

        filename = url_to_filename(img_url, type)
        new_file_path = os.path.join(path, filename)

        with open(new_file_path, "wb") as file:
            file.write(image)

        relative_path = os.path.join(new_dir_name, filename)
        object.attrs[obj_download_tag] = relative_path
    return soup


def download(url: str, path: str = os.getcwd()) -> str:
    new_html_file_name = url_to_filename(url)
    new_html_path = os.path.join(path, new_html_file_name)

    request = requests.get(url)
    with open(new_html_path, "w") as html_file:
        html_file.write(request.text)

    new_dir_path = f"{new_html_path[:-5]}_files"
    new_dir_name = os.path.split(new_dir_path)[1]
    os.mkdir(new_dir_path)

    with open(new_html_path, "r+", encoding="utf-8") as file:
        hostname = urlparse(url).hostname
        soup = get_images(file.read(), new_dir_path, new_dir_name, hostname)
        file.seek(0)
        file.write(str(soup.prettify()))

    return new_html_path


if __name__ == "__main__":
    download("https://ru.hexlet.io/courses")
