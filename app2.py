from flask import Flask, render_template, request, redirect, url_for,  Response, jsonify
from werkzeug.utils import secure_filename
# web site modules
app = Flask(__name__)

import tensorflow as tf
from tensorflow import keras
from keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.applications import imagenet_utils
from keras.backend import set_session
import matplotlib.pyplot as plt
from skimage.transform import resize

#model modules

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import operator
#utilities modules

global sess
sess = tf.compat.v1.Session()
set_session(sess)

global model_infectat
model_infectat = load_model('Modeleh5/model_covid.h5')
global model_xray
model_xray = load_model('Modeleh5/model_xray.h5')

global graph
graph = tf.get_default_graph()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/Analizeaza_RMN/', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('Imagini_salvate', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('file_input_covid.html')


@app.route('/Rezultat/<filename>')
def prediction(filename):
    my_image = plt.imread(os.path.join('Imagini_salvate', filename))
    my_image_re = resize(my_image, (64, 64, 3))

    with graph.as_default():
        set_session(sess)
        probabilities = model_xray.predict(np.array([my_image_re,]))[0,:]
        number_classes = ['Other', 'Xray']
        index = np.argsort(probabilities)
        predictions = {
            "class1" : number_classes[index[0]],
            "class2" : number_classes[index[1]],
            "prob1" : probabilities[index[0]],
            "prob2" : probabilities[index[1]],
        }

        if(number_classes[index[1]] == 'Xray'):
            print("FA ASTA E XRAY")
            probabilities = model_xray.predict(np.array([my_image_re,]))[0,:]
            number_classes = ['Sanatos' ,'Infectat']
            index = np.argsort(probabilities)
            predictions = {
                "class1" : number_classes[index[0]],
                "class2" : number_classes[index[1]],
                "prob1" : probabilities[index[0]],
                "prob2" : probabilities[index[1]],
            }
            return render_template('rezultat.html', predictions=predictions)

    print(predictions)
    return render_template('rezultat.html', predictions=predictions)

@app.route('/Informatii/')
def info():
    return render_template('informatii.html')

@app.route('/Numar_Cazuri/')
def infected():
    return render_template('numar_cazuri.html')


if __name__ == '__main__':
    app.run(debug=True)
