import sys
import time
import numpy as np
import sounddevice as sd
import json
import argparse

def print_err(*args, **kwargs):
  kwargs['file'] = sys.stderr
  print(*args, **kwargs)

def check_percentage(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("{} is not a valid percentage [0-100]".format(value))
    if ivalue < 0 or ivalue > 100:
        raise argparse.ArgumentTypeError("{} is not a valid percentage [0-100]".format(value))
    return ivalue

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--duration', help="Duration of sound, in seconds", nargs='?', default=3, type=int)
parser.add_argument('-f', '--freq', help="Sampling frequency, in Hz", nargs='?', default=48000, type=int)
parser.add_argument('-v', '--volume', help="Volume coefficient [0-100]", nargs='?', default=100, type=check_percentage)
parser.add_argument('--write-wav', '--ww', help="Write samples to wav file", nargs='?', default='')
parser.add_argument('-q', '--quiet', help="Quiet mode: don't play sound", action='store_true', required=False)

args = parser.parse_args()

duration = args.duration
fs = args.freq
volume = args.volume * 0.01
write_wav = args.write_wav
quiet_mode = True if args.quiet else False

# set parameter for both input and output
sd.default.samplerate = fs

# set parameters for input device
# discovered device from "python3 -m sounddevice"
sd.default.device = 2
sd.default.channels = 1 
print('Record sound for {} seconds...'.format(duration))
samples = sd.rec(duration * fs, blocking=True)

if volume != 1:
    print('Apply volume...')
    samples = np.multiply(volume, samples, dtype=np.float32)

if write_wav:
    import wave
    from time import gmtime, strftime
    #wave_fname = 'rec_' + strftime("%Y%m%d_%H%M%S", gmtime()) + '.wav'
    wave_fname = write_wav
    print('Write samples to file {}'.format(wave_fname))
    wave_out = wave.open(wave_fname, "wb")
    wave_out.setnchannels(1)
    wave_out.setsampwidth(2)
    wave_out.setframerate(fs)
    wave_out.writeframes(np.int16(32767*samples))
    wave_out.close()

if not quiet_mode:
    # set parameters for output device
    sd.default.device = 0
    sd.default.channels = 2 
    print('Play sound (Ctrl+C to interrupt)...')
    try:
        sd.play(samples, blocking=True)
    except KeyboardInterrupt:
        sd.stop()

