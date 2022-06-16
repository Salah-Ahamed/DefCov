"""
this class represents loading dataset,model creation,training , testing ,saving
"""
import os
import numpy as np
import csv
from sklearn.preprocessing import LabelEncoder

# importing the keras modules
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, GRU, BatchNormalization
from keras import regularizers
from keras.constraints import unit_norm
import tensorflow as tf
from matplotlib import pylab
import seaborn as sns


class SaveModel:

    def __init__(self, soundType, train_and_test_dir):
        self.train_and_test_dir = train_and_test_dir
        self.soundType = soundType
        self.x_train=[]
        self.y_train=[]
        self.xtest=[]
        self.y_test=[]



    def LoadData(self):
        x_train = np.load('./{}/{}/X_train.npy'.format(self.train_and_test_dir, self.soundType))
        x_test = np.load('./{}/{}/X_test.npy'.format(self.train_and_test_dir, self.soundType))
        x_train = np.stack(x_train)
        x_test = np.stack(x_test)

        with open('./{}/{}/y_train.csv'.format(self.train_and_test_dir, self.soundType), newline='') as f:
            reader = csv.reader(f)
            y_train = list(reader)
        y_train.pop(0)


        with open('./{}/{}/y_test.csv'.format(self.train_and_test_dir, self.soundType), newline='') as f:
            reader = csv.reader(f)
            y_test = list(reader)
        y_test.pop(0)

        encoder = LabelEncoder()
        encoder.fit(y_train)

        self.y_train = encoder.transform(y_train).reshape([len(y_train), 1])

        encoder = LabelEncoder()
        encoder.fit(y_test)

        self.y_test = encoder.transform(y_test).reshape([len(y_test), 1])

        self.X_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
        self.xtest = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

        # print(self.X_train.shape)
        # print(self.xtest.shape)
        # print(self.y_train.shape)
        # print(self.y_test.shape)
        return self.X_train, self.y_train, self.xtest, self.y_test

    def CreateModel1(self, epochs, splits_dataset):
        x_train, y_train, xtest, y_test = splits_dataset
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform',
                         kernel_regularizer=regularizers.l2(l=0.01), padding='same', input_shape=(x_train.shape[1:])))
        Dropout(0.25),
        model.add(Conv2D(64, kernel_size=(3, 3), strides=(2, 2), activation='relu',
                         kernel_regularizer=regularizers.l2(l=0.01), padding='same')),
        model.add(MaxPooling2D((2, 2)))
        BatchNormalization()
        Dropout(0.2),

        model.add(Flatten())
        model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(1, activation='sigmoid'))

        '''
        Optimizer = Adam
        Loss = binary_crossentropy
        '''
        optimiser = tf.optimizers.Adam(learning_rate=0.0001)
        model.compile(loss='binary_crossentropy', optimizer=optimiser, metrics=['accuracy'])
        model.summary()

        history = model.fit(x_train, y_train, validation_data=(xtest, y_test), batch_size=32, epochs=epochs)

        if not os.path.exists('models'):
            os.makedirs('models')

        print("saving model")
        model.save('models/{}_model'.format(self.soundType))

        return history

    def CreateModel2(self,epochs, splits_dataset):
        x_train, y_train, xtest, y_test = splits_dataset
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same',
                         input_shape=(x_train.shape[1:])))
        Dropout(0.25),
        model.add(Conv2D(64, kernel_size=(3, 3), strides=(2, 2), activation='relu', padding='same')),
        model.add(MaxPooling2D((2, 2)))
        BatchNormalization()

        model.add(Flatten())
        model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(1, activation='sigmoid'))

        '''
        Optimizer = Adam
        Loss = binary_crossentropy
        '''
        optimiser = tf.optimizers.Adam(learning_rate=0.001)
        model.compile(loss='binary_crossentropy', optimizer=optimiser, metrics=['accuracy'])
        model.summary()

        history = model.fit(x_train, y_train, validation_data=(xtest, y_test), batch_size=32, epochs=epochs)

        if not os.path.exists('models'):
            os.makedirs('models')

        print("saving model")
        model.save('models/{}_model'.format(self.soundType))

        return history

    def SelectModel(self, splits_dataset):

        if self.soundType == 's_cough':
            epochs = 10
            return self.CreateModel1(epochs, splits_dataset)

        elif self.soundType == 'h_cough':
            epochs = 11
            return self.CreateModel1(epochs,splits_dataset)

        elif self.soundType == 'F_count':
            epochs = 12
            return self.CreateModel2(epochs,splits_dataset)

        elif self.soundType == 's_breath':
            epochs = 12
            return self.CreateModel1(epochs,splits_dataset)

        elif self.soundType == 'vowel_E' or self.soundType == 'vowel_O':
            epochs=10
            return self.CreateModel2(epochs,splits_dataset)

    def ModelAccuracyGraph(self, history):

        pylab.plot(history.history['accuracy'])
        pylab.plot(history.history['val_accuracy'])
        pylab.title('model accuracy')
        pylab.ylabel('accuracy')
        pylab.xlabel('epoch')
        pylab.legend(['train', 'val'], loc='upper left')
        pylab.show()

    def ModelLossGraph(self, history):
        pylab.plot(history.history['loss'])
        pylab.plot(history.history['val_loss'])
        pylab.title('model loss')
        pylab.ylabel('loss')
        pylab.xlabel('epoch')
        pylab.legend(['train', 'val'], loc='upper left')
        pylab.show()

    def ModelClassificationReport(self):
        import sklearn.metrics
        from sklearn.metrics import confusion_matrix
        from sklearn.metrics import classification_report
        model = tf.keras.models.load_model('models/{}_model'.format(self.soundType))

        # extract the predicted probabilities
        p_pred = model.predict(self.xtest)
        p_pred = p_pred.flatten()
        # print(p_pred.round(2))
        # [1. 0.01 0.91 0.87 0.06 0.95 0.24 0.58 0.78 ...

        # extract the predicted class labels
        y_pred = np.where(p_pred > 0.5, 1, 0)
        # print(y_pred)
        # [1 0 1 1 0 1 0 1 1 0 0 0 0 1 1 0 1 0 0 0 0 ...

        cf_matrix = confusion_matrix(self.y_test, y_pred)

        # classification report for precision, recall f1-score and accuracy
        matrix = classification_report(self.y_test, y_pred)
        print('Classification report : \n', matrix)

        return cf_matrix

    def ModelConfusionMatrix(self):
        cf_matrix = self.ModelClassificationReport()
        group_names = ['True Neg', 'False Pos', 'False Neg', 'True Pos']
        group_counts = ["{0:0.0f}".format(value) for value in
                        cf_matrix.flatten()]
        group_percentages = ["{0:.2%}".format(value) for value in
                             cf_matrix.flatten() / np.sum(cf_matrix)]
        labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
                  zip(group_names, group_counts, group_percentages)]
        labels = np.asarray(labels).reshape(2, 2)
        sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')

    def ModelEvaluation(self, splits_dataset):
        history = self.SelectModel(splits_dataset)
        self.ModelAccuracyGraph(history)
        self.ModelLossGraph(history)
        self.ModelConfusionMatrix()


#
# sounds = ['s_cough', 'h_cough', 's_breath', 'F_count', 'vowel_E', 'vowel_O']
# data=[]
# for s in sounds:
#     m = SaveModel(s,'sounds_dataset')
#     x_train, y_train, xtest, y_test = m.LoadData()
#     data.append(xtest)
#     data.append(y_test)
#     dict.update({'s_cough':xtest,y_test})
#     m.ModelEvaluation(x_train, y_train, xtest, y_test)
sounds = ['s_cough', 'h_cough', 's_breath', 'F_count', 'vowel_E', 'vowel_O']
s_cough, h_cough, s_breath, F_count, vowel_O, vowel_E = ([] for i in range(6))



import itertools
def predictmodel(m):

    print(m.soundType)
    print('*****************************************************************************************************')
    model = tf.keras.models.load_model('models/{}_model'.format(m.soundType))
    # p_pred = model.predict(m.xtest[:10])
    # y_pred = np.where(p_pred > 0.5, 1, 0)
    #
    # res = list(itertools.chain(*p_pred))
    # print(",".join(map(str, res)))
    # print('predicted:',y_pred.flatten())
    res = list(itertools.chain(*m.y_test[:20]))
    print("real:",res)
    if 1 in res:
        print("yes")
        pos=res.index(1)
        print("index:",str(pos))
        pos_y=m.y_test[:20][pos]
        print("array_index_value:",str(pos_y))
        pos_x=m.xtest[:20][pos_y]
        p_pred = model.predict(pos_x)
        y_pred = np.where(p_pred > 0.5, 1, 0)
        print("prob:",str(p_pred))
        print('real:',str(pos_y))
        print('predicted:',str(y_pred))


    print('*****************************************************************************************************')





def getdata():
    # list_sounds = [s_cough]
    for s in sounds:
        print("ok")
        m = SaveModel(s, 'sounds_dataset')
        m.LoadData()
        p=predictmodel(m)
        # getPositive(p)




getdata()
# x_train, y_train, xtest, y_test=s_cough[0]
# print(len(xtest))
# print("ok")


