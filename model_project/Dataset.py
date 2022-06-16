"""
this class represents the dataset ,converting audio data into mel-spectrogram returning train and test data splits
Augmentation of train data

"""
import os.path
from collections import Counter

import librosa
import numpy as np
import pandas as pd
from librosa import display
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from audiomentations import Compose, AddGaussianNoise, PitchShift
from matplotlib import pylab


class Dataset:

    def __init__(self, sound_type):
        self.y_test = []
        self.y_train = []
        self.X_test = []
        self.X_train = []
        self.sr = 22500
        self.custpath = 'sounds_dataset'
        self.csvpath = 'sounds_csv'
        self.sound_type = sound_type

    def perform_Oversampling_Smote(self):
        counter = Counter(self.y_train)
        print(counter)
        counter = Counter(self.y_test)
        print(counter)

        for x in self.y_train:
            if str(x) == 'nan':
                print(x)
                i = self.y_train.index('nan')
                # dict['X_train'] = dict['X_train'].tolist()
                self.X_train.pop(i)
                self.y_train = [x for x in self.y_train if str(x) != 'nan']
        print("deleted nan")
        self.X_train = np.array(self.X_train)
        self.y_train = np.array(self.y_train)
        sm = SMOTE(random_state=2)
        print("ok")
        X_train_res, y_train_res = sm.fit_resample(self.X_train, self.y_train)
        print('After OverSampling, the shape of train_X: {}'.format(X_train_res.shape))
        print('After OverSampling, the shape of train_y: {} \n'.format(y_train_res.shape))
        self.X_train = X_train_res
        self.y_train = y_train_res

    def create_Train_And_Test_data(self, csvfile):
        print("I entered here")
        df = pd.read_csv(csvfile)
        print("I read the csv file")
        y = np.array(df['label'].values.tolist())
        X = np.array(df.loc[:, df.columns != 'label'])
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42,
                                                                                shuffle=False)
        self.perform_Oversampling_Smote()

    def generateMel(self, audio):
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
        mel = librosa.feature.melspectrogram(y=audio, sr=self.sr)
        s_db = librosa.power_to_db(mel, ref=np.max)
        display.specshow(s_db)
        return s_db

    def savelist(self, dict1):

        for k, v in dict1.items():
            print(k)
            if k == "X_train":
                pathaudio = os.path.join(self.custpath, self.sound_type, str(k) + ".npy")
                np.save(pathaudio, v)
                print("done {} {}".format(str(k), self.sound_type))

            if k == "X_test":
                pathaudio = os.path.join(self.custpath, self.sound_type, str(k) + ".npy")
                np.save(pathaudio, v)
                print("done {} {}".format(str(k), self.sound_type))

            if k == "y_train":
                df = pd.DataFrame(v, columns=['label'])
                pathaudio = os.path.join(self.custpath, self.sound_type, str(k) + ".csv")
                df.to_csv(pathaudio.format(str(k)), index=False)
                print("done {} {}".format(str(k), self.sound_type))

            if k == "y_test":
                df = pd.DataFrame(v, columns=['label'])
                pathaudio = os.path.join(self.custpath, self.sound_type, str(k) + ".csv")
                df.to_csv(pathaudio.format(str(k)), index=False)
                print("done {} {}".format(str(k), self.sound_type))

    add_noise = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.7),
    ])
    pitch_shift = Compose([
        PitchShift(min_semitones=-4, max_semitones=12, p=0.5),
    ])

    def generateMelSpectogram(self):
        # looping through train data to create melspec and augment data
        # temporary list for the input data
        Xtrain = []

        # list to append all the labels
        Y_train_ = []

        print(len(self.X_train))
        for i in range(len(self.X_train)):
            # try:

            print(i)
            y = self.y_train[i]
            # adding noise to the file
            noisy_audio = self.add_noise(self.X_train[i], 22050)
            # changing pitch of the audio
            pitch_audio = self.pitch_shift(self.X_train[i], 22050)

            # generate melspec for original and augmented files
            pylab.axis('off')  # no axis

            mel = self.generateMel(self.X_train[i])
            noise_mel = self.generateMel(noisy_audio)
            pitch_mel = self.generateMel(pitch_audio)

            # appending augmented data to original training data
            Xtrain.append(mel)
            Y_train_.append(y)
            Xtrain.append(noise_mel)
            Y_train_.append(y)
            Xtrain.append(pitch_mel)
            Y_train_.append(y)

        # except Exception as e:
        #     print("Error in file:")
        #     print("Error:", e)
        #     continue

        print(len(Xtrain))
        print(len(Y_train_))
        self.X_train = Xtrain
        self.y_train = Y_train_
        train_dict = {'X_train': self.X_train, 'y_train': self.y_train}
        self.savelist(train_dict)

    # looping through train data to create melspec and augment data
    # for i, dat in tqdm(enumerate(audio_test)):

    def testgeneratespec(self):
        # temporary list for the input data
        Xtest = []

        # list to append all the labels
        Y_test = []
        for i in range(len(self.X_test)):

            # try:
                print(i)
                # generate melspec for original and augmented files
                # mel = get_melspec(dat)
                mel = self.generateMel(self.X_test[i])

                # Appending test melspec to list
                Xtest.append(mel)
                Y_test.append(self.y_test[i])


            # except Exception as e:
            #     print("Error in file:")
            #     print("Error:", e)

        self.X_test = Xtest
        self.y_test = Y_test
        test_dict = {'X_test': self.X_test, 'y_test': self.y_test}
        self.savelist(test_dict)

    def samples(self):
        print("ok")
        csv_file = os.path.join(self.csvpath, self.sound_type + '.csv')
        self.create_Train_And_Test_data(csv_file)
        self.generateMelSpectogram()
        # self.testgeneratespec()


sounds = [ 's_cough','h_cough', 's_breath', 'F_count', 'vowel_E', 'vowel_O']

for s in sounds:
    d = Dataset(s)
    d.samples()
