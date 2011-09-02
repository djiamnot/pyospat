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

def map_from_zero_to_one(value):
    """
    Maps a value in the range [-1.0, 1.0] to the range [0.0, 1.0]
    @param value: float in the range [-1.0, 1.0]
    @rtype: float
    """
    return value * 0.5 + 0.5

def attenuate_according_to_angle(angle):
    """
    Computes attenuation per speaker (0..1)
    @param angle: radian
    @rtype: float
    """
    return map_from_zero_to_one(math.cos(angle))

def spread(value, exponent=2):
    """
    Apply spread factor (according to constant total power)
    @param value: input
    @param exponent: exponent, default=2
    @rtype: float
    """
    #TODO: give this a better name
    return math.pow(value, factor)

def angle_to_attenuation(speaker_aed, source_aed, exponent=2.0):
    """
    @param speaker_aed: AED position of the loudspeaker.
    @param source_aed: AED position of the sound source.
    @rtype: float
    @return: Audio level factor.
    """
    aed = maths.add(speaker_aed, source_aed)
    factor = 1.0
    factor *= spread(angle_to_attenuation(aed[0]), exponent)
    factor *= spread(angle_to_attenuation(aed[1]), exponent)
    # TODO: factor *= distance_to_attenuation(aed[2])
    return factor

class Renderer(object):
    """
    Actually renders audio.
    """
    def __init__(self):
        # speakers coordinates:
        self._speakers_angles = [
            [- math.pi / 4.0, 0.0, 0.0], # each speaker has an aed
            [math.pi / 4.0, 0.0, 0.0]
        ]
        # source:
        self._noise = pyo.Noise(mul=1.0)

        # variable delay:
        self._delay = pyo.Delay(self._noise, delay=0.0, maxdelay=1.0)

        # attenuator:
        self._mixer = pyo.Mixer(outs=2, chnls=1, time=0.050)
        self._mixer.addInput(0, self._delay)
        self._mixer.setAmp(0, 0, 0.125) # vin, vout, amp changed afterwhile
        self._mixer.setAmp(0, 1, 0.125) # changed afterwhile
        self._mixer.out()

    def set_delay(self, delay):
        """
        Changes the variable delay duration, for Doppler effect and a realistic rendering.
        @param delay: Duration in seconds.
        """
        # TODO: the binaural renderer should have a different variable delay for each ear.
        self._delay.setDelay(delay)

    def set_aed(self, aed):
        factor0 = factor_from_positions(aed, self._speakers_angles[0])
        factor1 = factor_from_positions(aed, self._speakers_angles[1])
        self._mixer.setAmp(0, 0, factor0)
        self._mixer.setAmp(0, 1, factor1)
        print("factors: %f %f" % (factor0, factor1))

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
            self._renderer.set_delay(message.getValues()[0])

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
            self._renderer.set_aed(message.getValues())

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

