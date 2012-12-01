#!/usr/bin/env python
# encoding: utf-8
"""
3 oscillators FM synthesis class.

"""
import math
import pyo

t = pyo.HarmTable([1,0.1])
class FMsynth(pyo.PyoObject):
    """
    Frequency modulation synthesizer.

    This is a simple FM synth. The code was taken from some pyo project, IIRC, but cannot recall which....
    Modified into a "proper" PyoObject class as per the tutorial on creating a flanger effect.
    """
    def __init__(self, fcar=125.00, ratio1=0.33001, ratio2=2.9993, index1=8, index2=4, mul=1, add=0):
        print("loading FMsynth")
        # Init PyoObject's basic attributes
        pyo.PyoObject.__init__(self)
        
        self._fcar = fcar
        self._ratio1 = ratio1
        self._ratio2 = ratio2
        self._index1 = index1
        self._index2 = index2
        self._fmod = self._fcar * self._ratio1
        self._fmodmod = self.fmod * self._ratio2
        self._amod = self._fmod * self._index1
        self._amodmod = self._fmodmod * self._index2
        

        # I don't understand yet why, but we need to convert all arguments to
        # lists for "list expansion"
        fcar, ratio1, ratio2, index1, index2, mul, add, lmax = \
        pyo.convertArgsToLists(fcar, ratio1, ratio2, index1, index2, mul, add)

        # Init some lists to keep track of created objects
        self._carriers = []
        self._modulators = []
        self._out = []
        # and the special self._base_objs, audio outputs seen byt the outside world
        # .play(), .out(), .stop() and .mix() methods act on this list of objects
        # mul and add attributes are also aplied here
        self._base_objs = []
        
        # construct our objects:
        for i in range(lmax):
            self._carriers.append(pyo.Sine)

        self._modmod = pyo.Sine(freq=wrap(self._fmodmod, i), mul=wrap(mul, i))
        self._mod = pyo.Sine(freq=wrap(self._fmod+self._modmod, i), mul=self._amod)
        self._car = pyo.Osc(t, fcar+self.mod, mul=.2)
        self._eq = pyo.EQ(self.car, freq=fcar, q=0.707, boost=-12)
        self._out = pyo.DCBlock(self.eq).out()
        
        
