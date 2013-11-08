#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *

class Granny(PyoObject):
    """
    Granulator based on Granule class
    """
    def __init__(self, path=None, mul=.2, add=0):
        PyoObject.__init__(self)
        self._path = path
        self._end = 0
        self._pitch_min = 0.99
        self._pitch_max = 1.01
        self._density = 8
        self._basedur = 0.1

        path, mul, add, lmax = convertArgsToLists(self._path, mul, add)

        self._table = SndTable(path=self._path)
        self._env = HannTable()
        self._pos = Randi(min=0, max=1, freq=0.25, mul=self._end)
        #self._density = Randi(min=10, max=30, freq=.1)
        self._pitch = Randi(min=0.99, max=1.01, freq=100)
        self._out = Granulator(self._table, self._env, pitch=self._pitch, 
                               pos=self._pos, dur=.2, grains=self._density, 
                               basedur=self._basedur, mul=.1, add=0)

        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
        return ["path", "pitch_min", "pitch_max", "density", "basedur", "mul", "add"]

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        """
        path: string
        """
        self._path = path
        self._table.path = path
        self._end = self._table.getSize()
        self._pos.mul = self._end

    @property
    def pitch_min(self):
        return self._pitch_min
    
    @pitch_min.setter
    def pitch_min(self, pitch):
        """
        pitch: float
        """
        self._pitch_min = pitch
        self._pitch.min = self._pitch_min = pitch

    @property
    def pitch_max(self):
        return self._pitch_max
    
    @pitch_max.setter
    def pitch_max(self, pitch):
        """
        pitch: float
        """
        self._pitch_max = pitch
        self._pitch.max = self._pitch_max

    @property
    def density(self):
        return self._density
    
    @density.setter
    def density(self, d):
        """
        d: float
        """
        self._density = d
        self._out.grains = self._density

    @property
    def basedur(self):
        return self._basedur
    
    @basedur.setter
    def basedur(self, d):
        """
        d: float
        """
        self._basedur = d
        self._out.basedur = self._basedur

    # override some methods
    def play(self, dur=0, delay=0):
        self._out.play(dur, delay)
        self._pos.play(dur, delay)
        self._pitch.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    def stop(self):
        self._out.stop()
        self._pos.stop()
        self._pitch.stop()
        return PyoObject.stop()
