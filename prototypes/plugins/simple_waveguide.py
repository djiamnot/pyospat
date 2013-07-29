#!/usr/bin/env python
# -*- coding: latin-1 -*-

import random
from pyo import *

class SimpleWaveguide(PyoObject):
    def __init__(self, freq=110, dur=1, deviation=1, mul=0.5, add=1):
        PyoObject.__init__(self)
        self._freq = freq
        self._dur = dur
        freq, dur, deviation, mul, add, lmax = convertArgsToLists(self._freq, self._dur, deviation, mul, add)
        self._trig = Trig()
        self._deviation = Randi(min=0.-deviation[-1], max=deviation[-1], freq=random.uniform(2,4), add=1)
        self._table = CosTable([(0,0),(50,1),(300,0),(8191,0)])
        self._impulse = TrigEnv(self._trig, table=self._table, dur=dur[-1]* 0.1)
        self._noise = Biquad(Noise(self._impulse), freq=2500)
        self._out = Waveguide(self._noise, freq=self._freq, dur=dur[-1], minfreq=0.5, mul=0.4)
        #self._out.out()
        self._base_objs = self._out.getBaseObjects()

    def setPitch(self, f):
        self._freq = f
        self._out.freq =f

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, f):
        self.setPitch(f)

    @property
    def dur(self):
        return self._freq

    @dur.setter
    def dur(self, d):
        self._dur = d
        self._out.dur = d

    def play(self, dur=0, delay=0):
        self._trig.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

if __name__ == "__main__":
    #import random
    s = Server().boot()
    s.start()
    a = SimpleWaveguide(freq=[200,330])
    b = Freeverb(a, size=[.79,.8], damp=.1).out()

    def notes():
        f = random.randrange(80, 408, 25)
        a.freq = [f, f + 20]
        a.dur = random.randrange(1,10,1)
        #print(a._freq)
        #print(a._dur)
        a.play()
    tm = Sine(freq=0.1, mul=.5, add=1.75)
    p = Pattern(notes, tm)
    p.play()
    b.ctrl()
    s.gui(locals())

