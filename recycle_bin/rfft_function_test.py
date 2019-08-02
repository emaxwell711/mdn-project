import wave
import struct
import numpy as np
import sys
from scipy.fftpack import rfft, rfftfreq
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
parser.add_argument('-f', '--fontSize', help = 'Font size', nargs= '?', default=12, type=int)

#parsing
parse = parser.parse_args() 
wavFileList = parse.wavFile
fontSize = parse.fontSize

#print(wavFileList)
#print(fontSize)

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

#plt.figure()

#tup[0] represents amplitude and tup[1] represents frequency
#tempmax = 0
#max_i = 0
#for tup in dftFrate:
#    ampl_list = tup[0]
#    freq_list = tup[1]
#    for i in range(len(ampl_list)):
#        if ampl_list[i] > tempmax:
#            tempmax = ampl_list[i]
#            max_i = i 
#
#    print(freq_list[max_i])

thresh = 1e5

#for tup in dftFrate:
#    ampl_list = tup[0]
#    freq_list = tup[1]
#    for a, f in zip(ampl_list, freq_list):
#      if a > thresh:
#        print(f, a)

for tup in dftFrate:
  for i in range(tup[0].size):
    if tup[0][i] > thresh:
      print(tup[1][i], tup[0][i])
