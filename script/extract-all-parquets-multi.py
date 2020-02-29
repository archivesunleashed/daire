import collections
import threading
import pyarrow.parquet as pq
from glob import glob
import base64
import io
import os
import os.path
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ./data/part-
IMAGE_DIR = "data/images"
IMAGELINK_DIR = "data/imagegraph"

# Main Function
def main():
    extractParquet(IMAGE_DIR, 
                  "image_info.txt", 
                  primary_key='md5',
                  collect_key='url',
                  save_ext=True,
                  save_image=True)

    extractParquet(IMAGELINK_DIR, 
                  "image_links.txt", 
                  primary_key='image_url',
                  collect_key='src',
                  save_ext=False,
                  save_image=False)


def extractParquet(base_dir, output_path, primary_key, collect_key, save_ext, save_image):
    print('>> [Pre-process] Starting')
    removeIfExist(output_path)

    threads = list()
    # ext_dicts[i] is a map from `primary_key` to image extension
    # collect_dicts[i] is a map from `primary_key` to a set of `collect_key`
    ext_dicts = list() 
    collect_dicts = list() 

    saver = ImageSaver()
    total_threads = 0
    for index, table_path in enumerate(glob(os.path.join(base_dir, 'part-*.parquet'))):
        ext_dicts.append({})
        collect_dicts.append(collections.defaultdict(set))
        x = threading.Thread(target=processTable, args=(
            index, saver, table_path, ext_dicts[index], collect_dicts[index],
            primary_key, collect_key, save_ext, save_image))
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

    # Merge results across all parquets
    
    extensions = {}
    if save_ext:
        for ext_dict in ext_dicts:
            # This overwrites existing values in extensions, but in this case we don't care
            extensions.update(ext_dict)

    collected_keys = collections.defaultdict(set)
    for collect_dict in collect_dicts:
        for k, v in d.items():
            collected_keys[k].union(v)

    with open(output_path, 'w') as output:
        for key, collected in collected_keys:
            collected_str = ' '.join(collected)
            if save_ext:
                line = f'{key} {extensions[key]} {collected_str}'
            else:
                line = f'{key} {collected_str}'

            output.write(line + '\n')

    print(f'<< [Pre-process] {len(ids)} images saved to img/')


def processTable(t_index, saver, table_path, ext_dict, collect_dict,
        primary_key, collect_key, save_ext, save_image):
    table = toPandasTable(table_path)
    num_elements = len(table)

    report_interval = num_elements if num_elements < 10000 else (num_elements//10)
    for index in range(num_elements):
        if index % report_interval == 0:
            print(
                f'>> [Pre-process][Table {t_index + 1}][Image][{index}/{num_elements}]')

        try:
            row = table.loc[index]
            dict_key = row[primary_key]

            collect_dict[dict_key].add(row[collect_key])

            if save_ext:
                ext_dict[dict_key] = extensionForRow(row)

            if save_image and saver.save(row):
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


def extensionForRow(row):
    return row['filename'].split(".")[-1]

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
