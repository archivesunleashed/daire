import threading
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
    output_path = "./img/imgs.txt"
    removeIfExist(output_path)

    threads = list()
    t_idss = list()
    saver = ImageSaver()
    total_threads = 0
    for index, table_path in enumerate(glob('./data/part-*.parquet')):
        t_idss.append(set())
        x = threading.Thread(target=processTable, args=(
            index, saver, table_path, t_idss[index], ))
        threads.append(x)
        x.start()
        # Rate Limiting
        total_threads += 1
        if total_threads == 20:
            for index, thread in enumerate(threads):
                thread.join()
            threads = list()
            total_threads = 0


    for index, thread in enumerate(threads):
        thread.join()

    ids = set()
    for t_ids in t_idss:
        ids = ids.union(t_ids)

    output = open(output_path, "w")
    for path in ids:
        output.write(path + '\n')

    output.close()
    print(f'<< [Pre-process] {len(ids)} images saved to img/')


def processTable(t_index, saver, table_path, ids):
    table = toPandasTable(table_path)
    num_elements = len(table)

    report_interval = num_elements if num_elements < 10000 else (num_elements//10)
    for index in range(num_elements):
        if index % report_interval == 0:
            print(
                f'>> [Pre-process][Table {t_index + 1}][Image][{index}/{num_elements}]')

        try:
            row = table.loc[index]
            if saver.save(row) is True:
                ids.add(genImagePath(row))
        except Exception as e:
            print(f">> [Pre-process] Skipping row {index}. Reason: {e}")

    print(
        f'<< [Pre-process][Table {t_index + 1}][Image][{num_elements}/{num_elements}]')


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


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


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


class ImageSaver:
    def __init__(self):
        self.ids = set()
        self.mutex = threading.Lock()

    def save(self, row):
        img = toPILImage(row)
        if img is False:
            return False

        output_path = genImageFullPath(row)
        self.mutex.acquire()
        visited = (output_path in self.ids)
        if visited is False:
            self.ids.add(output_path)
        self.mutex.release()

        if visited is True:
            img.save(output_path)

        return visited


# Trigger Multi Threading Version
if __name__ == '__main__':
    emptyFolder()
    main()
