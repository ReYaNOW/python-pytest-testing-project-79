import os
import requests
from requests.exceptions import MissingSchema, ConnectionError


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) \
            Gecko/20100101 Firefox/112.0"
}


def request_errors_handler(url):
    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
        return request

    except MissingSchema:
        if '.' not in url:
            raise MissingSchema("Not correct URL!")
        raise MissingSchema(f"Your url: '{url}', there http or https is \
missing")

    except ConnectionError:
        raise ConnectionError("Not correct URL!")


def io_errors_handler(type, path, request):
    match type:
        case "file":
            try:
                with open(path, "w") as html_file:
                    html_file.write(request.text)
            except FileNotFoundError:
                raise FileNotFoundError(f"Directory does not exist \
here! {path}")

            except PermissionError:
                path = os.path.split(path)[0]
                raise PermissionError(f"Insufficient permissions to create a \
{type} in {path} !")

        case "directory":
            try:
                os.mkdir(path)

            except FileExistsError:
                path = os.path.split(path)[0]
                raise FileExistsError(f"You have not deleted files from this \
folder ({path}) since the last launch of the program!")
