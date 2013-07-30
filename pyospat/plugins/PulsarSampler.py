#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *

class PulsarSampler(PyoObject):
    """
    A pulsar synth reading from a table recorded live. 
    """
    def __init__(self, freq=80, length=1, lfo=[.1,.15], mul=0.5, add=1):
        PyoObject.__init__(self)
        self._dur = dur
        self._freq = freq
        self._length = length
        freq, length, lfo, mul, add, lmax = convertArgsToLists(self._freq, self._length, lfo, mul, add)

        self._input = Input(0)
        self._han = HannTable()
        self._lfo = Sine([.1,.15], mul=.2, add=.5)
        self._table = NewTable(length=10, chnls=1)
        self._rec = TableRec(self._input, table=self._table, fadetime=0.01)
        self._out = Pulsar(table=self._table, env=self._han, freq=self._freq, frac=self._lfo, mul=0.12)
        #self._out = TrigEnv(self._rec['trig'], table=self._table, dur=self._dur)

        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
        return["freq", "length", "lfo", "mul", "add"]

    def setLfo(self, f):
        self._freq = f
        self._lfo.freq =f

    @property
    def lfo(self):
        return self._freq

    @lfo.setter
    def lfo(self, f):
        self.setPitch(f)

    def setPitch(self, f):
        self._freq = f
        self._out.freq = f

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, f):
        self.setPitch(f)

    @property
    def length(self):
        return self._length

    @dur.setter
    def length(self, d):
        self._length = d
        self._table.dur = d

    def play(self, dur=0, delay=0):
        self._rec.play(dur,delay)
        self._out.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

if __name__ == "__main__":
    import random
    s = Server().boot()
    #s.setInOutDevice(5)
    s.start()
    a = PulsarSampler()
    b = Freeverb(a, size=[.79,.8], damp=.1).out()
    trigger = 10

    def freqs():
        f = random.randrange(20, 1000, 15)
        a.freq = [f, f * random.random(), f*random.random(), f ]
        #a.dur = d*0.01
        print(a._freq)
        global trigger
        trigger = random.randrange(10, 20, 1)
        a.play()

    def lfos():
        lfo = random.randrange(1, 100, 15)
        a.lfo = [lfo * random.random(), lfo * random.random(), lfo * random.random(), lfo * random.random()]
        print(a.lfo)

    p = Pattern(freqs, trigger)
    p.play()
    pl = Pattern(lfos, 5)
    pl.play()
    b.ctrl()
    s.gui(locals())

