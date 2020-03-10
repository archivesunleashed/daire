import pyarrow.parquet as pq
import pandas as pd
from glob import glob
import os

# Global Variable
PARQUETS_DIR = "./data/"
OUTPUT_PATH = "url_to_name.txt"


# Main Function
def main():
    removeIfExist(OUTPUT_PATH)
    output = open(OUTPUT_PATH, 'w')
    unique = set()

    t_paths = glob(os.path.join(PARQUETS_DIR, 'part-*.parquet'))
    for t_index, t_path in enumerate(t_paths):
        print(f'Reading Table {t_index + 1}/{len(t_paths)}')
        table = toPandasTable(t_path)
        for index, row in table.iterrows():
            k = row.url
            v = genImagePath(row)

            if k not in unique:
                output.write(f"{k} {v}\n")


# Utils Functions
def toPandasTable(path):
    pyarrow_table = pq.read_table(path)
    return pyarrow_table.to_pandas()


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def genImagePath(row):
    uid = row['md5']
    ext = row['filename'].split(".")[-1]
    return uid + '.' + ext


# Trigger by `python script/extract-parquets-url-to-name.py`
# Sequential Implementation outputs OUTPUT_PATH "{url} {name.ext}"
# Takes around 1m37s with 829 parquets
if __name__ == '__main__':
    main()
