#!/usr/bin/env python
"""
The Application class.
"""
import pyo
import time
from pyospat import server

class Application(object):
    def __init__(self, configuration):
        self._configuration = configuration
        addresses = ["/pitch", "/amp"]
        self._osc_receiver = pyo.OscDataReceive(self._configuration.osc_receive_port, addresses, self._on_message_received)
        self._sine = pyo.Sine(freq=0.0, mul=1.0).out()

    def _on_message_received(self, address, *args):
        print("%s %s" % (address, args))
        if address == "/pitch":
            self._sine.setFreq(args[0])
        elif address == "/amp":
            self._sine.setMul(args[0])
