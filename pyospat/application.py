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
import math
import pyo

from txosc import osc
from txosc import dispatch
from txosc import async

from pyospat import server
from pyospat import maths
from pyospat import sound_source as ss

class Renderer(object):
    """
    Actually renders audio.
    """
    def __init__(self, listener_id, speakers_angles):
        # speakers coordinates:
        self._speakers_angles = speakers_angles
        # ID
        self._listener_id = listener_id
        # sources:
        self._sources = {}

    def set_aed(self, source_name, aed):
        """
        Sets the aed of the single sound source.
        Distance must be > 0.0
        @param source_name: source name
        @type source_name: string
        @param aed: azimuth, elevation, distance
        @type aed: list
        """
        # TODO: handle more than one sound source.
        factor0 = maths.angles_to_attenuation(aed, self._speakers_angles[0])
        factor1 = maths.angles_to_attenuation(aed, self._speakers_angles[1])
        self._sources[source_name]._mixer.setAmp(0, 0, factor0)
        self._sources[source_name]._mixer.setAmp(0, 1, factor1)
        print("factors: %f %f" % (factor0, factor1))

    def add_source(self, source_name):
        """
        Add an audio source
        @param source_name: name of the source
        @type source_name: string
        @param type_name: type of the source
        @type type_name: object type
        @rtype: bool
        """
        if source_name not in self._sources:
            self._sources[source_name] = ss.SoundSource(2)
            return True
        else:
            return False

def _type_tags_match(message, expected):
    """
    Checks that some typetags string matches the expected.
    """
    if message.getTypeTags() == expected:
        return True
    else:
        print("Bad type tags for message %s. Expected %s" % (message, expected))
        return False

def _get_connection_id(message):
    """
    Split the path of a SpatOSC OSC URL to give the connection ID.
    """
    try:
        connection_id = message.address.split("/")[3]
        print(connection_id, " connected...")
        return connection_id
    except IndexError, e:
        print(str(e))
        return None

def _get_node_id(message):
    """
    Split the path of a SpatOSC OSC URL to give the node ID.
    """
    try:
        connection_id = message.address.split("/")[3]
        return connection_id
    except IndexError, e:
        print(str(e))
        return None

class Application(object):
    """
    Main class of this application.
    """
    def __init__(self, configuration):
        """
        @param configuration: Instance of a Configuration.
        """
        self._configuration = configuration
        self._speakers_angles = [
            [- math.pi / 4.0, 0.0, 0.0], # each speaker has an aed
            [math.pi / 4.0, 0.0, 0.0]
        ]
        self._renderer = Renderer('noise', self._speakers_angles)
        port_number = self._configuration.osc_receive_port
        self._receiver = dispatch.Receiver()
        from twisted.internet import reactor
        self._server_port = reactor.listenUDP(
            port_number, async.DatagramServerProtocol(self._receiver))
        print("Listening on osc.udp://localhost:%s" % (port_number))
        self._setup_osc_callbacks()

    def _setup_osc_callbacks(self):
        self._receiver.addCallback(
            "/spatosc/core/*/*/xyz", self._handle_node_xyz)
        self._receiver.addCallback(
            "/spatosc/core/connection/*/aed", self._handle_connection_aed)
        self._receiver.addCallback(
            "/spatosc/core/connection/*/delay", self._handle_connection_delay)
        self._receiver.addCallback(
            "/spatosc/core", self._handle_core)
        self._receiver.fallback = self._fallback

    def _handle_core(self, message, address):
        """
        Handles /spatosc/core ,ss command arg
        """
        # this seems to be different from the previous spatosc behaviour?
        print("  Got {0} from {1}".format(message, address))
        command = message.getValues()[0]
        if _type_tags_match(message, "ss"):
            arg = message.getValues()[1]
            if command == 'createSoundSource':
                self._renderer.add_source(arg)
                self._renderer._sources[arg].set_uri('pyo://Noise')
            elif command == 'createListener':
                print("Created listener: ", arg)
        elif _type_tags_match(message, "sss"):
            if command == 'connect':
                # TODO: handle connections?
                print("Got: ",message.getValues()[1:])

    def _handle_create_listener(self, message, address):
        """
        Handles /spatosc/core/scene/create_listener ,s node_id
        """
        print("  Got {} from {}".format(message, address))
        if not _type_tags_match(message, "s"):
            return
        node_id = message.getValues()[0]
        print("Created listener: ", note_id)

    def _handle_create_source(self, message, address):
        """
        Handles /spatosc/core/scene/create_source ,s node_id
        """
        print("  Got {} from {}".format(message, address))
        if not _type_tags_match(message, "ss"):
            return
        node_id = message.getValues()[0]
        self._renderer.add_source(node_id)
        print("Created source: ", node_id)

    def _handle_connection_delay(self, message, address):
        """
        Handles /spatosc/core/connection/*/delay ,f delay
        """
        # print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "f"):
            return
        connection_id = _get_connection_id(message)
        if connection_id is not None:
            # TODO: handle connection delay
            pass
            #self._renderer.set_delay(message.getValues()[0])

    def _handle_connection_aed(self, message, address):
        """
        Handles /spatosc/core/connection/*/aed ,fff azimuth elevation distance
        Azimuth and elevation are in radians.
        """
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff"):
            return
        connection_id = _get_connection_id(message)
        if connection_id is not None:
            #self._renderer.set_aed(message.getValues())
            aed = message.getValues()
            print("Getting {0} from {1}".format(aed,connection_id))
            self._renderer.set_aed('noise', aed)

    def _handle_node_xyz(self, message, address):
        """
        Handles /spatosc/core/*/*/xyz ,fff x y z
        """
        # print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff"):
            return
        node_id = _get_node_id(message)
        if node_id is not None:
            pass #TODO

    def _fallback(self, message, address):
        """
        Fallback for any unhandled message
        """
        # print("  Got unkown path %s from %s" % (message, address))

