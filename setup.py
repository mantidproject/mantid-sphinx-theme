#!/usr/bin/env python

from setuptools import setup
import mantid_sphinx_theme

setup(
    name="mantid_sphinx_theme",
    version=mantid_sphinx_theme.__version__,
    url="https://github.com/martyngigg/mantid_sphinx_theme",
    license="BSD",
    author="Mantid Developers",
    description="Mantid Project theme for Sphinx",
    long_description=open("README.md").read(),
    zip_safe=False,
    packages=["mantid_sphinx_theme"],
    include_package_data=True,
    # http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
    entry_points={
        "sphinx.html_themes": [
            "mantid_sphinx_theme = mantid_sphinx_theme",
        ]
    },
    install_requires=open("requirements.txt").read().strip().split("\n"),
)
