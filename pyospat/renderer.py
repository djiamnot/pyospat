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

from pyospat import sound_source
from pyospat import introspection
from pyospat import logger

log = logger.start(name="renderer", level="info")

PROPERTY_SPREAD = "setSpread"

class Renderer(object):
    """
    Actually renders audio.
    """
    def __init__(self, listener_id, speakers_angles):
        # speakers coordinates:
        self._speakers_angles = speakers_angles
        # ID
        self._listener_id = listener_id
        log.debug("New renderer instance with listener %s" % (self._listener_id))
        # sources:
        self._sources = {}

    def get_listener_id(self):
        """
        Returns our listener ID.
        @rtype: str
        """
        return self._listener_id

    def add_listener(self, listener_id):
        """
        Add listener
        @param listener_id: name of the listener
        @type listener_id: string
         @rtype: bool
        """
        log.debug("entered renderer.add_listener()")
        if listener_id not in self._listener_id:
            log.debug("will add make %s"%(listener_id))
            self._listener_id = listener_id
            log.debug("Success adding listener %s" % (self._listener_id))
            return True
        else:
            log.debug("Already have listener named %s" % (listener_id))
            return False

    def set_connected(self, source_id, listener_id, connected=True):
        if listener_id == self._listener_id:
            if self.has_source(source_id):
                self._sources[source_id].set_connected(connected)
    
    def set_uri(self, source_name, uri):
        """
        Sets the URI of a node.
        URI might be one of:
        * pyo://Noise
        * adc://0
        * adc://1
        * adc://2
        * ...
        @return success
        @rtype bool
        """
        if self.has_source(source_name):
            log.debug("renderer will call set_uri() on %s"%(self._sources[source_name]))
            self._sources[source_name].set_uri(uri)
            log.debug("Success seting URI %s to %s" % (uri, source_name))
            return True
        else:
            return False

    def set_aed(self, source_name, aed):
        """
        Sets the aed of the single sound source.
        Distance must be > 0.0
        @param source_name: source name
        @type source_name: string
        @param aed: azimuth, elevation, distance
        @type aed: list
        """
        if self.has_source(source_name):
            self._sources[source_name].set_relative_aed(aed, self._speakers_angles)
        else:
            log.debug("%s No such node: %s" % (self, source_name))

    def set_delay(self, source_name, delay):
        """
        Sets the delay of the single sound source.
        @param source_name: source name
        @type source_name: string
        @param delay: delay
        @type delay: float
        """
        if self.has_source(source_name):
            if delay < 0.0:
                log.warning("Negative delay? %f" % (delay))
                delay = 0.0
            self._sources[source_name].set_delay(delay)

    def set_node_property(self, node_id, property_name, value):
        """
        handles node property changes.
        """
        log.debug("set_node_property called with node:%s prop:%s value:%s" % (node_id, property_name, str(value)))
        if node_id == self._listener_id:
            if property_name == PROPERTY_SPREAD:
                try:
                    self._set_spread(float(value))
                except ValueError, e:
                    print(str(e))
        if node_id in self._sources:
            log.debug("%s is in sources..." % (node_id))
            log.debug("setting %s's property %s to %s" % (node_id, property_name, str(value)))
            self._sources[node_id].set_property(property_name, value)

    def _set_spread(self, spread=2.0):
        """
        sets the spread for each speaker.
        """
        for source in self._sources.itervalues():
            source.set_spread(spread)

    def has_source(self, source_name):
        log.debug("We have the source: %s" % (self._sources.keys()))
        return source_name in self._sources.keys()

    def get_number_of_speakers(self):
        """
        Count the speakers
        """
        return len(self._speakers_angles)

    def add_source(self, source_name):
        """
        Add an audio source
        @param source_name: name of the source
        @type source_name: string
        @param type_name: type of the source
        @type type_name: object type
        @rtype: bool
        """
        log.debug("entered renderer.add_source()")
        if source_name not in self._sources:
            log.debug("will instantiate %s"%(source_name))
            self._sources[source_name] = sound_source.SoundSource(self.get_number_of_speakers())
            log.debug("Success instantiating %s at %s" % (source_name, self._sources[source_name]))
            return True
        else:
            log.warning("Already have sound source %s" % (source_name))
            return False

    def delete_source(self, source_name):
        log.debug("delete_source(%s)" % (source_name))
        if source_name in self._sources:
            del self._sources[source_name]
        else:
            log.debug("Could not find sound source %s" % (source_name))
            return False

    def clear_scene(self):
        log.warning("clear_scene()!")
        for k in self._sources.keys():
            del self._sources[k]

    def __str__(self):
        ret = ""
        ret += "Renderer source nodes:"
        if len(self._sources) == 0:
            ret += "\n (none)"
        else:
            for k, v in self._sources.iteritems():
                ret += "\n * " + k
        return ret
