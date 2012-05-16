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
The SoundSource class
"""
from pyospat import introspection
from pyospat import maths
import os
import pyo

class SoundSource(object):
    """
    A sound source node in the renderer
    """
    def __init__(self, outs):
        """
        @param outs: number of outputs
        @type outs: int
        """
        print("instantiating a SoundSource... ")
        self._source = None
        self._is_connected_to_listener = False
        self._number_of_outputs = outs
        self._uri = None
        #TODO: self._delay = pyo.Delay()
        self._mixer = pyo.Mixer(outs=self._number_of_outputs, chnls=1, time=0.050)
        self._previous_aed = [0.0, 0.0, 0.0]
        self._previous_speakers_angles = []
        self._spread = 2.0
        print("Done")

    def __del__(self):
        del self._source
        del self._mixer
        #del self._delay
            
    def set_connected(self, connected):
        """
        @param connected: bool
        """
        self._is_connected_to_listener = connected
        self._connect()

    def get_connected(self):
        """
        Check if connected
        """
        if self._is_connected_to_listener:
            return True
        else:
            return False

    def set_delay(self, delay):
        """
        Set delay time
        @param del: delay time
        @type del: float
        """
        print("TODO: SoundSource::setDelay(%f)" % (delay))
        # self._delay.setDelay(delay)

    def _set_uri_adc(self, uri):
        """
        @rtype: bool
        """
        try:
            adc_num = int(uri.split("/")[-1])
        except IndexError, e:
            print(e)
            return False
        except TypeError, e:
            print(e)
            return False
        else:
            del self._source
            # TODO: check if adc_num is a valid audio input
            print(" set URI ADC: %d" % (adc_num))
            self._source = pyo.Input(chnl=adc_num)
            return True

    def _set_uri_pyo_generator(self, uri):
        """
        @rtype: bool
        """
        try:
            print("*** pyo generator: Trying to instantiate %s"%(uri))
            obj_name = uri.split("/")[-1]
            print("*** Object name is %s"%(obj_name))
            _Pyobj = introspection.get_class(obj_name)
            print("*** We got an object %s..."%(_Pyobj))
            if introspection.class_has_property(_Pyobj, 'input'):
                print obj_name, "is not a generator."
                return False
            else:
                if self._source is not None:
                    #self._source().stop()
                    del self._source
                self._source = _Pyobj()
                print("*** pyo generator: apparent success...")
                return True
        except IndexError, e:
            print(e)
            return False

    def _set_uri_pyo(self, uri):
        """
        @rtype: bool
        """
        try:
            obj_name = uri.split("/")[-1]
        except IndexError, e:
            print(e)
            return False
        if obj_name == "Noise":
            print("Got Noise!")
            if self._source is not None:
                print("try to delete any existing source")
                del self._source
            print("Create noise")
            self._source = pyo.Noise()
            print("Noise created at %s" %(self._source))
            return True
        else:
            print("Pyo object {0} not supported, yet!".format(obj_name))
            return False

    def _set_uri_file(self, uri):
        """
        @rtype: bool
        """
        f_name = uri[7:]
        if os.path.exists(f_name):
            del self._source
            print("Playing sound file: %s" % (f_name))
            self._source = pyo.SfPlayer(f_name, loop=True)
            return True
        else:
            print("Sound file %s does not exist." % (f_name))
            return False

    def set_uri(self, uri):
        """
        Sets the source URI.
        Valid prefixes:
        * adc://
        * pyo://
        * file://
        """
        print("setting URI to %s" % (uri))
        if self._uri == uri:
            return
        success = False
        if uri.startswith("adc://"):
            success = self._set_uri_adc(uri)
        # elif uri.startswith("pyo://"):
        #     success = self._set_uri_pyo(uri)
        elif uri.startswith("pyo://"):
            print("*** Entering _set_uri_pyo_generator ***")
            success = self._set_uri_pyo_generator(uri)
#            success = self._set_uri_pyo(uri)
        elif uri.startswith("file://"):
            success = self._set_uri_file(uri)
        if success:
            self._uri = uri
            self._connect()
            self._set_aed_to_previous()
        else:
            print("Failed to set source URI to %s" % (uri))

    def _set_aed_to_previous(self):
        self.set_relative_aed(self._previous_aed, self._previous_speakers_angles)

    def set_spread(self, spread):
        self._spread = float(spread)
            
    def set_relative_aed(self, aed, speaker_angles):
        """
        @param aed: azimuth, elevation, distance
        @param speaker_angles: list of aed for each speaker
        @type aed: list
        @type speaker_angles: list
        """
        # TODO: set_xyz should call this
        index = 0
        for angle in speaker_angles:
            factor = maths.angles_to_attenuation(aed, angle, self._spread)
            self._mixer.setAmp(0, index, factor)
            print("factor[%d]: %f" % (index, factor))
            index += 1
        self._previous_aed = aed
        self._previous_speakers_angles = speaker_angles
        
    def _connect(self):
        print("%s attempts to connect %s" % (self, self._source))
        if self._source is not None:
            print("%s is not empty so it should connect to mixer" % (self._source))
            self._mixer.addInput(0, self._source)
        # self._mixer.setAmp(0, 0, 0.5)
        # self._mixer.setAmp(0, 1, 0.5)
        if self._is_connected_to_listener:
            self._mixer.out()
        else:
            self._mixer.stop()

