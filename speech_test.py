#!/usr/bin/env python

import numpy as np
import nam_fingerprint as fingerprint 
#import fingerprint_shazam as fingerprint 
import librosa
import librosa.display 
from scipy.io import wavfile 
import matplotlib.pyplot as plt 
import scipy 
import soundfile as sf 
import matplotlib.mlab as mlab 
from collections import Counter

############# test Shazam with speech file #########3

fan_value = 30
neighborhood_numb = 3

fingerprint_origin = fingerprint.fingerprint_audio_shazam("./audio/turn_on_-_male_US.wav",debug=True,n_fft=256, neighborhood_numb=neighborhood_numb, fan_value=fan_value, region_t=100)

fingerprint_test = fingerprint.fingerprint_audio_shazam("./audio/turn_on_-_female_US.wav", debug=True, n_fft=256, neighborhood_numb=neighborhood_numb, fan_value=fan_value, region_t=100)

length_origin = len(fingerprint_origin)
length_test = len(fingerprint_test)
#print(length_origin, length_test)
match = []

point_origin = []
point_test = []

for i in range(length_origin):
    for j in range(length_test):
        if fingerprint_origin[i, 0] == fingerprint_test[j, 0]:
            match.append( int( float(fingerprint_origin[i, 1]) - float(fingerprint_test[j, 1]) ) )
            point_origin.append(fingerprint_origin[i, 1])
            point_test.append(fingerprint_test[j, 1])

#print(match)
match = abs(np.asarray(match))
#count = max(np.bincount(match))

#print(count)
letter_counts = Counter(match)
plt.subplot(211)
plt.scatter(point_origin, point_test, c='r', alpha=1)
ax = plt.subplot(212)
frequencies = letter_counts.values()
names = letter_counts.keys()
x_coords = np.arange(len(letter_counts))
ax.bar(x_coords, frequencies, align='center')
ax.xaxis.set_major_locator(plt.FixedLocator(x_coords))
ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
plt.show()

#####################################################################33
#y, fs = sf.read("./audio/goodbye.wav", dtype='float32')
#y_sf = y_sf.astype(np.float)
#fs, y = wavfile.read("./audio/goodbye.wav")
#y = y.astype(np.float)
#print(y_sf)
#print(y)

#spectrum = np.abs(librosa.stft(y, n_fft=256, hop_length=128, center=False))
#spectrum_sf = librosa.amplitude_to_db(spectrum_sf, top_db=0)

#spectrum = 20 * np.log10(spectrum)
#spectrum_sf[spectrum_sf == -np.inf] = 0
#print(np.min(spectrum_sf), np.max(spectrum_sf))
#spectrum = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=256, hop_length=128, center=False)))
#print(np.max(spectrum), np.max(spectrum_sf))
#print(spectrum[0])

#print(spectrum_sf[0])

#plt.figure(1)
#librosa.display.specshow(spectrum, sr=fs, cmap='Greys', x_axis='time', y_axis='linear')
#plt.colorbar(format='%+2.0f dB')
#spec, _, _ = mlab.specgram(y, NFFT=256, noverlap=128, window=mlab.window_hanning, Fs=fs)
#spec = 10*np.log10(spec)
#spec[spec == -np.inf] = 0
#print(np.min(spec), np.max(spec))

#plt.figure(2)
#librosa.display.specshow(spectrum, sr=fs, cmap='Greys', x_axis='time', y_axis='linear')
#plt.colorbar(format='%+2.0f dB')

#plt.figure(3)
#librosa.display.specshow(spec, sr=fs, cmap='Greys', x_axis='time', y_axis='linear')
#plt.colorbar(format='%+2.0f dB')

#plt.figure(4)
#plt.subplot(211)
#plt.plot(y)
#plt.subplot(212)
#plt.plot(y_sf)
#plt.show()
