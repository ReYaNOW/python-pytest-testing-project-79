import argparse
import sys
import os
from page_loader import download


def make_parser():
    description = "web page downloader"
    parser = argparse.ArgumentParser(prog="page-loader",
                                     description=description)
    parser.add_argument(
        "url",
        type=str,
    )

    help_ = f"output directory, default is current ('{os.getcwd()}')"
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help=help_,
        type=str,
    )
    return parser


def main():
    parser = make_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()
    path = download(args.url, args.output)
    absolute_path = os.path.abspath(path)
    if path != '<Error>':
        print(f"Page was downloaded as '{absolute_path}'")


if __name__ == "__main__":
    main()
