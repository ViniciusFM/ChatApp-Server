import json
import os
from flask import (
    Flask, render_template, jsonify, request,
    abort
)
from functools import wraps
from model import Message, init_db

WD          = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE  = os.path.join(WD, 'config.json')

# --- app

def create_app():
    _app = Flask(__name__)
    with _app.app_context():
        with open(CONFIGFILE, 'r', encoding='utf-8') as cfgfile:
            cfgdict = json.load(cfgfile)
            _app.config.update(cfgdict)
        init_db(_app)
    return _app
app = create_app()

# --- utils

def auth_required(f):
    @wraps(f)
    def inject(*args, **kwargs):
        token = request.headers.get('Token-Auth')
        if token != app.config['SECRET_KEY']:
            abort(400)
        return f(*args, **kwargs)
    return inject

# --- routes

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/messages/new', methods=['POST'])
@auth_required
def new_message():
    msgdict = request.get_json()
    if (not 'text' in msgdict):
        abort(400)
    msg = Message.new(msgdict['text'])
    return jsonify(msg.toDict())

@app.route('/messages', methods=['GET'])
@auth_required
def get_messages():
    ret = []
    for msg in Message.query.all():
        ret.append(msg.toDict())
    return jsonify(ret)
