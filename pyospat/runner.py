#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pyospat
# Copyright (C) 2011 Alexandre Quessy
# Copyright (C) 2011 Michal Seta
#
# This file is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Pyospat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyospat.  If not, see <http://www.gnu.org/licenses/>.

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

