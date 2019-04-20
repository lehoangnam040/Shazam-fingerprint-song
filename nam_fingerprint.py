#!/usr/bin/env python

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab 
import hashlib 
from operator import itemgetter 

from scipy.io import wavfile 
from scipy.ndimage.filters import maximum_filter 
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion 
import librosa 
import librosa.display 
import scipy.signal
from collections import Counter
import pickle
import soundfile as sf 
from skimage.feature import peak_local_max 

DEFAULT_NFFT = 4096
DEFAULT_OVERLAP_RATIO = 0.5
FAN_VALUE = 20

MIN_AMPLITUDE = 10

NEIGHBORHOOD_NUMBER = 10
REGION_F = 200
REGION_T = 200
HASH_KEEP = 24              # CHARACTERS
DEFAULT_BACKGROUND = 0

def fingerprint_audio_shazam(file_name, debug=False, n_fft=DEFAULT_NFFT, overlap_ratio=DEFAULT_OVERLAP_RATIO, neighborhood_numb=NEIGHBORHOOD_NUMBER, min_amplitude=MIN_AMPLITUDE, fan_value=FAN_VALUE,
        region_t=REGION_T, region_f=REGION_F):

    data, fs = sf.read(file_name)
    data = librosa.resample(data, fs, 8000)
    fs = 8000

    #spectrum, _, _ = mlab.specgram(data, NFFT=n_fft, Fs=fs, window=mlab.window_hanning, noverlap=int(n_fft * overlap_ratio))
    spectrum = np.abs(librosa.stft(data, n_fft=n_fft, hop_length=int(n_fft * overlap_ratio), window=scipy.signal.hanning, center=False))
    
    spectrum = 20 * np.log10(spectrum)
    spectrum[spectrum == -np.inf] = np.min(spectrum)

    ## find peaks algorithm
    peaks_filtered = peak_local_max(spectrum, threshold_abs=np.median(spectrum), min_distance=neighborhood_numb)


    freq_idx = peaks_filtered[:, 0]   
    time_idx = peaks_filtered[:, 1]  
    
    if debug:
        plt.figure(1)
        plt.plot(np.arange(len(data)) * 1.0 / fs, data)
        plt.ylabel("Amplitude")
        plt.xlabel("Time (s)")

        duration = librosa.get_duration(y=data, sr=fs)
 
        freq_unit = (fs / 2.0) / spectrum.shape[0]
        time_unit = duration / spectrum.shape[1]
        plt.figure(2)
        librosa.display.specshow(spectrum, sr=fs, cmap='Greys', x_axis='s', y_axis='linear', x_coords=np.arange(spectrum.shape[1] + 1)*time_unit)
        plt.colorbar(format='%+2.0f dB')
        plt.scatter(time_idx * time_unit, freq_idx * freq_unit, c='r', s=5)
        plt.show()

    star = zip(freq_idx, time_idx)
    star.sort(key=itemgetter(1, 0))
    star = np.asarray(star)

    fingerprints = list()
    star_length = len(star)

    for i in range(star_length):
        for j in range(1, fan_value):
            if (i + j) < star_length and (star[i + j, 1] - star[i, 1]) > 0 and (star[i + j, 1] - star[i, 1]) < region_t:
                freq_anchor = star[i, 0]
                freq_target = star[i + j, 0]

                offset_anchor = star[i, 1]
                delta_t = star[i + j, 1] - star[i, 1]
                
                h = hashlib.sha1("%s|%s|%s" % (str(freq_anchor), str(freq_target), str(delta_t)))

                fingerprints.append([h.hexdigest()[0:HASH_KEEP], offset_anchor])

    return np.asarray(fingerprints, dtype=object)
