#!/usr/bin/env python
"""
Example of using a OSC receiver with Pyo.
"""
import pyo
import time
from pyospat import server

class Example(object):
    def __init__(self):
        self._port = 10001
        addresses = ["/pitch", "/amp"]
        self._osc_receiver = pyo.OscDataReceive(self._port, addresses, self._on_message_received)
        self._sine = pyo.Sine(freq=0.0, mul=1.0).out()

    def _on_message_received(self, address, *args):
        print("%s %s" % (address, args))
        if address == "/pitch":
            self._sine.setFreq(args[0])
        elif address == "/amp":
            self._sine.setMul(args[0])

if __name__ == "__main__":
    s = server.ServerWrapper()
    example = Example()
    s.run()
    # why does it often end with a segmentation fault?

