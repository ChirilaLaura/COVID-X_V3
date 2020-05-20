import tensorflow as tf 
tf.compat.v1.disable_eager_execution()
#main thing that makes the whole project works(this will be here until we train another model with EAAAGERRR EXECUTIOOON LAURAAAA)

from flask import Flask, render_template, request, redirect, url_for,  Response, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
app = Flask(__name__)
#web modules activated 

from tensorflow import keras
from keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.compat.v1.keras.backend import set_session
from tensorflow.compat.v1 import get_default_graph
import matplotlib.pyplot as plt
from skimage.transform import resize
#AI modules(useless...)

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
global my_image_re
global graph
graph = get_default_graph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def image():
	if request.method == 'POST':
		file = request.files['file']
		filename = secure_filename(file.filename)
		file.save(os.path.join('Imagini_salvate', filename))
		return redirect(url_for('prediction', filename=filename))
	return render_template('index.html')

@app.route('/rezultat/')
def pleacadeaici():
	return redirect(url_for('index'))

@app.route('/rezultat/<filename>', methods=['GET', 'POST'])
def prediction(filename):
	
	if Path("Imagini_salvate/" + str(filename)).is_file() == False or os.path.getsize("Imagini_salvate/" + str(filename)) > 8 * 1000000: 
		return render_template('size_error.html') 
	else:
		my_image = plt.imread(os.path.join('Imagini_salvate', filename))
		my_image_re = resize(my_image, (64, 64, 3))
		with graph.as_default():
			set_session(sess)
			probabilities = model_xray.predict(np.array([my_image_re,]))[0,:]
			number_classes = ['This is not a X-Ray', 'This is a X-Ray']
			index = np.argsort(probabilities)
			predictions = {
				"class1" : number_classes[index[0]],
				"class2" : number_classes[index[1]],
				"prob1" : format(probabilities[index[0]] * 100, '.7f'),
				"prob2" : format(probabilities[index[1]] * 100, '.7f'), 
			}
			if(number_classes[index[1]] == 'This is a X-Ray'):
				print("FA ASTA E X-Ray")
				probabilities = model_infectat.predict(np.array([my_image_re,]))[0,:]
				number_classes = ['Probably infected', 'Probably healthy']
				index = np.argsort(probabilities)
				predictions = {
					"class1" : number_classes[index[0]],
					"class2" : number_classes[index[1]],
					"prob1" : format(probabilities[index[0]] * 100, '.7f'),
					"prob2" : format(probabilities[index[1]] * 100, '.7f'),
				}
			os.remove('Imagini_salvate/' + str(filename))
		return render_template('rezultat.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
