#!/usr/bin/env python
# -*- coding: latin-1 -*-

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
    def __init__(self, freq=110, dur=1, deviation=1, mul=0.5, add=1):
        PyoObject.__init__(self)
        self._freq = freq
        self._mul = mul
        self._add = add
        self._dur = dur
        self._deviation = Randi(min=0.-deviation, max=deviation, freq=random.uniform(2,4), add=1)
        self._trig = []
        self._deviations = []
        self._tables = []
        self._impulses = []
        self._noises = []
        self._waves = []
        self._outs = []
        self._base_objs = []
        
        freq, dur, mul, add, lmax = convertArgsToLists(freq, dur, mul, add)
        
        for i in range (lmax):
            self._freq = wrap(freq, i)
            self._trig.append(Trig().play())
            # self._deviations.append(Randi(
            #         min=0.-wrap(deviation, i), 
            #         max=wrap(deviation, i), 
            #         freq=random.uniform(2,4) , 
            #         add=1))
            self._tables.append(CosTable([(0,0),(50,1),(300,0),(8191,0)]))
            self._impulses.append((TrigEnv(wrap(self._trig, 1), table=wrap(self._tables, 1), dur=wrap(dur,i )* 0.1)))
            self._noises.append(Biquad(Noise(wrap(self._impulses, 1)), freq=2500))
            self._outs.append(Waveguide(
                    wrap(self._noises, i), 
                    #freq=wrap(freq,i)*wrap(deviation,i),
                    freq = self._freq * deviation,
                    #freq = self._freq,
                    #dur=wrap(dur,i), 
                    dur = dur,
                    minfreq=.5, 
                    mul=wrap(mul,i)))
            self._base_objs.extend(self._outs[-1].getBaseObjects())

    def __dir__(self):
        return ["freq", "dur", "deviation", "mul", "add"]
    
    def setPitch(self, freq):
        self._freq = freq
        x, lmax = convertArgsToLists(freq)
        [obj.setFreq(wrap(x,1)) for i, obj in enumerate(self._base_objs)]

    def setDur(self, dur):
        self._dur = dur
        x, lmax = convertArgsToLists(dur)
        [obj.setFreq(wrap(x,1)) for i, obj in enumerate(self._base_objs)]

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

    @property
    def deviation(self):
        """
        Get deviation property
        @rtype : float
        """
        return self._deviation

    @freq.setter
    def freq(self, freq):
        self.setPitch(freq)

    @dur.setter
    def dur(self, dur):
        self._dur = dur

    @deviation.setter
    def deviation(self, deviation):
        self._deviation = deviation

    # TODO: add setters for mul, add, dur, deviation


    # override some methods
    def play(self, dur=1, delay=0):
        #print("running with: frequency %d" % (self._freq))
        #self._envs.play()
        dur, delay, lmax = convertArgsToLists(dur, delay)
        [obj.play(wrap(dur,i),wrap(delay,i)) for i, obj in enumerate(self._trig)]
        self._base_objs = [obj.play(wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        return self

    def stop(self):
        [obj.stop() for obj in self._trig]
        [obj.stop() for obj in self._base_objs]

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        dur, delay, lmax = convertArgsToLists(dur, delay)
        [obj.play(wrap(dur,1), wrap(delay,0)) for obj in self._trig]
        if type(chnl) == ListType:
            self._base_objs = [obj.out(wrap(chnl,i), wrap(dur,i), wrap(delay, i)) for i, obj in enumerate(self._base_objs)]
        else:
            if  chnl < 0:
                self._base_objs = [obj.out(i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(random.sample(self._base_objs, len(self._base_objs)))]
            else:
                self._base_objs = [obj.out(chnl+i*inc, wrap(dur,i), wrap(delay,i)) for i, obj in enumerate(self._base_objs)]
        return self

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(20., 10000., "log", "freq", self._freq),
                          SLMap(0.001, 20., "lin", "deviation", self._deviation),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

if __name__ == "__main__":
    import random
    s = Server().boot()
    s.start()
    a = PluckedString(freq=[220,230], dur=5).out()
    def notes():
        f = random.randrange(80, 408, 25)
        a.freq = [f, f + 20]
        a.dur = random.randrange(1,10,1)
        print(a.freq)
        print(a.dur)
        a.out()
    p = Pattern(notes, 3)
    p.play()
    s.gui(locals())
