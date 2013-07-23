#!/usr/bin/env python
"""
Example of panning with pyo
"""
import pyo
import time
from pyospat import server

if __name__ == "__main__":
    s = server.ServerWrapper()

    noise = pyo.Noise(mul=.125)
    lfo = pyo.Sine(freq=1.0, mul=0.5, add=0.5)
    p = pyo.Pan(noise, outs=2, pan=lfo).out()

    s.run()

