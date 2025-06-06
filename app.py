import datetime
import exceptions
import fnmatch
import json
import jwt
import time

from exceptions import ChatApiException, jsonifyFailure
from flask import (
    Flask, render_template, jsonify, request,
    abort, send_file, Response
)
from flask_simple_captcha import CAPTCHA
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
from model import (
    Channel, Message, init_model, User
)
from res import (
    CONFIGFILE, init_img_res, 
    get_image_path
)

# --- app

def create_app():
    _app = Flask(__name__)
    with _app.app_context():
        with open(CONFIGFILE, 'r', encoding='utf-8') as cfgfile:
            cfgdict = json.load(cfgfile)
            _app.config.update(cfgdict)
        init_model(_app)
        init_img_res()
        _simple_captcha = CAPTCHA(config={
            'SECRET_CAPTCHA_KEY':_app.config['SECRET_CAPTCHA_KEY']
        })
        _simple_captcha.init_app(_app)
    return _app, _simple_captcha
app, simple_captcha = create_app()

# --- utils

def auth_required(f):
    @wraps(f)
    def inject(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            abort(400)
        try:
            token = auth_header.split('Bearer ')[1]
            api_token = jwt.decode(token, 
                                   app.config['SECRET_KEY'], 
                                   algorithms=['HS256'])
            return f(user=User.fetch(api_token['uuid']), *args, **kwargs)
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidTokenError):
            return jsonifyFailure(exceptions.INVALID_TOKEN)
        except ChatApiException as e:
            return e.jsonify()
    return inject

def email_allowed(email:str):
    if 'RESTRICT_TO' not in app.config or\
        not app.config['RESTRICT_TO'] or\
        type(app.config['RESTRICT_TO']) != list:
            return True
    for rule in app.config['RESTRICT_TO']:
        if fnmatch.fnmatch(email, rule):
            return True
    return False

# --- routes.pages

@app.context_processor
def inject_request():
    return dict(request=request)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', timenow=int(time.time()))

@app.route('/invite/<string:uuid>', methods=['GET', 'POST'])
def channel_invitation(uuid):
    if request.method == 'GET':
        return render_template('invite.html', captcha=simple_captcha.create(), 
                               timenow=int(time.time()))
    if request.method == 'POST':
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if not simple_captcha.verify(c_text, c_hash):
            return render_template('invite.html', captcha=simple_captcha.create(), 
                                   wrong_captcha=True, timenow=int(time.time()))
        try:
            chn = Channel.fetch(uuid)
            return render_template('invite.html', uuid=uuid, channel_name=chn.alias, 
                                   timenow=int(time.time()))
        except ChatApiException:
            return render_template('invite.html', not_exist=True, 
                                   timenow=int(time.time())), 404

# --- routes.auth

@app.route('/token/is_valid', methods=['GET'])
@auth_required
def is_token_valid(user:User):
    return Response(status=200)

@app.route('/auth/google', methods=['POST'])
def google_login():
    data = request.get_json()
    if 'id_token' not in data:
        abort(400)
    try:
        idinfo = id_token.verify_oauth2_token(data['id_token'], 
                                            requests.Request(),
                                            app.config['GOOGLE_CLIENT_ID'])
        email = idinfo['email']
        if not email_allowed(email):
            return jsonifyFailure(exceptions.GOOGLE_ACC_NOT_ALLOWED)
        usr = User.get_user_or_none(email)
        if not usr:
            name = idinfo['name']
            usr = User.new(name, email)
        tdelta = app.config['TOKEN_EXP_DHM']
        api_token = jwt.encode({
            'uuid': usr.uuid,
            'exp': datetime.datetime.now(datetime.timezone.utc) + \
                    datetime.timedelta(days=tdelta[0], hours=tdelta[1], minutes=tdelta[2])
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'user': usr.toDict(sensitive=True), 'token': api_token})
    except GoogleAuthError as e:
        return jsonifyFailure(exceptions.GOOGLE_ACC_FAILED, str(e))

# --- routes.api

@app.route('/channels/<string:uuid>', methods=['GET'])
@auth_required
def get_channel(user:User, uuid:str):
    try:
        chn = Channel.fetch(uuid)
        return jsonify(chn.toDict())
    except ChatApiException as e:
        return e.jsonify()

@app.route('/img/<string:img_res>', methods=['GET'])
@auth_required
def get_img(user:User, img_res:str):
    try:
        return send_file(get_image_path(img_res))
    except ChatApiException as e:
        return e.jsonify()

@app.route('/channels/new', methods=['POST'])
@auth_required
def new_channel(user:User):
    chndict = request.get_json()
    if (not 'alias' in chndict):
        abort(400)
    chn = Channel.new(
        chndict['alias'], user,
        chndict['img_res'] if 'img_res' in chndict else None
    )
    return jsonify(chn.toDict())

@app.route('/messages/new', methods=['POST'])
@auth_required
def new_message(user:User):
    msgdict = request.get_json()
    if (not 'text' in msgdict) and\
       (not 'channel_uuid' in msgdict):
        abort(400)
    try:
        msg = Message.new(msgdict['channel_uuid'], 
                          msgdict['text'],
                          user)
    except ChatApiException as e:
        return e.jsonify()
    return jsonify(msg.toDict())
