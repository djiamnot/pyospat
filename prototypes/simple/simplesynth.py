import os
import time
import pyo

S_RATE = 44100
BACKEND = 'portaudio'

class Pluck(object):
    def __init__(self):

        self.table = None
        self.metronome = None
        self.pick = None
        self.s1 = None
        self.s2 = None
    
    def run(self):
         self.s1 = pyo.Sine(freq=400, mul=.5).out(0)
         self.s2 = pyo.Sine(freq=250, mul=.5).out(1)

if __name__ == '__main__':
    server = pyo.Server(sr=S_RATE, nchnls=2).boot()
    server.start()

    pluck = Pluck()
    pluck.run()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt, e: # Ctrl-C
        # raise e
        print(e)
        os._exit(0)
    except SystemExit, e: # sys.exit()
        # raise e
        print(e)
        os._exit(0)
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        os._exit(1)
