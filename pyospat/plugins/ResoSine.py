#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *

class ResoSine(PyoObject):
    """
    Blit generator through a waveguide
    """
    def __init__(self, freq=[100,200,300,400], dur=1.0, mul=0.5, add=1):
        """
        
        """
        PyoObject.__init__(self)

        # instance variables
        self._dur = dur
        self._freq = freq
        self._harms = 1
        self._res_len = 10 # duration of the waveguide resonance (sec.)
        self._res_mix = [0.25, 0.5, 0.7, 0.2] # strength of the 4 voices

        dur, freq, mul, add, lmax = convertArgsToLists(
            self._dur, 
            self._freq,
            mul, add
            )
        
        # DSP graph
        self._env = Adsr(attack=.001, decay=.02, sustain=.05, release=.1, dur=.2, mul=.5)
        self._sin = Blit(freq=self._freq, harms=self._harms, mul=self._env)
        self._wg = Waveguide (self._sin, 
                               freq=freq, 
                               dur=self._res_len, 
                               minfreq=20, 
                               mul=self._res_mix,
                               )
        self._mix1 = Interp(self._wg[0], self._wg[1])
        self._mix2 = Interp(self._wg[2], self._wg[3])
        self._out = Interp(self._mix1, self._mix2)

        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
        return["dur", "freq", "res_len", "res_mix", "harms", "mul", "add"]

    @property
    def dur(self):
        return self._dur

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, freq):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._freq = freq
        if type(self._freq) is "list":
            self._sin.freq = self._freq[0]
        else:
            self._sin.freq = self._freq
        self._wg.freq = freq

    @property
    def res_len(self):
        return self._res_len

    @res_len.setter
    def res_len(self, x):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._res_len = x
        self._wg.dur = x

    @property
    def res_mix(self):
        return self._res_mix

    @res_mix.setter
    def res_mix(self, x):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._res_mix = x
        self._wg.mul = x

    @property
    def harms(self):
        return self._harms

    @harms.setter
    def harms(self, x):
        """
        set number of harmonics
        """
        self._harms = x
        self._sin.harms = x

    # override some methods
    def play(self, dur=0, delay=0):
        self._env.play(dur, delay)
        # self._impulse.play(dur, delay)
        # self._noise.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    def stop(self):
        self._env.stop()
        return PyoObject.stop()
