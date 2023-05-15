import os
import requests


def url_to_filename(url: str):
    new_url = url.replace("https://", "").replace("http://", "")
    result = ""
    for char in new_url:
        if not char.isdigit() and not char.isalpha():
            result += "-"
        else:
            result += char

    result += ".html"
    return result


def download(url: str, path: str = os.getcwd()) -> str:
    new_file_name = url_to_filename(url)
    new_path = os.path.join(path, new_file_name)

    request = requests.get(url)
    with open(new_path, "w") as file:
        file.write(request.text)
    return new_path
