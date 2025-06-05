from flask import jsonify, Response

CHAT_API_EXCP               = ('Chat API Exception', 0, 400)
USER_NOT_FOUND              = ('User doesn\'t exist.', 1, 404)
CHANNEL_NOT_FOUND           = ('Channel doesn\'t exist.', 2, 404)
INVALID_IMG_RESOLUTION      = ('Invalid image resolution.', 3, 406)
INVALID_B64_FORMAT          = ('Invalid base64 encoding.', 4, 406)
UNKNOW_IMG_CRETION_PROBLEM  = ('Problem during image creation.', 5, 400)
IMG_NOT_FOUND               = ('Image resource not found.', 6, 404)
INVALID_TOKEN               = ('Invalid or expired token.', 7, 403)
GOOGLE_ACC_NOT_ALLOWED      = ('Google account not allowed.', 8, 403)
GOOGLE_ACC_FAILED           = ('Google account connection failure.', 9, 403)

def jsonifyFailure(excp:tuple, extra:str=None) -> Response:
    ret = {
            'errmsg'  : excp[0],
            'errcode' : excp[1],
            'extra'   : extra
    }
    return jsonify(ret), excp[2]

class ChatApiException(Exception):
    def __init__(self, excp:tuple=CHAT_API_EXCP, extra:str=None):
        super().__init__(excp[0])
        self.excp = excp
        self.extra = extra
    def jsonify(self) -> Response:
        return jsonifyFailure(self.excp, self.extra)
