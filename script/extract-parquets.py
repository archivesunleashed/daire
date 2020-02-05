import pyarrow.parquet as pq
from glob import glob
import base64
import io
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


# Main Function
def main():
    print('>> [Pre-process] Starting')
    output = open("./img/imgs.txt", "w")
    count = 0

    table_paths = glob('./data/part-*.parquet')
    for table_index, table_path in enumerate(table_paths):
        table = toPandasTable(table_path)
        num_elements = len(table)
        print(f'>> [Pre-process][Table][{table_index + 1}/{len(table_paths)}][Image][{num_elements}]')

        for index in range(num_elements):
            try:
                row = table.loc[index]
                if saveImage(row) is True:
                    count += 1
                    output.write(genImagePath(row) + '\n')
            except Exception as e:
                print(f">> [Pre-process] Skipping row {index}. Reason: {e}")

    print(f'<< [Pre-process] {count} images saved to img/')
    output.close()


# Utils Functions
def emptyFolder(folder_path='./img/*'):
    for path in glob(folder_path):
        os.remove(path)


def toPandasTable(path):
    pyarrow_table = pq.read_table(path)
    return pyarrow_table.to_pandas()


def genImagePath(row):
    uid = row['md5']
    ext = row['filename'].split(".")[-1]
    return uid + '.' + ext


def genImageFullPath(row):
    return './img/' + genImagePath(row)


def toPILImage(row, target_size=None):
    base64_decoded = base64.b64decode(row.bytes)
    try:
        res = Image.open(io.BytesIO(base64_decoded)).convert('RGB')
        if target_size is None:
            return res
        else:
            return res.resize(target_size)
    except Exception as e:
        print('[util][toPILImage] Failed:', e)
        return False


def saveImage(row):
    img = toPILImage(row)
    if img is False:
        return False

    output_path = genImageFullPath(row)
    img.save(output_path)
    return True


# Trigger
if __name__ == '__main__':
    emptyFolder()
    main()
