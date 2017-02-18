# -*- coding: utf-8 -*-
import sys
import pyaudio
from numpy.fft import rfft
from numpy import int16, empty, fromstring, roll

FFT_LEN = 1024 # size of rolling buffer for FFT
CHUNK = 128 # Size of each 'frame' in rolling buffer
SIGNAL_SCALE = 0.0000003 # Scaling factor for output
RATE = 16000 # Sampling rate


SPARKS = [
  ' ',
  u'\u2581',
  u'\u2582',
  u'\u2583',
  u'\u2584',
  u'\u2585',
  u'\u2586',
  u'\u2587',
  u'\u2588'
]
SPARKS_LEN = len(SPARKS)


def spark(i):
    i = int(i * SPARKS_LEN)
    if i >= SPARKS_LEN:
        # Go red when it's above max height
        return u'\033[0;31m' + SPARKS[-1] + u'\033[0m'
    return SPARKS[i]


def run():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1, # Mono
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    signal = empty(FFT_LEN, dtype=int16)

    try:
        # Disable cursor
        sys.stdout.write('\033[?25l')
        while 1:
            # Roll in new frame into buffer
            signal = roll(signal, -CHUNK)
            signal[-CHUNK:] = fromstring(stream.read(CHUNK), dtype=int16)

            # Now transform!
            fftspec = rfft(signal)

            # Print it
            bars = u''.join(spark(abs(x * SIGNAL_SCALE)) for x in fftspec[1 : FFT_LEN / 5])
            sys.stdout.write('\r' + bars)
    except KeyboardInterrupt:
        print ''
    finally:
        # Turn the cursor back on
        sys.stdout.write('\033[?25h')


if __name__ == "__main__":
    run()
