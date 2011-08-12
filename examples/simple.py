#!/usr/bin/env python
"""
Uses the ServerWrapper class
"""
import pyo
from pyospat import server

if __name__ == "__main__":
    pyo_server = server.ServerWrapper()
    sine = pyo.Sine(freq=440.0, mul=0.125).out()
    pyo_server.run()

