#!/usr/bin/env python
"""
setup.py for Pyoscape
Also sets up the man pages.

To update the version number : 
vim -o pyoscape/__init__.py
"""
from setuptools import setup
import sys
import pyoscape

setup(
    name="pyoscape",
    version=pyoscape.__version__,
    description="Python renderer for SpatOSC",
    author="SAT",
    author_email="alexandre@quessy.net",
    url="http://github.com/sat-metalab/pyoscape",
    packages=["pyoscape"],
    scripts=[]
    )
