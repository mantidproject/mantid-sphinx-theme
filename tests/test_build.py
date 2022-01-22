"""Verify a test build with Sphinx"""
import os
from pathlib import Path
from shutil import copytree

from bs4 import BeautifulSoup
import pytest
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

PATH_TESTS = Path(__file__).parent


class SphinxBuild:
    def __init__(self, app: SphinxTestApp, src: Path):
        self.app = app
        self.src = src

    def build(self):
        self.app.build()
        assert self.warnings == "", self.status
        return

    @property
    def warnings(self):
        return self.app._warning.getvalue()

    @property
    def status(self):
        return self.app._status.getvalue()

    @property
    def outdir(self):
        return self.app.outdir

    def html_tree(self, *path):
        path_page = self.outdir.joinpath(*path)
        if not path_page.exists():
            raise ValueError(f"{path_page} does not exist")
        return BeautifulSoup(path_page.read_text("utf8"), "html.parser")


@pytest.fixture()
def sphinx_build_factory(make_app, tmp_path):
    def _func(src_folder, **kwargs):
        copytree(PATH_TESTS / "sites" / src_folder, tmp_path / src_folder)
        app = make_app(
            srcdir=sphinx_path(os.path.abspath((tmp_path / src_folder))), **kwargs
        )
        return SphinxBuild(app, tmp_path / src_folder)

    yield _func


def test_build_html(sphinx_build_factory: SphinxBuild, file_regression):
    """Test building the base html template and config."""
    sphinx_build: SphinxBuild = sphinx_build_factory("base")

    # Basic build with defaults
    sphinx_build.build()
    assert (sphinx_build.outdir / "index.html").exists(), sphinx_build.outdir.glob("*")

    index_html = sphinx_build.html_tree("index.html")
    subpage_html = sphinx_build.html_tree("section1/index.html")

    # Navbar structure
    navbar = index_html.select("div#navbar-center")[0]
    file_regression.check(navbar.prettify(), basename="navbar_ix", extension=".html")

    # Navbar structure
    navbar = index_html.select("div#navbar-center")[0]
    file_regression.check(navbar.prettify(), basename="navbar_ix", extension=".html")

    # Sidebar structure
    sidebar = index_html.select(".bd-sidebar")[0]
    file_regression.check(sidebar.prettify(), basename="sidebar_ix", extension=".html")

    # Sidebar subpage
    sidebar = subpage_html.select(".bd-sidebar")[0]
    file_regression.check(
        sidebar.prettify(), basename="sidebar_subpage", extension=".html"
    )
