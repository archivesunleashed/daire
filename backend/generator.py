from glob import glob
import pyarrow.parquet as pq
import time
import os
from backend.model import extract_features_by_path, predict_by_path, get_label_from_prediction
import hnswlib
import numpy as np
from random import randint
from flask import url_for

# Constants
DIM = 2048
TOTAL_NUM_ELEMENTS = 0
ELEMENTS = []
DUPLICATE_COUNTS = {}
IMAGE_SOURCES = {}
HNSW = None


# Main Function
def gen_random(path, pageNumber=1):  # Show top 10 closest images for an entry
    global DIM, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    index = randint(0, TOTAL_NUM_ELEMENTS)
    class_label = None

    try:
        if path is None:
            path = ELEMENTS[index]
        else:
            path = 'img/' + path
        if os.path.exists(path) is False:
            return False, False
        features = extract_features_by_path(path)
        prediction = predict_by_path(path)
        class_label = get_label_from_prediction(prediction)
    except Exception as e:
        msg = f"Failed query {index}. Reason: {e}"
        print(msg)
        raise Exception(msg)

    res = []
    k = 20 * pageNumber
    # https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    # ef needs to be between k and dataset.size()
    ef = 2 * k
    HNSW.set_ef(ef)
    print(f"Querying {k} image labels [{class_label}]")
    labels, distances = HNSW.knn_query(features, k=k)
    srcImage = None
    for index, dist in zip(labels[0], distances[0]):
        path = ELEMENTS[index]
        if srcImage is None:
            srcImage = path[4:]
        res.append({
            'distance': str(dist),
            'duplicates': getDuplicateCountByPath(path),
            'imgPath': genExternalImageURLByPath(path),
            'refURL': genReferenceURL(path),
            'sources': getSourcesByPath(path),
        })

    return srcImage, res


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
    HNSW.load_index(f'./bin/{loadFromIndex}.bin',
                    max_elements=TOTAL_NUM_ELEMENTS)
    HNSW.set_ef(50)

    print('<< [Loading HNSW] done')


def loadMetadata(filepath='full_info.txt'):
    inputfile = open(filepath, 'r')
    for line in inputfile:
        parsed_line = line.strip().split()
        filename = parsed_line[0]
        md5 = filename.split(".")[0]
        DUPLICATE_COUNTS[md5] = int(parsed_line[1])
        IMAGE_SOURCES[md5] = parsed_line[2:]


# Utils Functions
def genExternalImageURLByPath(full_path):
    path = full_path[4:]  # get rid of "img/" prefix
    return url_for('serveImages', path=path, _external=True)


def genReferenceURL(full_path):
    path = full_path[4:]  # get rid of "img/" prefix
    return url_for('serveReact', path=path, _external=True)


def getDuplicateCountByPath(full_path):
    path = full_path[4:]  # get rid of "img/" prefix
    md5 = path.split(".")[0]
    return DUPLICATE_COUNTS[md5]


def getSourcesByPath(full_path):
    path = full_path[4:]  # get rid of "img/" prefix
    md5 = path.split(".")[0]
    return IMAGE_SOURCES[md5]
