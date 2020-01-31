import base64
import io
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


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
