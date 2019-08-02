import wave
import struct
import numpy as np
import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import sys
import argparse

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
parser.add_argument('wavFile', help='Wav file name')
parser.add_argument('-f', '--fontSize', help = 'Font size', nargs= '?', default=12, type=int)
parser.add_argument('-p', '--pdf', help="Generate pdf instead of displaying figure", action='store_true', required=False)

# parse arguments
parse = parser.parse_args() 
wavFileName = parse.wavFile
fontSize = parse.fontSize
pdf = True if parse.pdf else False

if pdf:
  matplotlib.use('Agg')

data, frate = loadWav(wavFileName)

# create (mel) spectrogram
plt.figure()
S = librosa.feature.melspectrogram(data.astype(float), frate, n_mels=256)
log_S = librosa.power_to_db(S, ref=np.max)
librosa.display.specshow(log_S, sr=frate, x_axis='time', y_axis='mel')
#librosa.display.specshow(S, sr=frate, x_axis='time', y_axis='mel')

#plt.title('mel power spectrogram')

plt.xlabel("Time [s]",fontsize=int(fontSize))
plt.ylabel("Frequency [Hz]",fontsize=int(fontSize))

#plt.xticks(np.arange(0,50,10),np.arange(0,50,10))
plt.xticks(fontsize=int(fontSize))

#plt.yticks(np.arange(0,8000,1000), np.arange(0,8000,1000))
#plt.yticks([0, 500, 1000, 2000, 4000, 8000], fontsize=int(fontSize))

cbar = plt.colorbar(format='%+02.0f dB')
cbar.ax.tick_params(labelsize=int(fontSize))

#plt.axvline(x=2.7,linestyle='dashed',linewidth=4,color='#13D9D9',label="Queue length > threshold")
#plt.axvline(x=9.4,linestyle='dashed',linewidth=4,color='#FFE527',label="75 packets")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=4,color='#22D913',label="25 packets")

#plt.axvline(x=5.3,linestyle='dashed',linewidth=4,color='#22D913',label="Low threshold")
#plt.axvline(x=9.4,linestyle='-.',linewidth=4,color='#13D9D9',label="High threshold")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=3,color='#22D913',label="25 packets")
#plt.axvline(x=12.6,linestyle='dashed',linewidth=4,color='#22D913')

#plt.yticks(np.arange(0,900,100),fontsize=int(sys.argv[2]))
#plt.xlim(23,36)
#plt.ylim(ymin=2048)
#plt.legend(loc='upper right',framealpha=1)
#plt.legend(prop={'size': 16})
#plt.locator_params(axis='x', nbins=5)

plt.tight_layout()

if pdf:
  #plt.gray()
  plt.savefig(wavFileName.replace('.wav', '_mel.pdf'))
else:
  plt.show()

