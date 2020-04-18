# USAGE
# python train_model.py


import matplotlib
matplotlib.use("Agg")


from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import LearningRateScheduler
from keras.optimizers import SGD
from pyimagesearch.resnet import ResNet
from pyimagesearch import config
from sklearn.metrics import classification_report
from imutils import paths
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import argparse

config = tf.ConfigProto(log_device_placement=True)
config.gpu_options.allow_growth=True
session = tf.Session(config=config)


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", type=str, required=True,
	help="path to trained model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output loss/accuracy plot")
args = vars(ap.parse_args())


NUM_EPOCHS = 1500
INIT_LR = 1e-1
BS = 64

def poly_decay(epoch):
	
	maxEpochs = NUM_EPOCHS
	baseLR = INIT_LR
	power = 1.0

	
	alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power

	
	return alpha


totalTrain = len(list(paths.list_images("dataset/training")))
totalVal = len(list(paths.list_images("dataset/validation")))
totalTest = len(list(paths.list_images("dataset/testing")))

trainAug = ImageDataGenerator(
	rescale=1 / 255.0,
	rotation_range=20,
	zoom_range=0.05,
	width_shift_range=0.05,
	height_shift_range=0.05,
	shear_range=0.05,
	horizontal_flip=True,
	fill_mode="nearest")


valAug = ImageDataGenerator(rescale=1 / 255.0)


trainGen = trainAug.flow_from_directory(
	"dataset/training",
	class_mode="categorical",
	target_size=(64, 64),
	color_mode="rgb",
	shuffle=True,
	batch_size=BS)


valGen = valAug.flow_from_directory(
	"dataset/validation",
	class_mode="categorical",
	target_size=(64, 64),
	color_mode="rgb",
	shuffle=False,
	batch_size=BS)

testGen = valAug.flow_from_directory(
	"dataset/testing",
	class_mode="categorical",
	target_size=(64, 64),
	color_mode="rgb",
	shuffle=False,
	batch_size=BS)


model = ResNet.build(64, 64, 3, 2, (3, 4, 6),
	(64, 128, 256, 512), reg=0.0005)
opt = SGD(lr=INIT_LR, momentum=0.9)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

callbacks = [LearningRateScheduler(poly_decay)]
H = model.fit_generator(
	trainGen,
	steps_per_epoch=totalTrain // BS,
	validation_data=valGen,
	validation_steps=totalVal // BS,
	epochs=NUM_EPOCHS,
	callbacks=callbacks)


print("[INFO] evaluating network...")
testGen.reset()
predIdxs = model.predict_generator(testGen,
	steps=(totalTest // BS) + 1)


predIdxs = np.argmax(predIdxs, axis=1)


print(classification_report(testGen.classes, predIdxs,
	target_names=testGen.class_indices.keys()))


print("[INFO] serializing network to '{}'...".format(args["model"]))
model.save(args["model"])


N = NUM_EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")

plt.title("Training Loss and Accuracy on Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])
