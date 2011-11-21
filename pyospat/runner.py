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
from pyospat import application
from pyospat import configuration
from pyospat import server
from twisted.internet import error
import sys

DESCRIPTION = "Python audio renderer for SpatOSC"

def run():
    """
    Runs the application.
    """
    parser = OptionParser(usage="%prog [options]", version="%prog " + __version__, description=DESCRIPTION)
    parser.add_option("-v", "--verbose", action="store_true", help="Makes the output verbose.")
    parser.add_option("-p", "--osc-receive-port", type="int", default=10001, help="UDP port to listen to for OSC messages. Default is 10001")
    parser.add_option("-l", "--listener-id", type="string", default="listener0", help="ID of the listener in the spatosc scene")
    parser.add_option("-L", "--layout", type="string", default="STEREO", help="Speakers layout. One of STEREO, QUAD, OCTO")
    (options, args) = parser.parse_args()
    config = configuration.Configuration()
    if options.verbose:
        config.verbose = True
    if options.osc_receive_port:
        config.osc_receive_port = options.osc_receive_port
    if options.listener_id:
        config.listener_id = options.listener_id
    if options.layout:
        config.layout_name = options.layout

    s = server.ServerWrapper(use_twisted=True)
    try:
        app = application.Application(config)
    except error.CannotListenError, e:
        print(e)
        sys.exit(1)
    s.run()
    del app
    # why does it often end with a segmentation fault?

