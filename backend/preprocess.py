from glob import glob
import pyarrow.parquet as pq
import time
from backend.model import extract_features_by_path, predict_by_path, get_label_from_prediction
import hnswlib
import numpy as np
from random import randint
from flask import url_for

# Constants
DIM = 2048
PATH = './img/imgs.txt'
TOTAL_NUM_ELEMENTS = 0
ELEMENTS = []
HNSW = None


# Main Function
def gen_random():  # Show top 10 closest images for an entry
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    index = randint(0, TOTAL_NUM_ELEMENTS)
    class_label = None

    try:
        path = ELEMENTS[index]
        features = extract_features_by_path(path)
        prediction = predict_by_path(path)
        class_label = get_label_from_prediction(prediction)
    except Exception as e:
        print(f"Failed query {index}. Reason: {e}")

    print("Queried image label:", class_label)

    res = []
    labels, distances = HNSW.knn_query(features, k=10)
    for index, dist in zip(labels[0], distances[0]):
        path = ELEMENTS[index]
        res.append({
            'distance': str(dist),
            'imgPath': genExternalImageURLByPath(path)
        })
        # print("Label:", class_labels[idx])

    return res


def preprocess():
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    print('>> [Pre-process] starting')
    data = np.empty((0, DIM))
    data_labels = []

    inputfile = open(PATH, 'r')
    ELEMENTS = ['img/'+p.strip() for p in inputfile.readlines()]
    TOTAL_NUM_ELEMENTS = len(ELEMENTS)
    print(f'>> [Pre-process] Detected {TOTAL_NUM_ELEMENTS} elements')

    for index, path in enumerate(ELEMENTS):
        if index % 100 == 0:
            print(f'>> [Pre-process][{index}/{TOTAL_NUM_ELEMENTS}]')

        current_vector = extract_features_by_path(path)
        prediction = predict_by_path(path)
        data = np.concatenate((data, current_vector))
        data_labels.append(index)

    print('>> [Pre-process] hnswlib indexing')
    # Declaring index
    # possible options are l2, cosine or ip
    HNSW = hnswlib.Index(space='l2', dim=DIM)

    # Initing index - the maximum number of elements should be known beforehand
    # For more configuration, see: https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    HNSW.init_index(max_elements=TOTAL_NUM_ELEMENTS, ef_construction=200, M=16)

    # Element insertion (can be called several times):
    HNSW.add_items(data, data_labels)

    # Controlling the recall by setting ef:
    HNSW.set_ef(50)  # ef should always be > k

    print('<< [Pre-process] done')


# Utils Functions
def genExternalImageURLByPath(full_path):
    path = full_path[4:] # get rid of "img/" prefix
    return url_for('serveImages', path=path, _external=True)
