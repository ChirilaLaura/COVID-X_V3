from flask import Flask, render_template, request
#from keras.models import load_model
#from keras.backend import set_session
#from skimage.transfrom import resize
#import tensorflow as tf
import numpy as np
import os, requests

#global sess
#sess = tf.Session()
#set_session(sess)
#model = tf.keras.models.load_model('model.h5', custom_objects={'Adam': lambda **kwargs: hvd.DistributedOptimizer(keras.optimizers.Adam(**kwargs))})
#global graph
#graph = tf.get_default_graph()



app = Flask(__name__)

@app.route('/')
def index():
    #css(flips cards, style), home.html
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
'''
@app.route('/mri_scan', methods=['POST'])
def request_fisier():
    form = request.form
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template("<<fisier_request.html>>")
'''

if __name__ == '__main__':
    app.run(debug=True)
