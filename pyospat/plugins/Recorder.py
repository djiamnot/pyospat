#!/usr/bin/env python

from pyo import *

class Recorder(PyoObject):
    def __init__(self, inchannel=0, filename="/tmp/test.wav", dur=5.5, chnls=1):
        PyoObject.__init__(self)
        self._inchannel = inchannel
        self._input = Input(chnl=self._inchannel)
        self._filename = filename
        self._dur = dur
        self._chnls = chnls
        inchannel, filename, chnls, dur, lmax = convertArgsToLists(self._inchannel, self._filename, self._chnls, self._dur)
        self._out = Delay(self._input, delay=2.0, feedback=0, mul=0.1)
        self._base_objs = self._out.getBaseObjects()
        
    def __dir__(self):
        return["inchannel", "filename", "mul", "dur"]

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, path):
        """
        path: string - path to file to be recorded
        """
        self._filename = path

    @property
    def dur(self):
        return self._dur

    @dur.setter
    def dur(self, s):
        """
        path: float - duration of recording in seconds
        """
        self._dur = s

    @property
    def inchannel(self):
        return self._inchannel

    @inchannel.setter
    def inchannel(self, i):
        """
        i: int - input channel to record from
        """
        self._inchannel = int(i)
        self._input = Input(chnl=self._inchannel)

    def play(self):
        #self._input = Input(chnl=self._inchannel)
        _recorder = Record(self._input, self._filename, chnls=self._chnls)
        doit = Clean_objects(self._dur, _recorder)
        doit.start()
        print("Recording ch: ")
        print(self._inchannel)
        #return PyoObject.play(self, dur, delay)

if __name__ == "__main__":
    s = Server().boot()
    s.start()
    r = Recorder(inchannel=0, filename="/tmp/test.wav")
    r.play()
