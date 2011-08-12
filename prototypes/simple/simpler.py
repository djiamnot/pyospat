import pyo

s = pyo.Server(sr=44100, nchnls=2).boot()
s.start()

w = pyo.Sine(freq=200, mul=0.5).out()
