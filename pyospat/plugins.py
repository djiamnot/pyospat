#!/usr/bin/env python
# encoding: utf-8
"""
A copy of the Sine class for testing purposes.

"""
#import math
from pyo import *

print("module plugins imported")

class Sine2(PyoObject):
    """
    A simple sine wave oscillator.
    
    Parentclass: PyoObject
    
    Parameters:
    
    freq : float or PyoObject, optional
        Frequency in cycles per second. Defaults to 1000.
    phase : float or PyoObject, optional
        Phase of sampling, expressed as a fraction of a cycle (0 to 1).
        Defaults to 0.
        
    Methods:
    
    setFreq(x) : Replace the `freq` attribute.
    setPhase(x) : Replace the `phase` attribute.
    reset() : Resets the reading pointer to 0.
    
    Attributes:
    
    freq : float or PyoObject, Frequency in cycles per second.
    phase : float or PyoObject, Phase of sampling (0 -> 1).
    
    See also: Sine, Osc, Phasor
    
    Examples:
    
    >>> s = Server().boot()
    >>> s.start()
    >>> sine = Sine2(freq=[400,500], mul=.2).out()
    
    """
    def __init__(self, freq=1000, phase=0, mul=1, add=0):
        PyoObject.__init__(self)
        self._freq = freq
        self._phase = phase
        self._mul = mul
        self._add = add
        freq, phase, mul, add, lmax = convertArgsToLists(freq, phase, mul, add)
        self._base_objs = [Sine_base(wrap(freq,i), wrap(phase,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]
        print("Loaded Sine2 plugin")

    def __dir__(self):
        return ['freq', 'phase', 'mul', 'add']
        
    def setFreq(self, x):
        """
        Replace the `freq` attribute.
        
        Parameters:

        x : float or PyoObject
            new `freq` attribute.
        
        """
        self._freq = x
        x, lmax = convertArgsToLists(x)
        [obj.setFreq(wrap(x,i)) for i, obj in enumerate(self._base_objs)]
        
    def setPhase(self, x):
        """
        Replace the `phase` attribute.
        
        Parameters:

        x : float or PyoObject
            new `phase` attribute.
        
        """
        self._phase = x
        x, lmax = convertArgsToLists(x)
        [obj.setPhase(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def reset(self):
        """
        Resets current phase to 0.

        """
        [obj.reset() for i, obj in enumerate(self._base_objs)]


    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMapFreq(self._freq), SLMapPhase(self._phase), SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)
        
    @property
    def freq(self):
        """float or PyoObject. Frequency in cycles per second.""" 
        return self._freq
    @freq.setter
    def freq(self, x): self.setFreq(x)

    @property
    def phase(self):
        """float or PyoObject. Phase of sampling.""" 
        return self._phase
    @phase.setter
    def phase(self, x): self.setPhase(x)
