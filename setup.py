#!/usr/bin/env python
"""
setup.py for Pyospat
Also sets up the man pages.

To update the version number : 
vim -o pyospat/__init__.py
"""
from setuptools import setup
import sys
import pyospat

setup(
    name="pyospat",
    version=pyospat.__version__,
    description="Python audio renderer for SpatOSC",
    author="SAT",
    author_email="alexandre@quessy.net",
    url="http://github.com/sat-metalab/pyospat",
    packages=["pyospat"],
    scripts=[]
    )
