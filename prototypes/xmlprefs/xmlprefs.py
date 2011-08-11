#!/usr/bin/env python
"""
Example of reading XML file for Pyo preferences
"""
import pyo
import time
import os
from xml.dom import minidom

class PrefParser(object):
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
        return self._constructor_arguments

if __name__ == "__main__":
    parser = PrefParser()
    s = pyo.Server(**parser.get_kwargs()).boot()
    s.start()

    sine = pyo.Sine(freq=440.0, mul=0.125).out()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt, e:
        print("Interrupted")
    s.stop()

