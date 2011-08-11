#!/usr/bin/env python
"""
The ServerWrapper and PrefParser classes..
"""
import pyo
import time
import os
from xml.dom import minidom

class PrefParser(object):
    """
    Parses ~/.pyorc and provides kwargs for pyo.Server
    """
    def __init__(self, file_name=None):
        """
        @throws IOError if file is not found.
        """
        if file_name is None:
            file_name = os.path.expanduser("~/.pyorc")
        self._file_name = file_name
        self._constructor_arguments = {
            "sr": 44100,
            "buffersize": 256,
            "nchnls": 2,
            "duplex": 1,
            "audio": "portaudio",
            }
        self._parse()

    def _parse(self):
        if not os.path.exists(self._file_name):
            return
        parser = minidom.parse(self._file_name)
        root = parser.childNodes[0]
        for key in self._constructor_arguments.iterkeys():
            elements = root.getElementsByTagName(key)
            if len(elements) != 0:
                _type = type(self._constructor_arguments[key])
                text = elements[0].childNodes[0].toxml()
                self._constructor_arguments[key] = _type(text)
        print(self._constructor_arguments)
    
    def get_kwargs(self):
        """
        Provides kwargs for pyo.Server
        """
        return self._constructor_arguments

class ServerWrapper(object):
    """
    Encapsulates a pyo.Server and PrefParser
    """
    def __init__(self, config_file_name=None):
        parser = PrefParser(config_file_name)
        self._server = pyo.Server(**parser.get_kwargs()).boot()
        self._server.start()
        self._running = False

    def get_server(self):
        return self._server

    def run(self):
        """
        Runs a blocking main loop.
        """
        self._running = True
        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt, e:
            print("Interrupted")
        self._server.stop()

    def stop(self):
        """
        Stops the main loop
        """
        self._running = False

if __name__ == "__main__":
    # example:
    server = ServerWrapper()
    sine = pyo.Sine(freq=440.0, mul=0.125).out()
    server.run()

