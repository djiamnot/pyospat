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
    parser.add_option("-p", "--osc-receive-port", type="int", help="UDP port to listen to for OSC messages.")
    (options, args) = parser.parse_args()
    config = configuration.Configuration()
    if options.verbose:
        config.verbose = True
    if options.osc_receive_port:
        config.osc_receive_port = options.osc_receive_port

    s = server.ServerWrapper(use_twisted=True)
    app = application.Application(config)
    s.run()
    # why does it often end with a segmentation fault?

