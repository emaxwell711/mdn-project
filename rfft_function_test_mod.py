import wave
import struct
import numpy as np
import sys
from scipy.fftpack import rfft, rfftfreq
import argparse
import operator

def print_err(*args, **kwargs):
  kwargs['file'] = sys.stderr
  print(*args, **kwargs)

def loadWav(fname):
    wav_file = wave.open(fname, 'r')
    data_size = wav_file.getnframes()
    data = wav_file.readframes(data_size)
    frate = wav_file.getframerate()
    wav_file.close()
    data = struct.unpack('{n}h'.format(n=data_size), data)
    data = np.array(data)
    return data, frate

#define parser and arguments 
parser = argparse.ArgumentParser()
parser.add_argument('wavFile', help='List of wav files separated by spaces', nargs = '+')
parser.add_argument('-f', '--fontSize', help = 'Font size', nargs= '?', default=12, type=int)
parser.add_argument('-t', '--threshold', help = 'Threshold', nargs= '?', default=1e6, type=lambda x: int(float(x)))
parser.add_argument('-a', '--alphabet', help = 'Alphabet i.e. comma separated list of possible values of frequency', nargs= '?', default=None)

# parsing
args = parser.parse_args() 
wavFileList = args.wavFile
fontSize = args.fontSize
thresh = args.threshold
alphabet = [int(x) for x in args.alphabet.split(',')] if args.alphabet else None

#print(wavFileList)
#print(fontSize)

dft_dict = {}
thresh_dft_dict = {}

if alphabet:
  alphabet_gap = alphabet[1]-alphabet[0]

for wav in wavFileList:
  print_err('Analyse file {}'.format(wav))
  data, frate = loadWav(wav)
  # normalize volume
  #peak = np.max(data)
  #if peak < 32767:
  #  factor = 32767/peak
  #  data = np.multiply(factor, data, dtype=np.float32)
  # compute DFT
  dft = [int(x) for x in np.abs(rfft(data))]
  freq = [int(x*frate) for x in rfftfreq(len(dft))]
  # accumulate amplitude values for every frequency (a frequency mught have multiple amplitude contributions)
  dft_dict[wav] = {}
  for i in range(len(freq)):
    f = freq[i]
    a = dft[i]
    if f not in dft_dict[wav]:
      dft_dict[wav][f] = 0
    dft_dict[wav][f] += a
  # apply threshold
  thresh_dft_dict[wav] = {}
  for f in dft_dict[wav]:
    #if alphabet and ( f < alphabet[0]-alphabet_gap/2 or f > alphabet[-1]+alphabet_gap/2):
    #  continue
    if dft_dict[wav][f] > thresh:
      thresh_dft_dict[wav][f] = dft_dict[wav][f]

#plt.figure()

for wav in thresh_dft_dict:
  print('\n--- ' + wav)
  print('{:>6}{:>15}'.format('f', 'a'))
  for f in thresh_dft_dict[wav]:
    a = thresh_dft_dict[wav][f]
    print('{:>6}{:>15}'.format(f, a))

  print('After quantization')

  # tmp list of contiguous values
  f_list = sorted(thresh_dft_dict[wav].keys()) + [None]
  cont_f_list = []
  cont_a_list = []
  mean_f_list = []
  sensed_freqs = []
  for f in f_list:
    #print(f)
    if ( not cont_f_list or f == cont_f_list[-1]+1 ) and f != f_list[-1] and f is not None:
      # f is first of contiguous list of is contiguous to last f in list
      cont_f_list.append(f)
    else:
      # f is not contiguous to list: compute average f and average a
      for cf in cont_f_list:
        cont_a_list.append(thresh_dft_dict[wav][cf])
      mean_f = int(sum(cont_f_list)/len(cont_f_list))
      #print(mean_f)
      if alphabet:
        mean_f = min(alphabet, key=lambda x:abs(x-mean_f))
        #distance = min([abs(mean_f-x) for x in alphabet])
        #if distance < alphabet_gap/2:
        #  mean_f = min(alphabet, key=lambda x:abs(x-mean_f))
        #  #mean_f = min(alphabet, key=lambda x:min(abs(x-mean_f), alphabet_gap))
        #else:
        #  mean_f = None
      if mean_f is not None and mean_f not in mean_f_list:
        mean_f_list.append(mean_f)
        mean_a = int(sum(cont_a_list)/len(cont_a_list))
        print('{:>6}{:>15}'.format(mean_f, mean_a))
        sensed_freqs.append(mean_f)
      # and start new contiguous list
      cont_f_list = [f]
      cont_a_list = []

print('Sensed frequencies')
print(",".join([str(f) for f in sensed_freqs]))
