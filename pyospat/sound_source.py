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
from pyospat import logger
from pyospat import maths
from pyospat import plugins
from types import ModuleType
import os
import sys
import pyo

#from pyospat.plugins import SimpleSin

log = logger.start(name="sound_source", level="info")

class SoundSource(object):
    """
    A sound source node in the renderer
    """
    def __init__(self, outs):
        """
        @param outs: number of outputs
        @type outs: int
        """
        log.debug("instantiating a soundsource... ")
        self._source = None
        self._is_connected_to_listener = False
        self._number_of_outputs = outs
        self._uri = None
        #todo: self._delay = pyo.delay()
        self._mixer = pyo.Mixer(outs=self._number_of_outputs, chnls=1, time=0.050)
        self._compressor = None
        self._previous_aed = [0.0, 0.0, 0.0]
        self._previous_speakers_angles = []
        self._spread = 8.0

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
        check if connected
        """
        if self._is_connected_to_listener:
            return True
        else:
            return False

    def set_delay(self, delay):
        """
        set delay time
        @param del: delay time
        @type del: float
        """
        log.debug("todo: soundsource::setdelay(%f)" % (delay))
        # self._delay.setdelay(delay)

    def _set_uri_adc(self, uri):
        """
        @rtype: bool
        """
        try:
            adc_num = int(uri.split("/")[-1])
        except indexerror, e:
            print(e)
            return False
        except typeerror, e:
            print(e)
            return False
        else:
            del self._source
            # todo: check if adc_num is a valid audio input
            log.debug(" set uri adc: %d" % (adc_num))
            self._source = pyo.input(chnl=adc_num)
            return True

    def _set_uri_pyo_generator(self, uri):
        """
        @rtype: bool
        """
        try:
            log.debug("*** pyo generator: trying to instantiate %s"%(uri))
            obj_name = uri.split("/")[-1]
            log.debug("*** object name is %s"%(obj_name))
            _pyobj = introspection.get_class(obj_name)
            log.debug("*** we got an object %s..."%(_pyobj))
            if introspection.class_has_property(_pyobj, 'input') and _pyobj is not "input":
                log.debug(obj_name, "is not a generator.")
                return False
            else:
                if self._source is not None:
                    #self._source().stop()
                    del self._source
                #fixme: handle things like sfplayer which need to be instantiated with some arguments...
                self._source = _pyobj()
                log.debug("*** pyo generator: instantiated %s" % (self._source))
                return True
        except indexerror, e:
            print(e)
            return False

    def _set_uri_pyo(self, uri):
        """
        @rtype: bool
        """
        try:
            obj_name = uri.split("/")[-1]
        except indexerror, e:
            print(e)
            return False
        if obj_name == "noise":
            log.debug("got noise!")
            if self._source is not None:
                log.debug("try to delete any existing source")
                del self._source
            log.debug("create noise")
            self._source = pyo.noise()
            log.debug("noise created at %s" %(self._source))
            return True
        else:
            log.warning("Pyo object {0} not supported, yet!".format(obj_name))
            return False

    def _set_uri_file(self, uri):
        """
        @rtype: bool
        """
        f_name = uri[7:]
        if os.path.exists(f_name):
            if self._source is not None:
                del(self._source)
                log.debug("Playing sound file: {0}".format(f_name))
                self._source = pyo.SfPlayer(f_name, loop=True)
            else:
                log.debug("Playing sound file: {0}".format(f_name))
                self._source = pyo.SfPlayer(f_name, loop=True)
            return True
        else:
            log.debug("File {0} does not exist.".format(f_name))
            return False

    def set_uri(self, uri):
        """
        Sets the source URI.
        Valid prefixes:
        * adc://
        * pyo://
        * file://
        """
        log.debug("setting URI to %s" % (uri))
        if self._uri == uri:
            return
        success = False
        if uri.startswith("adc://"):
            success = self._set_uri_adc(uri)
        # elif uri.startswith("pyo://"):
        #     success = self._set_uri_pyo(uri)
        elif uri.startswith("pyo://"):
            log.debug("*** Entering _set_uri_pyo_generator ***")
            success = self._set_uri_pyo_generator(uri)
#            success = self._set_uri_pyo(uri)
        elif uri.startswith("file://"):
            success = self._set_uri_file(uri)
        elif uri.startswith("plugin://"):
            success = self._set_uri_plugin(uri)
        else:
            log.debug("{0} is not a known URI path".format(uri))
        if success:
            log.debug("  * {0} was loaded".format(uri))
            self._uri = uri
            self._connect()
            self._set_aed_to_previous()
        else:
            log.debug("Failed to set source URI to %s" % (uri))

    def _set_uri_plugin(self, uri): 
        """
        Sets a URI to a custom plugin. Plugins are custom defined pyo classes
        that encapsulate various generators/operators to form complex instruments.
        Chaining audio pyo classes from pyospat is currently not supported.
        The URI is in the form of plugin://<path>
        @param uri: string
        """
        imported_plugin = ""
        plug_name = uri[9:]
        import_name = "pyospat.plugins." + plug_name
        log.debug("loading a plugin: {0} ".format(plug_name))
        #print("Searching the folowing paths: ")
        #print(sys.path)
        # del self._source
        # # FIXME: potentially dangerous...
            #self._source = exec(plug_name)
        try:
            imported_plugin = __import__(import_name, fromlist=[""])
            print(imported_plugin)
        except Exception, e:
            print(e)
        #_Pyo_plugin = introspection.get_plugin_class(imported_plugin)
        if self._source is not None:
            del self._source
        self._source = eval("imported_plugin." + plug_name + "()")
        log.debug("*** pyospat plugin: instantiated %s" % (self._source))
        return True

    def set_property(self, property_name, value):
        """
        Manipulate properties
        value type: tuple
        """
        if self._source is not None:
            props = introspection.get_instance_properties(self._source)
            log.debug(props)
            if property_name == "play":
                log.debug("trying to play: ")
                try:
                    self._source.play()
                except TypeError, e:
                    print(e)
            elif property_name == "stop":
                try:
                    self._source.stop()
                except TypeError, e:
                    print("Cannot stop because of {0}".format(e))
            elif property_name in props:
                log.debug("Set %s property %s to %s" %(self._source, property_name, str(value)))
                introspection.set_instance_property(self._source, property_name, value)
            else:
                log.debug("%s does not have %s property" % (self._source, property_name))

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
            log.debug("factor[%d]: %f" % (index, factor))
            index += 1
        self._previous_aed = aed
        self._previous_speakers_angles = speaker_angles
        
    def _connect(self):
        log.debug("%s attempts to connect %s" % (self, self._source))
        if self._source is not None:
            log.debug("%s is not empty so it should connect to mixer" % (self._source))
            self._compressor = pyo.Compress(self._source)
            self._mixer.addInput(0, self._compressor)
        # self._mixer.setAmp(0, 0, 0.5)
        # self._mixer.setAmp(0, 1, 0.5)
        if self._is_connected_to_listener:
            self._mixer.out()
        else:
            self._mixer.stop()

