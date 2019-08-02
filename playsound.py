import sys
import time
import numpy as np
import json
import argparse
import wave

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

def check_shape(value):
    if value.startswith('si'):
        return 'sine'
    elif value.startswith('sq'):
        return 'square'
    else:
        raise argparse.ArgumentTypeError("{} is not a valid shape for sound wave".format(value))

parser = argparse.ArgumentParser()
parser.add_argument('tones', help="Tone[s] in the sound, in Hz", nargs='+')
parser.add_argument('-s', '--sequence', help="Generate sequence instead of chord", action='store_true', required=False)
parser.add_argument('-d', '--duration', help="Duration of sound, in seconds", nargs='?', default=3.0, type=float)
parser.add_argument('-f', '--freq', help="Sampling frequency, in Hz", nargs='?', default=48000, type=int)
parser.add_argument('-v', '--volume', help="Volume coefficient [0-100]", nargs='?', default=100, type=check_percentage)
parser.add_argument('--write-txt', '--wt', help="Write samples to txt file", action='store_true', required=False)
parser.add_argument('--write-wav', '--ww', help="Write samples to wav file", action='store_true', required=False)
parser.add_argument('-q', '--quiet', help="Quiet mode: don't play sound", action='store_true', required=False)

args = parser.parse_args()

tone_list = [ float(t) for t in args.tones ]
seq = True if args.sequence else False
duration = args.duration
fs = args.freq
volume = args.volume * 0.01
write_txt = True if args.write_txt else False
write_wav = True if args.write_wav else False
quiet_mode = True if args.quiet else False

print('Generate tones...')

tone_array_list = []

for freq in tone_list:
    # generate samples
    new_samples = np.sin(2*np.pi*freq*np.arange(0., duration, 1/fs), dtype=np.float32)
    tone_array_list.append(new_samples)

print('Combine tones...')
if not seq:
  # build list of sampled tones but multiplied by 1/N where N is number of tones
  # this way when we sum them together we are sure not to exceed |1|
  tmp_list = []
  for a in tone_array_list:
    tmp_list.append(np.multiply(1/len(tone_array_list), a, dtype=np.float32)) 
  tmp_samples = np.sum(tmp_list, axis=0)
else:
  tmp_samples = np.zeros(1, dtype=np.float32)
  for a in tone_array_list:
    tmp_samples = np.concatenate([tmp_samples, a])
# find maximum sampled value after combination
tmp_max = np.amax(tmp_samples)
# build final array normalized to maximum value
samples = np.multiply(1/tmp_max, tmp_samples, dtype=np.float32)

if volume < 100:
  print('Apply volume...')
  samples = np.multiply(volume, samples, dtype=np.float32)

if write_txt or write_wav:
  fname = "sound_" + ( 'seq_' if seq else '' ) + "_".join([ str(int(x)) for x in tone_list ])

if write_txt:
    array_fname = fname + '.txt'
    print('Write samples to file {}'.format(fname))
    np.savetxt(array_fname, samples, fmt='%.3f')

if write_wav:
    wave_fname = fname + '.wav'
    print('Write samples to file {}'.format(wave_fname))
    wave_out = wave.open(wave_fname, "wb")
    wave_out.setnchannels(1)
    wave_out.setsampwidth(2)
    wave_out.setframerate(fs)
    wave_out.writeframes(np.int16(32767*samples))
    wave_out.close()

if not quiet_mode:
  print('Play sound (Ctrl+C to interrupt)...')
  import sounddevice as sd
  sd.default.device = 0
  sd.default.samplerate = fs
  try:
      sd.play(samples, blocking=True)
  except KeyboardInterrupt:
      sd.stop()
  
