from glob import glob
import pyarrow.parquet as pq
import time
import hnswlib
from backend.model import extract_features, predict, get_label_from_prediction
import numpy as np
from backend.util import toPILImage
from random import randint

# Constants
PATH = './data/*.parquet'
TOTAL_NUM_ELEMENTS = 0
NUM_TABLES = 0
TABLES = []
TABLE_SIZES = []
HNSW = None


# Main Function
def gen_random():  # Show top 10 closest images for an entry
    global NUM_TABLES, TABLE_SIZES, TABLES, HNSW
    print('TABLES', len(TABLES))
    print('TABLE_SIZES', TABLE_SIZES)
    print('NUM_TABLES', NUM_TABLES)
    table_index = randint(0, 99999)
    row_index = randint(0, 99999)
    table_index = table_index % NUM_TABLES
    print('table_index', table_index)
    row_index = row_index % TABLE_SIZES[table_index]
    table = TABLES[table_index]
    res = {}

    try:
        row = table.loc[row_index]
        features = extract_features(row)
        prediction = predict(row)
        class_label = get_label_from_prediction(prediction)
    except Exception as e:
        print(f"Can't query row {i}. Reason: {e}")
        return gen_random()

    saveImage(row)
    print("Queried image label:", class_label)
    print("-------")

    labels, distances = HNSW.knn_query(features, k=10)
    for idx, dist in zip(labels[0], distances[0]):
        row = table.iloc[idx]
        # print('iloc', row)
        saveImage(row)
        # print("Label:", class_labels[idx])
        # print("Distance:", dist)
        print("-------")

    print('return', res)
    return res


def preprocess():
    global TOTAL_NUM_ELEMENTS, PATH, HNSW
    global TABLES, TABLE_SIZES, NUM_TABLES
    print('>> [Pre-process] starting')
    DIM = 2048
    data = np.empty((0, DIM))
    data_labels = []
    class_labels = {}

    table_index = 0
    for path in glob(PATH):
        t1 = time.time()
        table = toPandasTable(path)
        duration = time.time() - t1
        print(f"Loading table in {duration} seconds: {path}")
        num_elements = len(table)
        TOTAL_NUM_ELEMENTS += num_elements

        num_processed_elements = 0
        for i in range(num_elements):
            if i % 100 == 0:
                print(f'Loading {i}/{num_elements}')

            if i > 1000:
                break

            try:
                row = table.loc[i]
                current_vector = extract_features(row)
                prediction = predict(row)
                class_labels[i] = get_label_from_prediction(prediction)

                data = np.concatenate((data, current_vector))
                data_labels.append(i)
                num_processed_elements += 1
            except Exception as e:
                print(f">> [Pre-process] Skipping row {i}. Reason: {e}")

        # Increment Indices
        TABLES.append(table)
        print('len(TABLES)', len(TABLES))
        TABLE_SIZES.append(num_processed_elements)
        print('TABLE_SIZES', TABLE_SIZES)
        table_index += 1
        NUM_TABLES += 1
        print(f"Loaded table in {duration} seconds: {path}")

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

    print('>> [Pre-process] done')


# Utils Functions
def toPandasTable(path):
    pyarrow_table = pq.read_table(path)
    return pyarrow_table.to_pandas()

def saveImage(row):
    img = toPILImage(row)
    if img is not False:
        output_path = './img/' + row['md5'] + '.' + row['filename'].split(".")[-1]
        print('saving file to', output_path)
        img.save(output_path)
