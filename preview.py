#!/usr/bin/env python
"""Builds preview pages of the theme and starts a webserver if not already started
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from tempfile import TemporaryDirectory
from sphinx.cmd.build import build_main as sphinx_main

DEMO_SRC_DIR = Path(__file__).parent / "tests" / "sites" / "base"
BUILDER = "html"
PORT = 5000


def main() -> int:
    """Run a build and start a http server

    :return: Exit code for the process
    :rtype: int
    """
    with TemporaryDirectory() as build_dir:
        build_dir = Path(build_dir)
        build(BUILDER, DEMO_SRC_DIR, build_dir)
        return serve(build_dir, PORT)


def build(builder: str, source_dir: Path, build_dir: Path) -> int:
    """Build the demo pages from source_dir
    into build_dir using the builder

    :param builder: Sphinx builder type
    :type builder: str
    :param source_dir: Directory of source conf.py file
    :type source_dir: Path
    :param build_dir: Destination of built files
    :type build_dir: Path
    :return: Exit code from sphinx build
    :rtype: int
    """
    return sphinx_main(["-b", builder, str(source_dir), str(build_dir)])


def serve(serve_root: Path, port: int):
    """Start a http server on the given port

    :param serve_root: The root directory to serve the files
    :type serve_root: Path
    :param port: Serve on this port
    :type port: int
    """
    handler_class = partial(SimpleHTTPRequestHandler, directory=str(serve_root))
    with TCPServer(("", port), handler_class) as httpd:
        print(
            f"Serving HTTP on localhost port {port} " f"(http://localhost:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            return 0


if __name__ == "__main__":
    main()
