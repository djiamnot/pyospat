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

"""
Import of the zyne synth audio plugins.
This is being simplified.

"""

class CHO(object):
    def __init__(self):
        self._freq = 200
        self._env = Linseg([(0,0), (.01,1), (.19,1), (.2,0)]).stop()
        self._sin = Sine(freq=self._freq, mul=0)
        self.out = Pan(self._sin*self._env, pan=.5).out()

    def go(self, fq, mul):
        self._sin.setFreq(fq)
        self._sin.setMul(mul)
        self._env.play()

    def setFreq(self, freq):
        """
        set frequency attribute.

        Parameter:

        freq : float - new frequency
        """
        self._freq = freq

    @property
    def freq(self):
        """
        Set freq property
        @rtype : float
        """
        return self._freq

    @freq.setter
    def freq(self, freq):
        """
        set new frequency
        """
        self.setFreq(freq)

    @property
    def playing(self):
        """
        Playing active or stopped?
        @rtype: boolean
        """
        return self._env
    @playing.setter
    def playing(self, freq=800, mul=0.5):
        """
        Make it play
        """
        self.go(freq, mul)

    
    

class BaseSynth:
    def __init__(self):
            self.amp = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=2, mul=.5)
            self.pitch = 220.00
            self.trig = Trig().play()

        # elif vars.vars["VIRTUAL"]:
        #     self._virtualpit = Sig([0.0]*vars.vars["POLY"])
        #     self._trigamp = Sig([0.0]*vars.vars["POLY"])
        #     if with_transpo:
        #         self._transpo = Sig(value=0)

        #     else:

        #     self._lfo_amp = LFOSynth(.5, self._trigamp, self._midi_metro)

        #                            mul=self._rawamp, add=self._lfo_amp.sig())
        #     self.trig = Thresh(self._trigamp)
        # else:
        #     if with_transpo:
        #         self._note = Notein(poly=vars.vars["POLY"], scale=0)
        #         self._transpo = Sig(value=0)

        #     else:
        #         self._note = Notein(poly=vars.vars["POLY"], scale=scaling)

        #     self._trigamp = self._note["velocity"]
        #     self._lfo_amp = LFOSynth(.5, self._trigamp, self._midi_metro)

        #                            mul=self._rawamp, add=self._lfo_amp.sig())
        #     self.trig = Thresh(self._trigamp)
        
        # self._panner = Panner(self, self._trigamp, self._midi_metro)
        # self.panL = self._panner.amp_L
        # self.panR = self._panner.amp_R
    
        # self._params = [self._lfo_amp, None, None, None, self._panner]
        # for i, conf in enumerate(config):
        #     i1 = i + 1
        #     if conf[0] != "Transposition":
        #         self._params[i1] = Param(self, i1, conf, self._trigamp, self._midi_metro)
        #     else:
        #         self._params[i1] = ParamTranspo(self, self._midi_metro)

class FmSynth(BaseSynth):
    """
    Simple frequency modulation synthesis.
    
    With frequency modulation, the timbre of a simple waveform is changed by 
    frequency modulating it with a modulating frequency that is also in the audio
    range, resulting in a more complex waveform and a different-sounding tone.

    Parameters:

        FM Ratio : Ratio between carrier frequency and modulation frequency.
        FM Index : Represents the number of sidebands on each side of the carrier frequency.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    ________________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ________________________________________________________________________________________
    """
    def __init__(self):
        BaseSynth.__init__(self)
        self.p1 = 0.2
        self.p2 = 0.1
        self.p3 = 530
        self.indexLine = self.amp * 0.2
        self.indexrnd = Randi(min=.95, max=1.05, freq=[random.uniform(.5,2) for i in range(4)])
        self.norm_amp = self.amp * 0.1
        self.fm1 = FM(carrier=self.pitch, ratio=self.p1, index=self.indexLine*self.indexrnd[0], mul=self.amp)
        self.fm2 = FM(carrier=self.pitch*.997, ratio=self.p1, index=self.indexLine*self.indexrnd[1], mul=self.amp)
        self.fm3 = FM(carrier=self.pitch*.995, ratio=self.p1, index=self.indexLine*self.indexrnd[2], mul=self.amp)
        self.fm4 = FM(carrier=self.pitch*1.002, ratio=self.p1, index=self.indexLine*self.indexrnd[3], mul=self.amp)
        self.filt1 = Biquadx(self.fm1+self.fm3, freq=self.p3, q=1, type=0, stages=2).mix()
        self.filt2 = Biquadx(self.fm2+self.fm4, freq=self.p3, q=1, type=0, stages=2).mix()
        self.out = Mix([self.filt1, self.filt2], voices=2)

class AddSynth(BaseSynth):
    """
    Additive synthesis.
    
    Additive synthesis created by the addition of four looped sine waves.

    Parameters:

        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        Spread : Spreading factor of the sine wave frequencies.
        Feedback : Amount of output signal sent back in the waveform calculation.
    
    _______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.fac = Pow(range(1,6), self.p2, mul=[random.uniform(.995,1.005) for i in range(4)])
        self.feedrnd = Randi(min=.15, max=.25, freq=[random.uniform(.5,2) for i in range(4)])
        self.norm_amp = self.amp * 0.1
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.sine1 = SineLoop(freq=self.pitch*self.fac[0], feedback=self.p3*self.feedrnd[0], mul=self.leftamp).mix()
        self.sine2 = SineLoop(freq=self.pitch*self.fac[1], feedback=self.p3*self.feedrnd[1], mul=self.rightamp).mix()
        self.sine3 = SineLoop(freq=self.pitch*self.fac[2], feedback=self.p3*self.feedrnd[2], mul=self.leftamp).mix()
        self.sine4 = SineLoop(freq=self.pitch*self.fac[3], feedback=self.p3*self.feedrnd[3], mul=self.rightamp).mix()
        self.out = Mix([self.sine1, self.sine2, self.sine3, self.sine4], voices=2)

class WindSynth(BaseSynth):
    """
    Wind synthesis.
    
    Simulation of the whistling of the wind with a white noise filtered by four 
    bandpass filters.

    Parameters:

        Rand frequency : Speed of filter's frequency variations.
        Rand depth : Depth of filter's frequency variations.
        Filter Q : Inverse of the filter's bandwidth. Amplitude of the whistling.
    
    ______________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ______________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.clpit = Clip(self.pitch, min=40, max=15000)
        self.norm_amp = self.p3 * .2
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.noise = Noise(mul=self.amp*self.norm_amp)
        self.dev = Randi(min=0.-self.p2, max=self.p2, freq=self.p1*[random.uniform(.75,1.25) for i in range(4)], add=1)
        self.filt1 = Biquadx(self.noise, freq=self.clpit*self.dev[0], q=self.p3, type=2, stages=2, mul=self.leftamp).mix()
        self.filt2 = Biquadx(self.noise, freq=self.clpit*self.dev[1], q=self.p3, type=2, stages=2, mul=self.rightamp).mix()
        self.filt3 = Biquadx(self.noise, freq=self.clpit*self.dev[2], q=self.p3, type=2, stages=2, mul=self.leftamp).mix()
        self.filt4 = Biquadx(self.noise, freq=self.clpit*self.dev[3], q=self.p3, type=2, stages=2, mul=self.rightamp).mix()
        self.out = Mix([self.filt1, self.filt2, self.filt3, self.filt4], voices=2)

class SquareMod(BaseSynth):
    """
    Square waveform modulation.
    
    A square waveform, with control over the number of harmonics, which is modulated 
    in amplitude by itself.

    Parameters:

        Harmonics : Number of harmonics of the waveform.
        LFO frequency : Speed of the LFO modulating the amplitude.
        LFO Amplitude : Depth of the LFO modulating the amplitude.
    
    _______________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.table = SquareTable(order=10, size=2048)
        self.change = Change(self.p1)
        self.trigChange = TrigFunc(self.change, function=self.changeOrder)
        self.lfo = Osc(table=self.table, freq=self.p2, mul=self.p3*.1, add=.1)
        self.norm_amp = self.amp * self.lfo
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.osc1 = Osc(table=self.table, freq=self.pitch, mul=self.leftamp).mix()
        self.osc2 = Osc(table=self.table, freq=self.pitch*.994, mul=self.rightamp).mix()
        self.osc3 = Osc(table=self.table, freq=self.pitch*.998, mul=self.leftamp).mix()
        self.osc4 = Osc(table=self.table, freq=self.pitch*1.003, mul=self.rightamp).mix()
        self.out = Mix([self.osc1, self.osc2, self.osc3, self.osc4], voices=2)
    
    def changeOrder(self):
        order = int(self.p1.get())
        self.table.order = order

class SawMod(BaseSynth):
    """
    Sawtooth waveform modulation.
    
    A sawtooth waveform, with control over the number of harmonics, which is 
    modulated in amplitude by itself.

    Parameters:

        Harmonics : Number of harmonics of the waveform.
        LFO frequency : Speed of the LFO modulating the amplitude.
        LFO Amplitude : Depth of the LFO modulating the amplitude.
    
    ________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.table = SawTable(order=10, size=2048)
        self.change = Change(self.p1)
        self.trigChange = TrigFunc(self.change, function=self.changeOrder)
        self.lfo = Osc(table=self.table, freq=self.p2, mul=self.p3*.1, add=.1)
        self.norm_amp = self.amp * self.lfo
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.osc1 = Osc(table=self.table, freq=self.pitch, mul=self.leftamp).mix()
        self.osc2 = Osc(table=self.table, freq=self.pitch*.995, mul=self.rightamp).mix()
        self.osc3 = Osc(table=self.table, freq=self.pitch*.998, mul=self.leftamp).mix()
        self.osc4 = Osc(table=self.table, freq=self.pitch*1.004, mul=self.rightamp).mix()
        self.out = Mix([self.osc1, self.osc2, self.osc3, self.osc4], voices=2)
    
    def changeOrder(self):
        order = int(self.p1.get())
        self.table.order = order

class PulsarSynth(BaseSynth):
    """
    Pulsar synthesis.
    
    Pulsar synthesis is a method of electronic music synthesis based on the generation of 
    trains of sonic particles. Pulsar synthesis can produce either rhythms or tones as it 
    criss‐crosses perceptual time spans.
    
    Parameters:

        Harmonics : Number of harmonics of the waveform table.
        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        LFO Frequency : Speed of the LFO modulating the ratio waveform / silence.
    
    ______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    ______________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.table = SawTable(order=10, size=2048)
        self.change = Change(self.p1)
        self.trigChange = TrigFunc(self.change, function=self.changeOrder)
        self.env = HannTable()
        self.lfo = Sine(freq=self.p3, mul=.25, add=.7)
        self.norm_amp = self.amp * 0.2
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.pulse1 = Pulsar(table=self.table, env=self.env, freq=self.pitch, frac=self.lfo, mul=self.leftamp).mix()
        self.pulse2 = Pulsar(table=self.table, env=self.env, freq=self.pitch*.998, frac=self.lfo, mul=self.rightamp).mix()
        self.pulse3 = Pulsar(table=self.table, env=self.env, freq=self.pitch*.997, frac=self.lfo, mul=self.leftamp).mix()
        self.pulse4 = Pulsar(table=self.table, env=self.env, freq=self.pitch*1.002, frac=self.lfo, mul=self.rightamp).mix()
        self.out = Mix([self.pulse1, self.pulse2, self.pulse3, self.pulse4], voices=2)
    
    def changeOrder(self):
        order = int(self.p1.get())
        self.table.order = order

class Ross(BaseSynth):
    """
    Rossler attractor.
    
    The Rossler attractor is a system of three non-linear ordinary differential equations. 
    These differential equations define a continuous-time dynamical system that exhibits 
    chaotic dynamics associated with the fractal properties of the attractor.
    
    Parameters:

        Chaos : Intensity of the chaotic behavior.
        Chorus depth : Depth of the deviation between the left and right channels.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    _____________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _____________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.rosspit = Clip(self.pitch / 5000. + 0.25, min=0., max=1.)
        self.deviation = Randi(min=0.-self.p2, max=self.p2, freq=[random.uniform(2,4) for i in range(2)], add=1)
        self.norm_amp = self.amp * 0.3
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.ross1 = Rossler(pitch=self.rosspit*self.deviation[0], chaos=self.p1, stereo=True, mul=self.leftamp)
        self.ross2 = Rossler(pitch=self.rosspit*self.deviation[1], chaos=self.p1, stereo=True, mul=self.rightamp)
        self.eq1 = EQ(self.ross1, freq=260, q=25, boost=-12)
        self.eq2 = EQ(self.ross2, freq=260, q=25, boost=-12)
        self.filt1 = Biquad(self.eq1, freq=self.p3).mix()
        self.filt2 = Biquad(self.eq2, freq=self.p3).mix()
        self.out = Mix([self.filt1, self.filt2], voices=2)

class Wave(BaseSynth):
    """
    Bandlimited waveform synthesis.
    
    Simple waveform synthesis with different waveform shapes. The number of harmonic of the 
    waveforms is limited depending on the frequency played on the keyboard and the sampling 
    rate to avoid aliasing. Waveform shapes are:
    0 = Ramp (saw up), 1 = Sawtooth, 2 = Square, 3 = Triangle
    4 = Pulse, 5 = Bipolar pulse, 6 = Sample and Hold, 7 = Modulated sine
    
    Parameters:

        Waveform : Waveform shape.
        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        Sharpness : The sharpness factor allows more or less harmonics in the waveform.
    
    _____________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _____________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.change = Change(self.p1)
        self.trigChange = TrigFunc(self.change, function=self.changeWave)
        self.norm_amp = self.amp * 0.15
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.wav1 = LFO(freq=self.pitch, sharp=self.p3, type=0, mul=self.leftamp)
        self.wav2 = LFO(freq=self.pitch*.997, sharp=self.p3, type=0, mul=self.rightamp)
        self.wav3 = LFO(freq=self.pitch*1.002, sharp=self.p3, type=0, mul=self.leftamp)
        self.wav4 = LFO(freq=self.pitch*1.0045, sharp=self.p3, type=0, mul=self.rightamp)
        self.out = Mix([self.wav1.mix(), self.wav2.mix(), self.wav3.mix(), self.wav4.mix()], voices=2)
    
    def changeWave(self):
        typ = int(self.p1.get())
        self.wav1.type = typ
        self.wav2.type = typ
        self.wav3.type = typ
        self.wav4.type = typ

class PluckedString(BaseSynth):
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
    _______________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.deviation = Randi(min=0.-self.p3, max=self.p3, freq=[random.uniform(2,4) for i in range(2)], add=1)
        self.table = CosTable([(0,0),(50,1),(300,0),(8191,0)])
        self.impulse = TrigEnv(self.trig, table=self.table, dur=.1)
        self.noise = Biquad(Noise(self.impulse), freq=2500)
        self.leftamp = self.amp*self.panL
        self.rightamp = self.amp*self.panR
        self.wave1 = Waveguide(self.noise, freq=self.pitch*self.deviation[0], dur=self.p2, minfreq=.5, mul=self.leftamp).mix()
        self.wave2 = Waveguide(self.noise, freq=self.pitch*self.deviation[1], dur=self.p2, minfreq=.5, mul=self.rightamp).mix()
        self.out = Mix([self.wave1, self.wave2], voices=2)

class Reson(BaseSynth):
    """
    Stereo resonators.
    
    A Resonator network feeded with a white noise.
    
    Parameters:

        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        Chorus depth : Depth of the frequency deviation between the left and right channels.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    _______________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.deviation = Randi(min=0.-self.p2, max=self.p2, freq=[random.uniform(2,4) for i in range(4)], add=1)
        self.excite = Noise(.02)
        self.leftamp = self.amp*self.panL
        self.rightamp = self.amp*self.panR
        self.wave1 = Waveguide(self.excite, freq=self.pitch*self.deviation[0], dur=30, minfreq=1, mul=self.leftamp)
        self.wave2 = Waveguide(self.excite, freq=self.pitch*self.deviation[1], dur=30, minfreq=1, mul=self.rightamp)
        self.filt1 = Biquad(self.wave1, freq=self.p3).mix()
        self.filt2 = Biquad(self.wave2, freq=self.p3).mix()
        self.out = Mix([self.filt1, self.filt2], voices=2)

class CrossFmSynth(BaseSynth):
    """
    Cross frequency modulation synthesis.
    
    Frequency modulation synthesis where the output of both oscillators modulates the 
    frequency of the other one. 

    Parameters:

        FM Ratio : Ratio between carrier frequency and modulation frequency.
        FM Index 1 : This value multiplied by the carrier frequency gives the carrier 
                     amplitude for modulating the modulation oscillator frequency.
        FM Index 2 : This value multiplied by the modulation frequency gives the modulation 
                     amplitude for modulating the carrier oscillator frequency.
    
    __________________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    __________________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config,  mode=1)
        self.indexLine = self.amp * self.p2
        self.indexrnd = Randi(min=.95, max=1.05, freq=[random.uniform(.5,2) for i in range(4)])
        self.indexLine2 = self.amp * self.p3
        self.indexrnd2 = Randi(min=.95, max=1.05, freq=[random.uniform(.5,2) for i in range(4)])
        self.norm_amp = self.amp * 0.1
        self.leftamp = self.norm_amp*self.panL
        self.rightamp = self.norm_amp*self.panR
        self.fm1 = CrossFM(carrier=self.pitch, ratio=self.p1, ind1=self.indexLine*self.indexrnd[0], 
                            ind2=self.indexLine2*self.indexrnd2[0], mul=self.leftamp).mix()
        self.fm2 = CrossFM(carrier=self.pitch*.997, ratio=self.p1, ind1=self.indexLine*self.indexrnd[1], 
                            ind2=self.indexLine2*self.indexrnd2[1], mul=self.rightamp).mix()
        self.fm3 = CrossFM(carrier=self.pitch*.995, ratio=self.p1, ind1=self.indexLine*self.indexrnd[2], 
                            ind2=self.indexLine2*self.indexrnd2[2], mul=self.leftamp).mix()
        self.fm4 = CrossFM(carrier=self.pitch*1.002, ratio=self.p1, ind1=self.indexLine*self.indexrnd[3], 
                            ind2=self.indexLine2*self.indexrnd2[3], mul=self.rightamp).mix()
        self.filt1 = Biquad(self.fm1+self.fm3, freq=5000, q=1, type=0)
        self.filt2 = Biquad(self.fm2+self.fm4, freq=5000, q=1, type=0)
        self.out = Mix([self.filt1, self.filt2], voices=2)

class OTReson(BaseSynth):
    """
    Out of tune waveguide model with a recursive allpass network.
    
    A waveguide model consisting of a delay-line with a 3-stages recursive allpass filter 
    which made the resonances of the waveguide out of tune.
    
    Parameters:

        Transposition : Transposition, in semitones, of the pitches played on the keyboard.
        Detune : Control the depth of the allpass delay-line filter, i.e. the depth of the detuning.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    _______________________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _______________________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.excite = Noise(.02)
        self.leftamp = self.amp*self.panL
        self.rightamp = self.amp*self.panR
        self.wave1 = AllpassWG(self.excite, freq=self.pitch, feed=1, detune=self.p2, minfreq=1, mul=self.leftamp)
        self.wave2 = AllpassWG(self.excite, freq=self.pitch*.999, feed=1, detune=self.p2, minfreq=1, mul=self.rightamp)
        self.filt1 = Biquad(self.wave1, freq=self.p3).mix()
        self.filt2 = Biquad(self.wave2, freq=self.p3).mix()
        self.out = Mix([self.filt1, self.filt2], voices=2)

class InfiniteRev(BaseSynth):
    """
    Infinite reverb.
    
    An infinite reverb feeded by a short impulse of a looped sine. The impulse frequencies
    is controled by the pitches played on the keyboard.
    
    Parameters:

        Transposition : Transposition, in semitones, applied on the sinusoidal impulse.
        Brightness : Amount of feedback of the looped sine.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    _____________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _____________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.table = CosTable([(0,0), (4000,1), (8191,0)])
        self.feedtrig = Ceil(self.amp)
        self.feedadsr = MidiAdsr(self.feedtrig, .0001, 0.0, 1.0, 4.0)
        self.env = TrigEnv(self.trig, self.table, dur=.25, mul=.2)
        self.src1 = SineLoop(freq=self.pitch, feedback=self.p2*0.0025, mul=self.env)
        self.src2 = SineLoop(freq=self.pitch*1.002, feedback=self.p2*0.0025, mul=self.env)
        self.excite = self.src1+self.src2
        self.leftamp = self.amp*self.panL
        self.rightamp = self.amp*self.panR
        self.rev1 = WGVerb(self.excite, feedback=self.feedadsr, cutoff=15000, mul=self.leftamp)
        self.rev2 = WGVerb(self.excite, feedback=self.feedadsr, cutoff=15000, mul=self.rightamp)
        self.filt1 = Biquad(self.rev1, freq=self.p3).mix()
        self.filt2 = Biquad(self.rev2, freq=self.p3).mix()
        self.out = Mix([self.filt1, self.filt2], voices=2)

class Degradation(BaseSynth):
    """
    Signal quality reducer.
    
    Reduces the sampling rate and/or bit-depth of a chorused complex waveform oscillator.
    
    Parameters:

        Bit Depth : Signal quantization in bits.
        SR Scale : Sampling rate multiplier.
        Lowpass Cutoff : Cutoff frequency of the lowpass filter.
    
    _____________________________________________________________________________________
    Author : Olivier Bélanger - 2011
    _____________________________________________________________________________________
    """
    def __init__(self, config):
        BaseSynth.__init__(self, config, mode=1)
        self.table = HarmTable([1,0,0,.2,0,0,.1,0,0,.07,0,0,0,.05]).normalize()
        self.leftamp = self.amp*self.panL
        self.rightamp = self.amp*self.panR
        self.src1 = Osc(table=self.table, freq=self.pitch, mul=.25)
        self.src2 = Osc(table=self.table, freq=self.pitch*0.997, mul=.25)
        self.src3 = Osc(table=self.table, freq=self.pitch*1.004, mul=.25)
        self.src4 = Osc(table=self.table, freq=self.pitch*1.0021, mul=.25)
        self.deg1 = Degrade(self.src1+self.src3, bitdepth=self.p1, srscale=self.p2, mul=self.leftamp)
        self.deg2 = Degrade(self.src2+self.src4, bitdepth=self.p1, srscale=self.p2, mul=self.rightamp)
        self.filt1 = Biquad(self.deg1, freq=self.p3).mix()
        self.filt2 = Biquad(self.deg2, freq=self.p3).mix()
        self.mix = Mix([self.filt1, self.filt2], voices=2)
        self.out = DCBlock(self.mix)


