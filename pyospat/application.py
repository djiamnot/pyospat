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
import pyo
from pyospat import server
from pyospat import maths
from txosc import osc
from txosc import dispatch
from txosc import async
import math

def distance_to_attenuation(distance):
    """
    Not working yet. Just returns 1.0
    """
    # TODO: compute distance_to_attenuation
    return 1.0

class Renderer(object):
    """
    Not used yet.
    """
    def __init__(self):
        # speakers coordinates:
        self._speaker0_angle = - math.pi / 2.0
        self._speaker1_angle = math.pi / 2.0
        # source:
        self._noise = pyo.Noise(mul=.125)
        # attenuator:
        self._mixer1 = pyo.Mixer(outs=1, chnls=1)
        self._mixer1.addInput(0, self._noise)
        self._mixer1.setAmp(0, 0, 0.0) # changed afterwhile
        # panner:
        self._pan1 = pyo.Pan(self._noise, outs=1, pan=0.0)
        self._pan2 = pyo.Pan(self._noise, outs=1, pan=0.0)
        self._mixer2 = pyo.Mixer(outs=2, chnls=1)
        # input 0:
        self._mixer2.addInput(0, self._pan1)
        self._mixer2.setAmp(0, 0, 1.0)
        self._mixer2.setAmp(0, 1, 0.0)
        # input 1:
        self._mixer2.addInput(1, self._pan2)
        self._mixer2.setAmp(1, 0, 0.0)
        self._mixer2.setAmp(1, 1, 1.0)
        self._mixer2.out()

    def _set_attenuation(self, linear_gain):
        self._mixer1.setAmp(0, 0, linear_gain)

    def set_distance_and_angle(self, distance, angle):
        print("Renderer::set_distance_and_angle(%f, %f)" % (distance, angle))
        attenuation = distance_to_attenuation(distance)
        self._set_attenuation(attenuation)
        self._set_angle(angle)

    def _set_angle(self, angle):
        self._pan1.setPan(self._speaker0_angle + angle)
        self._pan2.setPan(self._speaker1_angle + angle)

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
        self._renderer = Renderer()
        port_number = self._configuration.osc_receive_port
        self._receiver = dispatch.Receiver()
        from twisted.internet import reactor
        self._server_port = reactor.listenUDP(port_number, async.DatagramServerProtocol(self._receiver))
        print("Listening on osc.udp://localhost:%s" % (port_number))
        self._setup_osc_callbacks()

    def _setup_osc_callbacks(self):
        self._receiver.addCallback("/spatosc/core/*/*/xyz", self._handle_node_xyz)
        self._receiver.addCallback("/spatosc/core/connection/*/aed", self._handle_connection_aed)
        self._receiver.addCallback("/spatosc/core/connection/*/delay", self._handle_connection_delay)
        self._receiver.addCallback("/spatosc/core/scene/create_source", self._handle_create_source)
        self._receiver.addCallback("/spatosc/core/scene/create_listener", self._handle_create_listener)
        self._receiver.fallback = self._fallback

    def _handle_create_listener(self, message, address):
        """
        Handles /spatosc/core/scene/create_listener ,s node_id
        """
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "s"):
            return
        node_id = message.getValues()[0]

    def _handle_create_source(self, message, address):
        """
        Handles /spatosc/core/scene/create_source ,s node_id
        """
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "s"):
            return
        node_id = message.getValues()[0]

    def _handle_connection_delay(self, message, address):
        """
        Handles /spatosc/core/connection/*/delay ,f delay
        """
        # print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "f"):
            return
        connection_id = _get_connection_id(message)
        if connection_id is not None:
            pass #TODO

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
            xyz = maths.aed_to_xyz(message.getValues()) #FIXME: should not need to convert to xyz to get 2D angle
            angle = maths.angle(xyz, [1.0, 0.0, 0.0]) # FIXME: what is a 0 degrees angle in xyz notation?
            distance = message.getValues()[2]
            self._renderer.set_distance_and_angle(distance, angle)
            print("angle: %f distance: %f" % (angle, distance))
            pass #TODO

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

