#!/usr/bin/env python
"""
The Runner function.
"""
from optparse import OptionParser
from pyospat import __version__
from pyospat import server
from pyospat import application
from pyospat import configuration
import os
import pyo
import sys
import time

DESCRIPTION = "Python audio renderer for SpatOSC"

def run():
    """
    Runs the application.
    """
    parser = OptionParser(usage="%prog [options]", version="%prog " + __version__, description=DESCRIPTION)
    parser.add_option("-v", "--verbose", action="store_true", help="Makes the output verbose.")
    (options, args) = parser.parse_args()
    config = configuration.Configuration()
    if options.verbose:
        config.verbose = True

    s = server.ServerWrapper(use_twisted=True)
    app = application.Application(config)
    s.run()
    # why does it often end with a segmentation fault?

