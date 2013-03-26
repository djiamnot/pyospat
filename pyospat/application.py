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
The Application class.
"""
from pyospat import renderer
from pyospat import speakerlayouts as layouts
from pyospat import logger
from pyospat import oscinterface as OSC
import math

log = logger.start(name="application")

class Application(object):
    """
    Main class of this application.
    """
    def __init__(self, configuration):
        """
        @param configuration: Instance of a Configuration.
        """
        self._configuration = configuration
        log.debug("*** starting with configuration:")
        log.debug(self._configuration)
        self._speakers_angles = [
            [- math.pi / 4.0, 0.0, 1.0], # each speaker has an aed
            [math.pi / 4.0, 0.0, 1.0]
        ]
        if self._configuration.layout_name == "STEREO":
            self._speakers_angles = layouts.STEREO
        if self._configuration.layout_name == "QUAD":
            self._speakers_angles = layouts.QUAD
        if self._configuration.layout_name == "OCTO":
            self._speakers_angles = layouts.OCTO
        if self._configuration.layout_name == "SATDOME":
            self._speakers_angles = layouts.SATDOME
        if self._configuration.layout_name == "DOME8x8":
            self._speakers_angles = layouts.DOME8x8

        self._renderer = renderer.Renderer(configuration.listener_id, self._speakers_angles)
        port_number = self._configuration.osc_receive_port
        OSC.OSCinterface(port_number, self._renderer)
        
