#! /usr/bin/env python3

from distutils.core import setup

setup(
    name = "python-eeschema",
    version = "0.1",
    packages = ["eeschema"],
    scripts = ["bin/csvtokicad"],
    description = "Python library for manipulating KiCad's EESchema library files",
    author = "Josef Gajdusek",
    author_email = "atx@atx.name",
    url = "https://github.com/atalax/python-kicad",
    keywords = ["kicad", "cad", "eda"],
    license = "MIT",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        ]
    )
