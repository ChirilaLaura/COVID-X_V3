from flask import Flask, render_template, request, redirect, url_for,  Response, jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import tensorflow as tf
from tensorflow import keras
from keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import os, sys
import numpy as np
from util import base64_to_pil


app = Flask(__name__)
MODEL = 'TestAI/model.h5'
model = load_model(MODEL)
model._make_predict_function()
print("loaded")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/CovidX/Analizeaza_RMN')
def image():
    if request.method == 'POST':
            return redirect(url_for('index'))
    return render_template('file_input_covid.html')

@app.route('/CovidX/Informatii')
def info():
    if request.method == 'POST':
            return redirect(url_for('index'))
    return render_template('informatii.html')

@app.route('/CovidX/numar_cazuri')
def infected():
    return render_template('numar_cazuri.html')


if __name__ == '__main__':
    app.run(debug=True)
