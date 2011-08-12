#!/usr/bin/env python
"""
The Runner function.
"""
from optparse import OptionParser
from pyospat import __version__
from pyospat import server
from pyospat import application
import os
import pyo
import sys
import time

DESCRIPTION = "Python audio renderer for SpatOSC"

class Configuration(object):
    """
    Configuration for the application.
    """
    def __init__(self):
        self.verbose = False
        self.osc_receive_port = 10001

def run():
    """
    Runs the application.
    """
    parser = OptionParser(usage="%prog [options]", version="%prog " + __version__, description=DESCRIPTION)
    parser.add_option("-v", "--verbose", action="store_true", help="Makes the output verbose.")
    (options, args) = parser.parse_args()
    configuration = Configuration()
    if options.verbose:
        configuration.verbose = True

    s = server.ServerWrapper()
    app = application.Application(configuration)
    s.run()
    # why does it often end with a segmentation fault?

