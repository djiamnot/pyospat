#!/usr/bin/env python
# -*- coding: latin-1 -*-

from pyo import *
#from pyospat import logger

#log = logger.start(name="AddSynth")

class AddSynth(PyoObject):
    """
    Additive synthesis.
    
    Additive synthesis created by the addition of four looped sine waves.
    
    Parameters:
    
    Transposition : Transposition, in semitones, of the pitches played on the keyboard.
    Spread : Spreading factor of the sine wave frequencies.
    Feedback : Amount of output signal sent back in the waveform calculation.
    
    _______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    Adapted for pyospat : Michal Seta
    _______________________________________________________________________________________
    """

    import random

    def __init__(self, freq=440, feedback=0.35, mul=0.5, add=1):
        #PyoObject.__init__(self)
        self._freq = freq
        self._feedback = feedback
        self._mul = mul
        self._add = add
        self._fac = []
        self._feedrnd = []
        self._sine1 = []
        self._sine2 = []
        self._sine3 = []
        self._sine4 = []
        self._outs = []
        self._base_objs = []

        freq, feedback, mul, add, lmax = convertArgsToLists(freq, feedback, mul, add)
        
        for i in range(lmax):
            #self._fac.append(Pow(range(1,6), [1,2,3,4], mul=[random.uniform(.995,1.005) for i in range(4)]))
            self._fac.append(Pow(range(1,6), [1,2,3,4], mul=[random.uniform(.995,1.005) for i in range(4)]))
            self._feedrnd.append(Randi(min=.15, max=.25, freq=[random.uniform(.5,2) for i in range(4)]))
            self._sine1.append(SineLoop(freq=wrap(freq,i)*self._fac[0], 
                                        feedback=wrap(feedback,i)*self._feedrnd[0], mul=wrap(mul,i)))
            self._sine2.append(SineLoop(freq=wrap(freq,i)*self._fac[0], 
                                        feedback=wrap(feedback,i)*self._feedrnd[0], mul=wrap(mul,i)))
            self._sine3.append(SineLoop(freq=wrap(freq,i)*self._fac[0], 
                                        feedback=wrap(feedback,i)*self._feedrnd[0], mul=wrap(mul,i)))
            self._sine4.append(SineLoop(freq=wrap(freq, i)*self._fac[0], 
                                        feedback=wrap(feedback,i)*self._feedrnd[0], mul=wrap(mul, i)))
            self._outs.append(Interp(Interp(self._sine1[-1], self._sine2[-1], mul=wrap(mul,i), add=wrap(add,i)), Interp(self._sine3[-1], self._sine4[-1], mul=wrap(mul,i), add=wrap(add,i)), mul=wrap(mul,i), add=wrap(add,i)))
            self._base_objs.extend(self._outs[-1].getBaseObjects())

    def __dir__(self):
        return ["freq", "feedback", "mul" , "add"]

    def setPitch(self, f):
        self._freq = f
        #x, lmax = convertArgsToLists(f)
        [obj.setFreq(f) for i, obj in enumerate(self._sine1)]
        [obj.setFreq(f) for i, obj in enumerate(self._sine2)]
        [obj.setFreq(f) for i, obj in enumerate(self._sine3)]
        [obj.setFreq(f) for i, obj in enumerate(self._sine4)]

    @property
    def freq(self):
        """
        freq property
        @rtype : float
        """
        return self._freq

    @property
    def feedback(self):
        """
        Feedback property
        @rtype : float
        """
        return self._feedback

    @freq.setter
    def freq(self, freq):
        self.setPitch(freq)

    @feedback.setter
    def feedback(self, fb):
        self._feedback = fb

    # def setFreq(self, f):
    #     f, lmax = convertArgsToLists(f)
    #     [obj.setFreq(wrap(f,i)) for i, obj in enumerate(self._base_objs)]


if __name__ == "__main__":
    s = Server().boot()
    a = AddSynth().play().out()
    #m = Mixer()
    s.gui(locals())
