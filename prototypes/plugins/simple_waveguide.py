#!/usr/bin/env python
# -*- coding: latin-1 -*-

import random
from pyo import *

class SimpleWaveguide(PyoObject):
    def __init__(self, freq=110, dur=1, deviation=1, mul=0.5, add=1):
        PyoObject.__init__(self)
        self._freq = freq
        self._dur = dur
        
        freq, dur, mul, add, lmax = convertArgsToLists(freq, self._dur, mul, add)
        
        self._trig = []
        self._impulse = []
        self._noise = []
        self._waveguide = []
        self._base_objs = []
        for i in range(lmax):
            self._trig.append(Trig())
            # self._trig = Trig()
            self._deviation = Randi(min=0.-deviation, max=deviation, freq=random.uniform(2,4), add=1)
            self._table = CosTable([(0,0),(50,1),(300,0),(8191,0)])
            self._impulse.append(TrigEnv(self._trig[-1], table=self._table, dur=self._dur* 0.1))
            self._noise.append(Biquad(Noise(wrap(self._impulse, 1)), freq=2500))
            self._waveguide.append(Waveguide(wrap(self._noise, 1), freq=self._freq, dur=self._dur, minfreq=0.5, mul=0.4))
            self._base_objs.extend(self._waveguide[-1].getBaseObjects())

    def __dir__(self):
        return ["freq", "dur", "mul", "add"]
        
    def setPitch(self, x):
        self._freq = x
        freq, lmax = convertArgsToLists(x)
        #self._waveguide.freq = freq
        [obj.setFreq(wrap(freq,1)) for i, obj in enumerate(self._base_objs)]

    def setDur(self, dur):
        self._dur = dur

    @property
    def freq(self):
        """
        Get freq property
        @rtype : float
        """
        return self._freq

    @property
    def dur(self):
        """
        Get dur property
        @rtype : float
        """
        return self._dur

    @freq.setter
    def freq(self, freq):
        self.setPitch(freq)

    @dur.setter
    def dur(self, dur):
        self._dur = dur

    def play(self, dur=0, delay=0):
        dur, delay, lmax = convertArgsToLists(dur, delay)
        # self._trig.play()
        # self._impulse.play()
        # self._noise.play()
        # return PyoObject.play(self)

        #[obj.play(wrap(dur,i),wrap(delay,i)) for i, obj in enumerate(self._trig)]
        #self._trig.play()
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._trig)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._impulse)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._noise)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._waveguide)]
        self._base_objs = [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        return self
    
    def stop(self):
        self._trig.stop()
        [obj.stop(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._impulse)]
        [obj.stop(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._noise)]
        [obj.stop(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._waveguide)]
        [obj.stop(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        return self

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        dur, delay, lmax = convertArgsToLists(dur, delay)
        #[obj.play(wrap(dur,1), wrap(delay,0)) for obj in self._trig]
        #self._trig.play()
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._trig)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._impulse)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._noise)]
        [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._waveguide)]
        #self._base_objs = [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        if type(chnl) == ListType:
            self._base_objs = [obj.out(wrap(chnl,i), wrap(dur,i), wrap(delay, i)) for i, obj in enumerate(self._base_objs)]
        else:
            if  chnl < 0:
                self._base_objs = [obj.out(i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(random.sample(self._base_objs, len(self._base_objs)))]
            else:
                self._base_objs = [obj.out(chnl+i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        return self

    # def out(self, chnl=0, inc=1, dur=0, delay=0):
    #     self._trig.play()
    #     self._impulse.play()
    #     self._noise.play()
    #     #return PyoObject.out(self)
    #     dur, delay, lmax = convertArgsToLists(dur, delay)
    #     [obj.play(wrap(dur,1), wrap(delay,0)) for obj in self._trig]
    #     if type(chnl) == ListType:
    #         self._base_objs = [obj.out(wrap(chnl,i), wrap(dur,i), wrap(delay, i)) for i, obj in enumerate(self._base_objs)]
    #     else:
    #         if  chnl < 0:
    #             self._base_objs = [obj.out(i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(random.sample(self._base_objs, len(self._base_objs)))]
    #         else:
    #             self._base_objs = [obj.out(chnl+i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
    #     return self


if __name__ == "__main__":
    #import random
    s = Server().boot()
    s.start()
    a = SimpleWaveguide(freq=[200,330, 440], dur=5).out(chnl=[0,1])
    def notes():
        f = random.randrange(80, 408, 25)
        a.freq = [f, f + 20]
        #a.dur = random.randrange(1,10,1)
        print(a.freq)
        for w in a._waveguide:
            print(w.freq)
        #print(a.dur)
        a.play()
    p = Pattern(notes, 3)
    p.play()
    s.gui(locals())
