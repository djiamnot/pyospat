#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *
import random

class Buzz(PyoObject):
    """
    Buzz opcode based on the csound opcode
    """
    def __init__(self, freq=[100,201], harmonicity = 0.1, dur=5, mul=0.5, add=1):
        """
        
        """
        PyoObject.__init__(self)

        # instance variables
        self._dur = dur
        self._freq = freq
        self._harmonicity = harmonicity
        self._attack = .9
        self._decay = .9
        self._sustain = 1
        self._release = 5

        dur, freq, harmonicity, mul, add, lmax = convertArgsToLists(
            self._dur, 
            self._freq,
            self._harmonicity,
            mul, add
            )
        
        # DSP graph
        self._env = Adsr(attack=self._attack, decay=self._decay, sustain=self._sustain, release=self._release, dur=self._dur, mul=.5).play()
        self._sig = Sine(freq=self._freq, mul=self._env)
        self._a = Sig(self._harmonicity)
        self._sin = Sin(self._sig)
        self._cos = Cos(self._sig)
        self._one_minus = Sig(1) - Pow(self._a, exponent=2)
        self._one_plus = Sig(1) + Pow(self._a, exponent=2)
        self._square = Sqrt(self._one_minus * self._one_plus)
        self._div = self._sin / (self._one_plus - 2*self._a * self._cos)
        self._buzz = (self._div * self._square)
        self._out = Interp(self._buzz[0], self._buzz[1])
        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
        return["dur", "freq", "harmonicity", "mul", "add"]

    @property
    def dur(self):
        return self._dur
    
    @dur.setter
    def dur(self, dur):
        """
        Change duration
        @dur: float (sec.)
        """
        self._dur = dur
        self._env.dur = dur
        self._attack = random.random()*dur/4
        self._env.attack = self._attack
        self._decay = random.random()*dur/4
        self._env.decay = self._decay
        self._sustain = random.random()*dur/4
        self._env.sustain = self._sustain
        self._release = random.random()*dur/4
        self._env.release = self._release

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, freq):
        """
        Frequency
        """
        self._freq = freq
        # if type(self._freq) is "list":
        #     self._sin.freq = self._freq[0]
        # else:
        #     self._sin.freq = self._freq
        self._sig.freq = freq

    @property
    def harmonicity(self):
        return self._harmonicity

    @harmonicity.setter
    def harmonicity(self, x):
        """
        harmonicity
        """
        self._harmonicity = x
        self._a.value = x

    # override some methods
    def play(self, dur=0, delay=0):
        self._env.play(dur, delay)
        #self._wg.play(dur, delay)
        # self._impulse.play(dur, delay)
        # self._noise.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    def stop(self):
        self._env.stop()
        #self._wg.stop()
        return PyoObject.stop()
