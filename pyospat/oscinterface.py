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

from txosc import async
from txosc import dispatch
from twisted.internet import reactor
    
def _type_tags_match(message, expected, verbose=False):
    """
    Checks that some typetags string matches the expected.
    """
    if message.getTypeTags() == expected:
        return True
    else:
        if verbose:
            print("Bad type tags for message %s. Expected %s" % (message, expected))
        return False

def get_connection_id(message):
    """
    Split the path of a SpatOSC OSC URL to give the connection ID.
    Example input: /spatosc/core/connection/source0->listener0/gainDB
    Example output: source0->listener0
    """
    # TODO: test it
    try:
        connection_id = message.address.split("/")[4]
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

class OSCinterface(object):
    """
    Handle osc communication
    """
    def __init__(self, port_number, renderer):
        """
        @param port_number: UDP port for OSC
        @param renderer: L{pyospat.renderer.Renderer} object to pass commands to
        @type _server_port: L{twisted.reactor.listenUDP} object
        @type _renderer: L{pyospat.renderer.Renderer} object
        """
        self._receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(
            port_number, async.DatagramServerProtocol(self._receiver))
        print("Listening on osc.udp://localhost:%s" % (port_number))
        self._renderer = renderer
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
        self._receiver.addCallback(
            "/spatosc/core/*/*/prop", self._handle_node_property)
        self._receiver.fallback = self._fallback

    def _handle_core(self, message, address):
        """
        Handles /spatosc/core ,ss command arg
        """
        # this seems to be different from the previous spatosc behaviour?
        print("  Got {0} from {1}".format(message, address))
        command = message.getValues()[0]
        if _type_tags_match(message, "s"):
            if command == "clear":
                self._renderer.clear_scene()
        elif _type_tags_match(message, "ss"):
            if command == "createSoundSource":
                node_id = message.getValues()[1]
                self._renderer.add_source(node_id)
#                self._renderer.set_uri(node_id, "pyo://Noise")
            elif command == "createListener":
                arg = message.getValues()[1]
                print("create listener: %s" % (arg))
                self._renderer.add_listener(arg)
                del arg
            elif command == "deleteNode":
                node_id = message.getValues()[1]
                if self._renderer.has_source(node_id):
                    self._renderer.delete_source(node_id)

        elif _type_tags_match(message, "sss"):
            if command == "connect":
                # TODO: handle connections
                source_name = message.getValues()[1]
                listener_name = message.getValues()[2]
                self._renderer.set_connected(source_name, listener_name)

    def _handle_node_property(self, message, address):
        """
        Handles /spatosc/core/<type>/<node>/prop ,s[sfi] command arg
        """
        # this seems to be different from the previous spatosc behaviour?
        print("  Got {0} from {1}".format(message, address))
        node_id = message.address.split("/")[4]
        if not self._renderer.has_source(node_id):
            print("No such source node: " + node_id)
            print(str(self._renderer))
            return
        property_name = message.getValues()[0]
        value = message.getValues()[1]
        if _type_tags_match(message, "ss", verbose=True): # string property
            if property_name == "uri":
                self._renderer.set_uri(node_id, value)
            else:
                self._renderer.set_node_property(node_id, property_name, value)
        else:
            self._renderer.set_node_property(node_id, property_name, value)

    def _handle_create_listener(self, message, address):
        """
        Handles /spatosc/core/scene/create_listener ,s node_id
        """
        print("  Got {} from {}".format(message, address))
        if not _type_tags_match(message, "s", verbose=True):
            return
        node_id = message.getValues()[0]
        print("Created listener: ", node_id)

    def _handle_create_source(self, message, address):
        """
        Handles /spatosc/core/scene/create_source ,s node_id
        """
        print("  Got {} from {}".format(message, address))
        if not _type_tags_match(message, "ss", verbose=True):
            return
        node_id = message.getValues()[0]
        self._renderer.add_source(node_id)
        print("Created source: ", node_id)

    def _handle_connection_delay(self, message, address):
        """
        Handles /spatosc/core/connection/*/delay ,f delay
        """
        # print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "f", verbose=True):
            return
        connection_id = get_connection_id(message)
        if connection_id is not None:
            try:
                from_id = connection_id.split("->")[0] #FIXME
                to_id = connection_id.split("->")[1] #FIXME
                if self._renderer.get_listener_id() == to_id:
                    delay = message.getValues()[0]
                    self._renderer.set_delay(from_id, delay)
            except KeyError, e:
                print(e)

    def _handle_connection_aed(self, message, address):
        """
        Handles /spatosc/core/connection/*/aed ,fff azimuth elevation distance
        Azimuth and elevation are in radians.
        """
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff", verbose=True):
            return
        connection_id = get_connection_id(message)
        if connection_id is not None:
            try:
                from_id = connection_id.split("->")[0] #FIXME
                to_id = connection_id.split("->")[1] #FIXME
                print("Connecting from %s to %s" % (from_id, to_id))
                if self._renderer.get_listener_id() == to_id:
                    aed = message.getValues() # 3 floats list
                    print("%s -> %s has AED: %s" % (from_id, to_id, aed))
                    self._renderer.set_aed(from_id, aed)
                else:
                    print("%s No such node: %s" % (self, from_id))
            except KeyError, e:
                print(e)

    def _handle_node_xyz(self, message, address):
        """
        Handles /spatosc/core/*/*/xyz ,fff x y z
        """
        # print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff", verbose=True):
            return
        node_id = _get_node_id(message)
        if node_id is not None:
            pass #TODO

    def _fallback(self, message, address):
        """
        Fallback for any unhandled message
        """
        print("  fallback: Got %s from %s" % (message, address))
