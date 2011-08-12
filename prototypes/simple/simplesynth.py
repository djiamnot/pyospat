import os
import pyo

S_RATE = 44100
BACKEND = 'portaudio'


class Pluck(object):
	def __init__(self):

		self.table = None
		self.metronome = None
		self.pick = None
		self.w = None
	
	def run(self):
		self.table = pyo.LinTable([(0,0), (2,1), (5,0), (8191,0)])
		self.metronome = pyo.Metro(.25, 4).play()
		self.pick = pyo.TrigEnv(self.metronome, table=self.table, dur=1)
		self.w = pyo.Waveguide(self.pick, freq=[200,400], dur=20, minfreq=20, mul=.5).out()


def main():
	server = pyo.Server(audio = BACKEND, jackname = 'pluck', sr = S_RATE, buffersize = 512).boot()
	server.start()
	pluck = Pluck()
	pluck.run()
    

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        os._exit(1)
