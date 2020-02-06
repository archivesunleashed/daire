from glob import glob
import pyarrow.parquet as pq
import time,os,sys
from model import extract_features_by_path, predict_by_path, get_label_from_prediction
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
PROCESSED = []


# Main Function
def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def loadIndex(loadFromIndex):
    # Phase 1
    index_path= f'./bin/{loadFromIndex}.bin'
    print('>> [Pre-process] loading index from', index_path)
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW, PROCESSED
    HNSW.load_index(index_path, max_elements=TOTAL_NUM_ELEMENTS)
    
    # Phase 2
    txt_path = f'./bin/{loadFromIndex}.txt'
    inputfile = open(txt_path, 'r')
    for line in inputfile.readlines():
        line = line.strip()
        if len(line) > 0:
            PROCESSED.append(line)
    inputfile.close()



def initializeIndex():
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW, PROCESSED

    # Declaring index
    # possible options are l2, cosine or ip
    HNSW = hnswlib.Index(space='l2', dim=DIM)

    # Initing index - the maximum number of elements should be known beforehand
    # For more configuration, see: https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    HNSW.init_index(max_elements=TOTAL_NUM_ELEMENTS, ef_construction=200, M=16)


def addAndSaveIndex(data, data_labels, index):
    print('>> [Pre-process] hnswlib indexing', index)
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    # Element insertion (can be called several times):
    HNSW.add_items(data, data_labels)
    # Save Phase 1
    output_path = f'./bin/{index}.bin'
    removeIfExist(output_path)
    HNSW.save_index(output_path)
    # Save Phase 2
    output_path = f'./bin/{index}.txt'
    removeIfExist(output_path)
    output = open(output_path, "w")
    for i in PROCESSED:
        output.write(i + '\n')
    output.close()


def main(loadFromIndex=None):
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW, PROCESSED
    print('>> [Pre-process] starting')
    data = np.empty((0, DIM))
    data_labels = []

    inputfile = open(PATH, 'r')
    ELEMENTS = ['img/'+p.strip() for p in inputfile.readlines()]
    TOTAL_NUM_ELEMENTS = len(ELEMENTS)
    print(f'>> [Pre-process] Detected {TOTAL_NUM_ELEMENTS} elements')

    initializeIndex()
    if loadFromIndex is not None:
        loadIndex(loadFromIndex)
    else:
        print("Fresh Start")

    for index, path in enumerate(ELEMENTS):
        if loadFromIndex is not None and index < loadFromIndex:
            continue

        if index % 1000 == 0:
            print(f'>> [Pre-process][{index}/{TOTAL_NUM_ELEMENTS}]')

        if index % 1000 == 0 and len(data_labels) > 0:
            # save progress
            addAndSaveIndex(data, data_labels, index)
            # reset
            data = np.empty((0, DIM))
            data_labels = []

        current_vector = extract_features_by_path(path)
        prediction = predict_by_path(path)
        data = np.concatenate((data, current_vector))
        data_labels.append(index)
        PROCESSED.append(path[4:]) # remove "img/" prefix

    print('<< [Pre-process] done')


if __name__ == '__main__':
    loadFromIndex = None
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    elif len(sys.argv) == 1:
        main()
    else:
        print('Too many/few Arguments')
