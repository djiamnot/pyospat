#!/usr/bin/env python
"""
Example of using a OSC receiver with Pyo.
"""
import pyo
import time

SAMPLING_RATE = 44100
NUM_CHANNELS = 2

if __name__ == "__main__":
    s = pyo.Server(sr=SAMPLING_RATE, nchnls=NUM_CHANNELS).boot()
    s.start()
    a = pyo.OscReceive(port=10001, address=['/pitch', '/amp'])
    b = pyo.Sine(freq=a['/pitch'], mul=a['/amp']).out()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt, e:
        print("Interrupted")
    s.stop()

