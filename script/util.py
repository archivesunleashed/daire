import base64
import io
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def toPILImageFromRow(row, target_size=None):
    base64_decoded = base64.b64decode(row.bytes)
    try:
        res = Image.open(io.BytesIO(base64_decoded)).convert('RGB')
        if target_size is None:
            return res
        else:
            return res.resize(target_size)
    except Exception as e:
        print('[util][toPILImageFromRow] Failed:', e)
        return False


def toPILImageFromPath(path, target_size=None):
    try:
        img = Image.open(path).convert('RGB')
        img = img.resize((299, 299))
    except Exception as e:
        print('[util][toPILImageFromPath] Failed:', e)
        raise Exception('[util][toPILImageFromPath] Failed:', e)

    return img
