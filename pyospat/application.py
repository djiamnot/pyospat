#!/usr/bin/env python
"""
The Application class.
"""
import pyo
from pyospat import server
from txosc import osc
from txosc import dispatch
from txosc import async
class Renderer(object):
    def __init__(self):
        pass

def _type_tags_match(message, expected):
    if message.getTypeTags() == expected:
        return True
    else:
        print("Bad type tags for message %s. Expected %s" % (message, expected))
        return False

def _get_connection_id(message):
    try:
        connection_id = message.address.split("/")[3]
        return connection_id
    except IndexError, e:
        print(str(e))
        return None

def _get_node_id(message):
    try:
        connection_id = message.address.split("/")[3]
        return connection_id
    except IndexError, e:
        print(str(e))
        return None

class Application(object):
    def __init__(self, configuration):
        self._configuration = configuration
        self._renderer = Renderer()
        port_number = self._configuration.osc_receive_port
        self._receiver = dispatch.Receiver()
        from twisted.internet import reactor
        self._server_port = reactor.listenUDP(port_number, async.DatagramServerProtocol(self._receiver))
        print("Listening on osc.udp://localhost:%s" % (port_number))
        self._setup_osc_callbacks()

    def _setup_osc_callbacks(self):
        PREFIX = "/spatosc/core"
        self._receiver.addCallback(PREFIX + "/*/*/xyz", self._handle_node_xyz)
        self._receiver.addCallback(PREFIX + "/connection/*/aed", self._handle_connection_aed)
        self._receiver.addCallback(PREFIX + "/connection/*/delay", self._handle_connection_delay)
        self._receiver.addCallback(PREFIX + "/scene/create_source", self._handle_create_source)
        self._receiver.addCallback(PREFIX + "/scene/create_listener", self._handle_create_listener)
        self._receiver.fallback = self.fallback


    def _handle_create_listener(self, message, address):
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "s"):
            return
        node_id = message.getValues()[0]

    def _handle_create_source(self, message, address):
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "s"):
            return
        node_id = message.getValues()[0]

    def _handle_connection_delay(self, message, address):
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "f"):
            return
        connection_id = _get_connection_id(message)
        if connection_id is not None:
            pass #TODO

    def _handle_connection_aed(self, message, address):
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff"):
            return
        connection_id = _get_connection_id(message)
        if connection_id is not None:
            pass #TODO

    def _handle_node_xyz(self, message, address):
        print("  Got %s from %s" % (message, address))
        if not _type_tags_match(message, "fff"):
            return
        node_id = _get_node_id(message)
        if node_id is not None:
            pass #TODO

    def fallback(self, message, address):
        """
        Fallback for any unhandled message
        """
        print("  Got unkown path %s from %s" % (message, address))

