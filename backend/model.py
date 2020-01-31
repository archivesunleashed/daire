from keras.applications.xception import Xception, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from keras.layers.core import Activation
from keras.models import Model
from backend.util import toPILImage
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
def predict(row):
    global MODEL

    img = toPILImage(row, target_size=(299, 299))
    if img is False:
        print('[model.py][Predict] Failed:', row)
        return False
    else:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = MODEL.predict(x)
        return preds


def extract_features(row):
    global FEATURE_MODEL

    img = toPILImage(row, target_size=(299, 299))
    if img is False:  # invalid img: e.g. index 3169 in Parquet 07
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
