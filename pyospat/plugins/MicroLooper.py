#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyo import *

class MicroLooper(PyoObject):
    """
    Loop small portions of samples from audio file. Can move within the length
    of the file, transpose, control beginning/end loop overlap
    """
    def __init__(self, path=None, pitch=1., start=0., freq=[100,200], dur=1.0, mul=0.5, add=1):
        """
        
        """
        PyoObject.__init__(self)

        # instance variables
        self._path = path
        self._pitch = pitch
        self._start = start
        self._dur = dur
        self._freq = freq
        self._xfade = 20 # duration of the loop crossfade
        self._res_len = 10 # duration of the waveguide resonance (sec.)
        self._res_mix = [0.25, 0.5] # strength of the 4 voices
        self._transposition = -5
        self._harm_wet = 1

        path, pitch, start, dur, freq, mul, add, lmax = convertArgsToLists(
            self._path, 
            self._pitch, 
            self._start, 
            self._dur, 
            self._freq,
            mul, add
            )
        
        # DSP graph
        self._table = SndTable(path=self._path)
        self._looper = Looper(self._table, 
                               pitch=pitch, 
                               start=start, 
                               dur=dur, 
                               xfade=self._xfade, 
                               autosmooth=True, 
                               mul=1, 
                               add=0)
        # self._wg = Waveguide (self._looper, 
        #                        freq=freq, 
        #                        dur=self._res_len, 
        #                        minfreq=20, 
        #                        mul=self._res_mix,
        #                        )
        self._wg = Biquad(self._looper, freq=freq, type=0, q=5)
        self._mix1 = Interp(self._wg[0], self._wg[1])
        #self._mix2 = Interp(self._wg[2], self._wg[3])
        #self._mix = Interp(self._mix1, self._mix2)
        # self._out = Mixer(outs=1, chnls=4)
        # self._out.addInput(0, self._wg[0])
        # self._out.addInput(1, self._wg[1])
        # self._out.addInput(2, self._wg[2])
        # self._out.addInput(3, self._wg[3])
        # self._out.setAmp(0, 0, 0.3)
        # self._out.setAmp(1, 0, 0.3)
        # self._out.setAmp(2, 0, 0.3)
        # self._out.setAmp(3, 0, 0.3)
        self._harm = Harmonizer(self._mix1, transpo=self._transposition, winsize=0.05)
        self._out = Interp(self._mix1, self._harm, interp=self._harm_wet)

        self._base_objs = self._out.getBaseObjects()

    def __dir__(self):
            return["path", "pitch", "start", "dur", "freq", "xfade", "res_len", "res_mix", "transposition", "harm_wet", "mul", "add"]

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
        print("Loaded: {0}, length: {1}".format(path, str(self._table.getDur())))

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, pitch):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._pitch = pitch
        self._looper.pitch = pitch

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        """
        Position of the loop start within the table (seconds)
        start: float (seconds)
        """
        table_duration = self._table.getDur()
        dur = self._dur
        
        # if table_duration - start >= dur:
        #     start = table_duration - dur
        # else:
        #     start = start % table_duration
        print("setting MicroLooper.start to {0}".format(start))
        self._start = start
        self._looper.start = start
            
    @property
    def dur(self):
        return self._dur

    @dur.setter
    def dur(self, dur):
        """
        Loop duration
        dur: float(seconds)
        """
        if dur >= self._table.getDur():
            self._dur = self._table.getDur()
            self._looper.dur = self._table.getDur()
        else:
            self._dur = dur
            self._looper.dur = dur
                                 
        print("setting MicroLoope dur to {0}".format(dur))

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
        self._wg.freq = freq

    @property
    def xfade(self):
        return self._xfade

    @xfade.setter
    def xfade(self, x):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._xfade = x
        self._looper.freq = x

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
    def transposition(self):
        return self._transposition

    @transposition.setter
    def transposition(self, x):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._transposition = x
        self._harm.transpo = x

    @property
    def harm_wet(self):
        return self._harm_wet

    @harm_wet.setter
    def harm_wet(self, x):
        """
        Change reading speed
        pitch: float, < 1 = lower, > 1 higher, 1 = original
        """
        self._harm_wet = x
        self._out.interp = x

    # override some methods
    def play(self, dur=0, delay=0):
        self._out.play(dur, delay)
        self._harm.play(dur, delay)
        self._looper.play(dur, delay)
        self._wg.play(dur, delay)
        # self._impulse.play(dur, delay)
        # self._noise.play(dur, delay)
        return PyoObject.play(self, dur, delay)
    
    def out(self, chnl=0, inc=1, dur=0, delay=0):
        return PyoObject.out(self, chnl, inc, dur, delay)

    def stop(self):
        self._out.stop()
        self._harm.stop()
        self._looper.stop()
        self._wg.stop()
        return PyoObject.stop()
