import io
import os
import sys
import uuid
from mimetypes import guess_extension

import numpy as np
import requests
import soundfile
from flask import Flask, request, jsonify, json
import random
import tensorflow as tf
import librosa as librosa
from werkzeug.utils import redirect

app = Flask(__name__)

covid_prob = []
s_cough = tf.keras.models.load_model('../models/{}_model'.format('s_cough'))
h_cough=tf.keras.models.load_model('../models/{}_model'.format('h_cough'))
s_breath=tf.keras.models.load_model('../models/{}_model'.format('s_breath'))
vowel_E=tf.keras.models.load_model('../models/{}_model'.format('vowel_E'))
F_count=tf.keras.models.load_model('../models/{}_model'.format('F_count'))
vowel_O=tf.keras.models.load_model('../models/{}_model'.format('vowel_O'))


def pad_trunc(aud, max_ms):
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


def preprocess(file_name):
    reaud, sr = librosa.load(file_name, duration=4)
    audio = pad_trunc(reaud, 4000)
    mel = librosa.feature.melspectrogram(y=audio, sr=sr)
    s_db = librosa.power_to_db(mel, ref=np.max)
    audio_reshaped = s_db.reshape(1, s_db.shape[0], s_db.shape[1], 1)
    return audio_reshaped


def prediction(model, audio_reshaped):
    predicted_output = model.predict(audio_reshaped)
    y_pred = np.where(predicted_output > 0.5, 'positive', 'negative')
    print(predicted_output, y_pred, file=sys.stderr)
    data = {
        "covid_status": json.dumps(str(y_pred[0][0])),
        "probability": json.dumps(float(predicted_output[0][0]))}
    covid_prob.append(float(data['probability']))
    os.remove("demo.wav")
    print(data, file=sys.stderr)
    return data


@app.route("/shallow_breath", methods=['post'])
def form():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_breath'))
    response= prediction(s_breath, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
#
@app.route("/shallow_cough", methods=['post'])
def predictshallow_cough():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_cough'))
    response= prediction(s_cough, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



@app.route("/heavy_cough", methods=['post'])
def predictheavy_cough():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_cough'))
    response= prediction(h_cough, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    #
    return response



@app.route("/vowel_E", methods=['post'])
def predictvowel_E():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_cough'))
    response= prediction(vowel_E, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    #
    return response



@app.route("/vowel_O", methods=['post'])
def predictvowel_O():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_cough'))
    response= prediction(vowel_O, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    #
    return response

@app.route("/fast_counting", methods=['post'])
def predictfastCounting():
    audio_file = request.files["file"]
    print(audio_file)
    audio_file.save('demo.wav')
    audio_reshaped = preprocess('demo.wav')
    # model = tf.keras.models.load_model('models/{}_model'.format('s_cough'))
    response= prediction(F_count, audio_reshaped)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    #
    return response




@app.route("/results")
def predict_all():
    print(covid_prob)
    for i in covid_prob:
        float(i)
    total_prob = sum(covid_prob)

    print(total_prob)
    average_predict = total_prob / len(covid_prob)
    if average_predict > 0.5:
        prediction = 'Positive'
    else:
        prediction = 'Negative'
    data = {"covid_status": prediction,
            "probability": json.dumps(float(average_predict))}
    covid_prob.clear()
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=False)
