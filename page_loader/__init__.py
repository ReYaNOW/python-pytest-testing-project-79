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


def url_validator(link, hostname):
    if link[:4] != 'http' and link[:4] != 'www.':
        if link[0] != '/':
            link = f'/{link}'
        link = f'{hostname}{link}'

    if link[:4] != 'http':
        link = f'http://{link}'
    return link


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) \
            Gecko/20100101 Firefox/112.0"}


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
        obj_link = object.get(obj_download_tag)
        obj_link = url_validator(obj_link, hostname)
        if urlparse(obj_link).hostname != hostname:
            continue
        image = requests.get(obj_link, headers=headers).content

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

    request = requests.get(url, headers=headers)
    if request.status_code == 404:
        print('Site with such url is not found!')
        return '<Error>'
    if request.status_code != 200:
        print('Internal Server Error')
        return '<Error>'

    with open(new_html_path, "w") as html_file:
        html_file.write(request.text)

    new_dir_path = f"{new_html_path[:-5]}_files"
    new_dir_name = os.path.split(new_dir_path)[1]
    try:
        os.mkdir(new_dir_path)
    except FileExistsError:
        print('You have not deleted files from this folder since the last \
               launch of the program!')
        return '<Error>'

    with open(new_html_path, "r+", encoding="utf-8") as file:
        hostname = urlparse(url).hostname
        soup = get_images(file.read(), new_dir_path, new_dir_name, hostname)
        file.seek(0)
        file.write(str(soup.prettify()))

    return new_html_path


if __name__ == "__main__":
    download('https://google.com/blyat', '/home/reyan/testdir')
