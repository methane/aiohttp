"""
Example of serving an Application using the `aiohttp.web` CLI.

Serve this app using::

    $ python -m aiohttp.web -H localhost -P 8080 --repeat 10 web_app.init \
    > "Hello World"

Here ``--repeat`` & ``"Hello World"`` are application specific command-line
arguments. `aiohttp.web` only parses & consumes the command-line arguments it
needs (i.e. ``-H``, ``-P`` & ``entry-func``) and passes on any additional
arguments to the `web_app.init` function for processing.
"""

from aiohttp.web import Application, Response
from argparse import ArgumentParser


def display_message(req):
    args = req.app["args"]
    text = "\n".join([args.message] * args.repeat)
    return Response(text=text)


def init(args):
    arg_parser = ArgumentParser(
        prog="aiohttp.web ...", description="Application CLI", add_help=False
    )

    # Positional argument
    arg_parser.add_argument(
        "message",
        help="message to print"
    )

    # Optional argument
    arg_parser.add_argument(
        "--repeat",
        help="number of times to repeat message", type=int, default="1"
    )

    # Avoid conflict with -h from `aiohttp.web` CLI parser
    arg_parser.add_argument(
        "--app-help",
        help="show this message and exit", action="help"
    )

    parsed_args = arg_parser.parse_args(args)

    app = Application()
    app["args"] = parsed_args
    app.router.add_route('GET', '/', display_message)

    return app
