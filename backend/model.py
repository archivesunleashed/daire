from keras.applications.xception import Xception, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from keras.layers.core import Activation
from keras.models import Model
from backend.util import toPILImageFromRow, toPILImageFromPath
from PIL import Image
import numpy as np
import tensorflow as tf
import time

# Constants
LAYER_NAME = "avg_pool"


# Setup
t1 = time.time()
MODEL = Xception(weights='imagenet')
graph1 = tf.get_default_graph()
FEATURE_MODEL = Model(
    inputs=MODEL.input,
    outputs=MODEL.get_layer(LAYER_NAME).output)
graph2 = tf.get_default_graph()
duration = time.time() - t1
print(f"Loaded model in {duration} seconds")


# Main Function
def predict_by_path(path):
    global MODEL, graph1

    img = toPILImageFromPath(path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    with graph1.as_default():
        return MODEL.predict(x)


def predict_by_row(row):
    global MODEL, graph1

    img = toPILImageFromRow(row, target_size=(299, 299))
    if img is False:
        print('[model.py][predict_by_row] Failed:', row)
        return False
    else:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        with graph1.as_default():
            return MODEL.predict(x)


def extract_features_by_path(path):
    global FEATURE_MODEL, graph2

    img = toPILImageFromPath(path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    with graph2.as_default():
        return FEATURE_MODEL.predict(x)


def extract_features_by_row(row):
    global FEATURE_MODEL, graph2

    img = toPILImageFromRow(row, target_size=(299, 299))
    if img is False:
        print('[model.py][Feature Extraction] Failed:', row)
        return False
    else:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        with graph2.as_default():
            return FEATURE_MODEL.predict(x)


# Utils Functions
def get_label_from_prediction(pred):
    result = decode_predict(pred, top=1)
    return result[0][1]


def decode_predict(preds, top=3):
    return decode_predictions(preds, top=top)[0]
