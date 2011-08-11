#!/usr/bin/env python
"""
Example of panning with pyo
"""
import pyo
import time

SAMPLING_RATE = 44100
NUM_CHANNELS = 2

if __name__ == "__main__":
    s = pyo.Server(sr=SAMPLING_RATE, nchnls=NUM_CHANNELS).boot()
    s.start()

    noise = pyo.Noise(mul=.125)
    lfo = pyo.Sine(freq=1.0, mul=0.5, add=0.5)
    p = pyo.Pan(noise, outs=2, pan=lfo).out()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt, e:
        print("Interrupted")
    s.stop()

