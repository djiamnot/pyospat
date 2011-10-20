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
import os
import pyo

class SoundSource(Object):
    """
    Creates sound nodes in the renderer
    """

    def __init__(self, outs):
        """
        @param outs: number of outputs
        @type outs: int
        """
        self._source = None
        self._is_connected_to_listener = True
        self._number_of_outputs = outs
        #self._delay = pyo.Delay()
        self._mixer = pyo.Mixer(outs=self._number_of_outputs, chnls=1, time=0.050)

    def __del__(self):
        del self._source
        del self._mixer
        #del self._delay
            
    def set_connected(self, connected):
        """
        @param connected: bool
        """
        self._is_connected_to_listener = connected
        # TODO: mute object if false.

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

    def set_uri(self, uri):
        if uri.startswith('adc://'):
            try:
                adc_num = int(uri.split('/')[-1])
            except IndexError, e:
                print(e)
                return False
            except TypeError, e:
                print(e)
                return False
            # TODO: check for ':'
            self._source = pyo.Input(chnl = adc_num)
        elif uri.startswith('pyo://'):
            try:
                obj_name = uri.split('/')[-1]
            except:
                IndexError, e:
                    print(e)
                    return False
            if obj_name == 'Noise':
                self._source = pyo.Noise()
                return True
            else:
                print("Pyo object {} not supported, yet!".format(obj_name))
                return False
        elif uri.startswith('file://'):
            f_name = uri[6:]
            if os.path.exist(f_name)
                self._source = pyo.SfPlayer(f_name, loop = True)
                return True
            else:
                print("Sound file does not exist.")
                return False
            
    def set_relative_aed(self, aed):
        """
        @param aed: azimuth, elevation, distance
        @type aed: list
        """
        factor0 = maths.angles_to_attenuation(aed, self._speakers_angles[0])
        factor1 = maths.angles_to_attenuation(aed, self._speakers_angles[1])
        self._mixer.setAmp(0, 0, factor0)
        self._mixer.setAmp(0, 1, factor1)
        
    def _connect(self):
        self._mixer.addInput(0, self._source)
        
