#!/usr/bin/env python
# -*- coding: latin-1 -*-

import random
from pyo import *

class SimpleWaveguide(PyoObject):
    def __init__(self, freq=110, dur=1, deviation=1, mul=0.5, add=1):
        PyoObject.__init__(self)
        self._freq = freq
        self._trig = Trig().play()
        self._deviation = Randi(min=0.-deviation, max=deviation, freq=random.uniform(2,4), add=1)
        self._table = CosTable([(0,0),(50,1),(300,0),(8191,0)])
        self._impulse = TrigEnv(self._trig, table=self._table, dur=dur* 0.1)
        self._noise = Biquad(Noise(self._impulse), freq=2500)
        self._out = Waveguide(self._noise, freq=self._freq, dur=dur, minfreq=0.5, mul=0.4)
        self._out.out()

if __name__ == "__main__":
    #import random
    s = Server().boot()
    s.start()
    a = SimpleWaveguide(freq=[200,330])
    def notes():
        f = random.randrange(80, 408, 25)
        a.freq = [f, f + 20]
        a.dur = random.randrange(1,10,1)
        print(a.freq)
        print(a.dur)
        #a.out()        
    p = Pattern(notes, 3)
    p.play()
    s.gui(locals())

