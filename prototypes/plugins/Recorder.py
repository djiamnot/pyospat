#!/usr/bin/env python

from pyo import *

class Recorder(PyoObject):
    def __init__(self, inchannel=0, filename="/tmp/test.wav", dur=5.5, chnls=1):
        PyoObject.__init__(self)
        self._inchannel = inchannel
        self._input = Input(self._inchannel)
        self._filename = filename
        self._dur = dur
        self._chnls = chnls
        inchannel, filename, chnls, dur, lmax = convertArgsToLists(self._inchannel, self._filename, self._chnls, self._dur)
        
        #self._base_objs = self._out.getBaseObjects()
        
    def __dir__(self):
        return["inchannel", "filename", "dur", "chnls"]
    @property
    def filename(self):
        return self._filename
    @filename.setter
    def path(self, path):
        """
        path: string - path to file to be recorded
        """
        self._path = path

    @property
    def input(self):
        return self._inchannel

    @input.setter
    def input(self, i):
        """
        i: int - input channel to record from
        """
        self._inchannel = i

    @property
    def chnls(self):
        return self._chnls

    @chnls.setter
    def chnls(self, ch):
        """
        i: int - number of channels to record 
        """
        self._chnls = ch

    def play(self):
        _recorder = Record(self._input, self._filename)
        doit = Clean_objects(self._dur, _recorder)
        doit.start()
        #return PyoObject.play(self, dur, delay)

if __name__ == "__main__":
    s = Server().boot()
    s.start()
    r = Recorder(inchannel=0, filename="/tmp/test.wav")
    r.play()
