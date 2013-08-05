#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *
#from pyospat import logger

#log = logger.start(name="PluckedString")

class PluckedString(PyoObject):
    """
    Simple plucked string synthesis model.
    
    A Resonator network is feed with a burst of noise to simulate the behavior of a
    plucked string.
    
    Parameters:

        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        Duration : Length, in seconds, of the string resonance.
        Chorus depth : Depth of the frequency deviation between the left and right channels.
    
    _______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    Adapted to pyospat: Michal Seta
    _______________________________________________________________________________________
    """
    def __init__(self, freq=[210, 250, 280, 300], dur=1, deviation=1, mul=0.5, add=0):
        PyoObject.__init__(self)
        self._freq = freq
        self._dur = dur
        freq, dur, deviation, mul, add, lmax = convertArgsToLists(self._freq, self._dur, deviation, mul, add)
        self._trig = Trig()
        self._deviation = Randi(min=0.-deviation[-1], max=deviation[-1], freq=random.uniform(2,4), add=1)
        self._table = CosTable([(0,0),(50,1),(300,0),(8191,0)])
        self._impulse = TrigEnv(self._trig, table=self._table, dur=dur[-1]* 0.1)
        self._noise = Biquad(Noise(self._impulse), freq=2500)
        self._pluck = Waveguide(self._noise, freq=self._freq, dur=dur[-1], minfreq=20, mul=0.5)
        # TODO: fix this 
        self._out = Mixer(outs=1, chnls=4)
        self._out.addInput(0, self._pluck[0])
        self._out.addInput(1, self._pluck[1])
        self._out.addInput(2, self._pluck[2])
        self._out.addInput(3, self._pluck[3])
        self._out.setAmp(0, 0, 0.1)
        self._out.setAmp(1, 0, 0.1)
        self._out.setAmp(2, 0, 0.1)
        self._out.setAmp(3, 0, 0.1)
        #self._out.out()
        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
        return ["freq", "dur", "deviation", "mul", "add"]

    def setPitch(self, f):
        self._freq = f
        self._pluck.freq =f

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, f):
        self.setPitch(f)
        print("Current pitch: {0}".format(self._freq))
        print("Pluck has {0} streams of audio".format(len(self._pluck)))

    @property
    def dur(self):
        return self._freq

    @dur.setter
    def dur(self, d):
        self._dur = d
        self._pluck.dur = d

    @property
    def deviation(self):
        """
        Get deviation property
        @rtype : float
        """
        return self._deviation

    @deviation.setter
    def deviation(self, deviation):
        self._deviation = deviation

    # TODO: add setters for deviation
    # override some methods
    def play(self, dur=0, delay=0):
        self._trig.play(dur, delay)
        # self._impulse.play(dur, delay)
        # self._noise.play(dur, delay)
        self._pluck.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    def stop(self):
        self._trig.stop()
        self._impulse.stop()
        self._noise.stop()
        return PyoObject.stop()


    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(18.01, 16000., "log", "freq", self._freq),
                          SLMap(0.001, 20., "lin", "duration", self._dur),
                          SLMap(-5., 5., "lin", "deviation", self._deviation),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

if __name__ == "__main__":
    import random
    s = Server().boot()
    s.start()
    a = PluckedString(freq=[200,330]).out()
    def notes():
        f = random.randrange(80, 408, 25)
        a.freq = [f, f + 20]
        a.dur = random.randrange(1,10,1)
        print(a.freq)
        print(a.dur)
        a.play()
        a.out()
        
    p = Pattern(notes, 3)
    p.play()
    a.ctrl()
    s.gui(locals())
