#!/usr/bin/env python
"""
3D panner
"""
import pyo
import math
from pyoscape import server

class Panner3d(object):
    def __init__(self, azimuth=0.0, elevation=0.0):
        self._mixer = pyo.Mixer(outs=1, chnls=1, time=0.025)
        self._azimuth = 0.0
        self._elevation = 0.0
        self.set_position(azimuth, elevation)

    def set_position(self, azimuth, elevation):
        """
        Azimuth and elevation are in degrees.
        """
        self._azimuth = azimuth
        self._elevation = elevation
        gain = math.sin(math.radians(self._azimuth)) * math.cos(math.radians(self._elevation))
        self._mixer.setAmp(0, 0, gain)

    def get_output(self):
        return self._mixer[0][0]

    def add_input(self, signal, voice=0):
        self._mixer.addInput(voice, signal)

    def delete_input(self, voice=0):
        self._mixer.delInput(voice)

if __name__ == "__main__":
    pyo_server = server.ServerWrapper() # boots and starts a pyo.Server
    sine = pyo.Sine(freq=440.0, mul=0.125)

    # left
    left_panner = Panner3d()
    left_panner.add_input(sine)
    left_panner.set_position(90.0, 0.0)

    # right
    right_panner = Panner3d()
    right_panner.add_input(sine)
    right_panner.set_position(180 - 90.0, 0.0)

    # plug to dac
    left_panner.get_output().out(0)
    right_panner.get_output().out(1)

    pyo_server.run() # just a main loop

