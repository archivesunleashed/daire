from keras.applications.xception import Xception, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from keras.layers.core import Activation
from keras.models import Model
from backend.util import toPILImageFromRow, toPILImageFromPath
from PIL import Image
import numpy as np
import time

# Constants
LAYER_NAME = "avg_pool"


# Setup
t1 = time.time()
MODEL = Xception(weights='imagenet')
FEATURE_MODEL = Model(
    inputs=MODEL.input,
    outputs=MODEL.get_layer(LAYER_NAME).output)
duration = time.time() - t1
print(f"Loaded model in {duration} seconds")


# Main Function
def predict_by_path(path):
    global MODEL

    img = toPILImageFromPath(path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = MODEL.predict(x)
    return preds


def predict_by_row(row):
    global MODEL

    img = toPILImageFromRow(row, target_size=(299, 299))
    if img is False:
        print('[model.py][predict_by_row] Failed:', row)
        return False
    else:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = MODEL.predict(x)
        return preds


def extract_features_by_path(path):
    global FEATURE_MODEL

    img = toPILImageFromPath(path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return FEATURE_MODEL.predict(x)


def extract_features_by_row(row):
    global FEATURE_MODEL

    img = toPILImageFromRow(row, target_size=(299, 299))
    if img is False:
        print('[model.py][Feature Extraction] Failed:', row)
        return False
    else:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        return FEATURE_MODEL.predict(x)


# Utils Functions
def get_label_from_prediction(pred):
    result = decode_predict(pred, top=1)
    return result[0][1]


def decode_predict(preds, top=3):
    return decode_predictions(preds, top=top)[0]
