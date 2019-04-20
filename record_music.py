#!/usr/bin/env python

import numpy as np 
import soundfile as sf 

##################### record 5s of a song ##################

file_path = "./audio/Anh Nha O Dau The - AMee_B Ray.wav"

y, fs = sf.read(file_path, dtype='float32')

## ghi tu giay thu 5 den giay thu 10
sf.write('./audio/Anh Nha O Dau The sample.wav', y[fs*5:fs*10], fs)

print('done')


