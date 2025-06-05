import base64
import binascii
import exceptions
import os
import PIL
import uuid

from exceptions import ChatApiException
from io import BytesIO
from PIL import Image

WD              = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE      = os.path.join(WD, 'config.json')
IMG_RES         = os.path.join(WD, 'instance', 'images')
_MAX_H, _MAX_W  = 256, 256 # max image pixel

def init_img_res():
    if not os.path.exists(IMG_RES):
        os.makedirs(IMG_RES)

def store_pic_from_base64(pic_b64:str|None) -> str|None:
    '''
        Returns the picture uuid resource or None if pic_b64 = None.
        Raises ChatApiException
    '''
    if not pic_b64:
        return None
    try:
        resuuid = uuid.uuid4().hex
        fpath = os.path.join(IMG_RES, f'{resuuid}.jpg')
        im = Image.open(BytesIO(base64.b64decode(pic_b64)))
        if(im.height <= _MAX_H and im.width <= _MAX_W):
            im.save(fpath, 'JPEG')
        else:
            raise ChatApiException(
                exceptions.INVALID_IMG_RESOLUTION,
                extra=f'max: {_MAX_W}x{_MAX_H} pixels'
            )
    except binascii.Error as e:
        raise ChatApiException(
            exceptions.INVALID_B64_FORMAT,
            extra=str(e)
        )
    except (FileNotFoundError, PIL.UnidentifiedImageError) as e:
        raise ChatApiException(
            exceptions.UNKNOW_IMG_CRETION_PROBLEM,
            extra=str(e)
        )
    return resuuid

def get_image_path(resuuid:str) -> str|None:
    '''
        Returns path.
        raises ChatApiException
    '''
    path = os.path.join(IMG_RES, f'{resuuid}.jpg')
    if os.path.exists(path):
        return path
    else:
        raise ChatApiException(exceptions.IMG_NOT_FOUND)
