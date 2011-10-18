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
SoundSource class
"""

class SoundSource(Node):
    """
    Creates sound nodes in the renderer
    """

    def __init__(self, outs):
        """
        @param outs: number of outputs
        @type outs: int
        """
        self._is_connected_to_listener = True
        self._number_of_outputs = outs
        self._delay = pyo.Delay()
        self._mixer = pyo.Mixer(outs=self._number_of_outputs, chnls=1, time=0.050)

    def __del__(self):
        pass

    def set_connected(self, connected):
        """
        @param connected: bool
        """

    def get_connected(self):
        """
        Check if connected
        """
        if self._is_connected_to_listener:
            return True
        else:
            return False

    def set_delay(self, del):
        """
        Set delay time
        @param del: delay time
        @type del: float
        """
        self._delay.setDelay(del)

    set relative_aed(self, aed):
        """
        @param aed: azimuth, elevation, distance
        @type aed: list
        """

        
