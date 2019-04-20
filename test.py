#!/usr/bin/env python

import numpy as np 
import nam_fingerprint as fingerprint
#import fingerprint_shazam as fingerprint 
from matplotlib import pyplot as plt 
from collections import Counter 
import pickle

################## test Shazam with 2 songs ######################

#fingerprint_origin = None 

#with open("./nam-db/Yesterday - The Beatles.pkl", "rb") as f:
#    fingerprint_origin = pickle.load(f)
n_fft = 1024

fingerprint_origin = fingerprint.fingerprint_audio_shazam("./audio/Yesterday - The Beatles.wav", n_fft=n_fft)

fingerprint_test = fingerprint.fingerprint_audio_shazam("./audio/yesterday cover.wav", n_fft=n_fft, debug=True)
 
length_origin = len(fingerprint_origin)
length_test = len(fingerprint_test)
# #print(length_origin, length_test)
match = []
# # # 
point_origin = []
point_test = []
# # # 
for i in range(length_origin):
     for j in range(length_test):
        if fingerprint_origin[i, 0] == fingerprint_test[j, 0]:
             match.append( int( float(fingerprint_origin[i, 1]) - float(fingerprint_test[j, 1]) ) )
             point_origin.append(fingerprint_origin[i, 1])
             point_test.append(fingerprint_test[j, 1])
# # # 
match = abs(np.asarray(match))
# #count = max(np.bincount(match))
# #match = match.astype(str)
# # # 
# #print(count)
letter_counts = Counter(match)
plt.subplot(211)
plt.title("Scatterplot of matching hash locations")
plt.scatter(point_origin, point_test, c='r', alpha=1)

ax = plt.subplot(212)
frequencies = letter_counts.values()
names = letter_counts.keys()
x_coords = np.arange(len(letter_counts))
plt.title("Histogram of differences of time offsets: signals match")
plt.xlabel("Offset t(database) - t(record)")
ax.bar(x_coords, frequencies, align='center')
ax.xaxis.set_major_locator(plt.FixedLocator(x_coords))
ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
plt.show()
