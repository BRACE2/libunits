#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io, re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwds):
    path = join(dirname(__file__), *names)
    with io.open(path, encoding=kwds.get("encoding", "utf8")) as f:
        return f.read()

long_description = "%s\n" % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.md")
        )
    )


setup(
    name="elle_units",
    description="Utilities for managing units in calculations",
    version="0.0.3",
    long_description=long_description,
    author="Claudio Perez",
    author_email="claudio_perez@berkeley.edu",
    url="https://github.com/claudioperez/elle-units",

    namespace_packages=["elle"],
    packages=["elle.units"],
    # package_data={'elle.units':['data/*.json']},
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
    ],
)
