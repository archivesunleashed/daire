from glob import glob
import pyarrow.parquet as pq
import time,os
from backend.model import extract_features_by_path, predict_by_path, get_label_from_prediction
import hnswlib
import numpy as np
from random import randint
from flask import url_for

# Constants
DIM = 2048
TOTAL_NUM_ELEMENTS = 0
ELEMENTS = []
HNSW = None


# Main Function
def gen_random(path):  # Show top 10 closest images for an entry
    global DIM, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    index = randint(0, TOTAL_NUM_ELEMENTS)
    class_label = None

    try:
        if path is None:
            path = ELEMENTS[index]
        else:
            path = 'img/' + path
        if os.path.exists(path) is False:
            return False
        features = extract_features_by_path(path)
        prediction = predict_by_path(path)
        class_label = get_label_from_prediction(prediction)
    except Exception as e:
        msg = f"Failed query {index}. Reason: {e}"
        print(msg)
        raise Exception(msg)

    print("Queried image label:", class_label)

    res = []
    labels, distances = HNSW.knn_query(features, k=20)
    for index, dist in zip(labels[0], distances[0]):
        path = ELEMENTS[index]
        res.append({
            'distance': str(dist),
            'imgPath': genExternalImageURLByPath(path),
            'refURL': genReferenceURL(path),
        })
        # print("Label:", class_labels[idx])

    return res


def loadHNSW(loadFromIndex=131490):
    if loadFromIndex is None:
        raise Exception("Invalid index to load from")

    global DIM, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    print('>> [Loading HNSW] starting')

    inputfile = open(f'./bin/{loadFromIndex}.txt', 'r')
    ELEMENTS = ['img/'+p.strip() for p in inputfile.readlines()]
    TOTAL_NUM_ELEMENTS = len(ELEMENTS)
    print(f'>> [Loading HNSW] Detected {TOTAL_NUM_ELEMENTS} elements')

    print('>> [Loading HNSW] hnswlib indexing')
    HNSW = hnswlib.Index(space='l2', dim=DIM)
    HNSW.load_index(f'./bin/{loadFromIndex}.bin', max_elements=TOTAL_NUM_ELEMENTS)
    HNSW.set_ef(50)

    print('<< [Loading HNSW] done')


# Utils Functions
def genExternalImageURLByPath(full_path):
    path = full_path[4:] # get rid of "img/" prefix
    return url_for('serveImages', path=path, _external=True)

def genReferenceURL(full_path):
    path = full_path[4:] # get rid of "img/" prefix
    return url_for('serveReact', path=path, _external=True)
