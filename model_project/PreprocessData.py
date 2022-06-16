"""
this class preprocesses the audio files
"""
import os
import random
from collections import Counter

import librosa
import numpy as np
import pandas as pd




class PreprocessData:

    """
    this function cleans the audio data

    """
    sr = 22500

    def pad_trunc(self,aud, max_ms):
        sig_len = len(aud)
        max_len = 22050 // 1000 * max_ms
        if (sig_len > max_len):
            # Truncate the signal to the given length
            aud = aud[:max_len]
        elif (sig_len < max_len):
            # Length of padding to add at the beginning and end of the signal
            pad_begin_len = random.randint(0, max_len - sig_len)
            print(pad_begin_len)
            pad_end_len = max_len - sig_len - pad_begin_len
            print(pad_end_len)
            aud = np.pad(aud, (pad_begin_len, pad_end_len), 'constant')
        return (aud)

    def clean_audio(self,new_data,s,X,Y):
        for i in range(len(new_data)):
            try:
                print(i)
                audio_file = new_data[s][i]
                class_id = new_data['covid_status'][i]
                reaud, sr = librosa.load(audio_file, duration=4)
                rechan = self.pad_trunc(reaud, 4000)
                X.append(rechan)
                Y.append(class_id)
            except:
                print("not found")
                if new_data.index[i]:
                    new_data.drop([new_data.index[i]])
                else:
                    continue

    def makedirsSound(self,path_audio):
        if not os.path.exists(path_audio):
            os.makedirs(path_audio)
            print("Created Directory : ", dir)
        else:
            print("Directory already existed ")

    def make_csv_sound_type(self):
        path_audio = 'sounds_csv'
        self.makedirsSound(path_audio)
        new_data=pd.read_csv('combine_data.csv')
        status = ' h_cough s_breath F_count vowel_E vowel_O'
        status = status.split()
        for s in status:
            X = []
            Y = []
            print(s)
            self.clean_audio(new_data, s, X, Y)
            counter = Counter(Y)
            print(counter)
            my_ar = np.array(X)
            df = pd.DataFrame(my_ar)
            df.insert(loc=0, column='label', value=Y)
            Counter(Y)
            df.to_csv('{}/{}.csv'.format(path_audio,s))
            print("done one")

# c = CombinedCsv()
# y=c.clean_csv(c)

# p=PreprocessData()
# p.make_csv_sound_type()






