import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
import numpy as np
import sys
import scipy
from scipy.fftpack import fft, rfft, fftfreq, rfftfreq
import argparse
import operator

def openWav(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        wav_file.close()
        data = struct.unpack('{n}h'.format(n=data_size), data)
        data = np.array(data)
        return data

def getFrate(fname):
        wav_file = wave.open(fname, 'r')
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        frate = wav_file.getframerate()
        return frate

#define parser and arguments 
parser = argparse.ArgumentParser()
parser.add_argument('wavFile', help='List of wav files separated by spaces', nargs = '+')
parser.add_argument('-x', '--xLim', help = 'Upper x axis limit', nargs= '?', default=20000, type=int)
parser.add_argument('-f', '--fontSize', help = 'Font size', nargs= '?', default=12, type=int)
parser.add_argument('-p', '--pdf', help="Generate pdf instead of displaying figure", action='store_true', required=False)

#parsing
parse = parser.parse_args() 
wavFileList = parse.wavFile
x_lim = parse.xLim
fontSize = parse.fontSize
pdf = True if parse.pdf else False

if pdf:
  matplotlib.use('Agg')

print(wavFileList)
print(fontSize)

wavDataFrate = []
for wav in wavFileList:
    data = openWav(wav)
    frate = getFrate(wav)
    wavDataFrate.append((data, frate))

dftFrate = [] 
for tup in wavDataFrate:
    dft = rfft(tup[0])
    freq = rfftfreq(dft.size)
    freqFrate = [int(x*tup[1]) for x in freq]
    dftFrate.append((dft, freqFrate))
#print(wavDataFrate)
#print(dftFrate)
#print abs(sum(map(operator.sub,w1,w2)))

plt.figure()
for tup in dftFrate:
    plt.plot(tup[1], np.abs(tup[0]), color = 'blue', linewidth=1, label='on')

plt.xlim(0, x_lim)

plt.xlabel("Frequency [Hz]", fontsize=fontSize)
plt.ylabel("Magnitude", fontsize=fontSize)

if pdf:
  #plt.gray()
  plt.savefig(wavFileName.replace('.wav', '_rfft.pdf'))
else:
  plt.show()


