#!/usr/bin/env python

import soundfile as sf
import numpy as np 
import matplotlib.pyplot as plt

############ add noise to an audio file ################

y, fs = sf.read("./audio/yesterday sample.wav")

y_noise = y + 0.05 * np.random.randn(len(y))
sf.write("./audio/yesterday noisy.wav", y_noise, fs)

plt.subplot(211)
plt.plot(y)
plt.subplot(212)
plt.plot(y_noise)
plt.show()
