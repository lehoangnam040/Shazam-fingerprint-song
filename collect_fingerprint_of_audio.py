#!/usr/bin/env python

#import fingerprint_shazam as fingerprint 
import nam_fingerprint as fingerprint 
import numpy as np 
import pickle 

#### audio file => fingerprint => dump to .pkl file

file_path = "./audio/Yesterday - The Beatles.wav"

fingerprint_list = fingerprint.fingerprint_audio_shazam(file_path, debug=False)

with open("./nam-db/" + file_path[8:-4] + ".pkl", "wb") as f:
    pickle.dump(fingerprint_list, f)

print('done')
