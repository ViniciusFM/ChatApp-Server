import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from res import (
    store_pic_from_base64,
    APIResException
)

db = SQLAlchemy()

def init_model(app):
    db.init_app(app)
    db.create_all()

def get_uuid() -> str:
    return uuid.uuid4().hex

class APIModelException(Exception):
    def __init__(self, msg='API Model Exception'):
        super().__init__(msg)

class User(db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    uuid        = db.Column(db.String(32), default=get_uuid, unique=True)
    name        = db.Column(db.String(256))
    email       = db.Column(db.String(256), unique=True)
    channels    = db.relationship('Channel', lazy=True)
    @staticmethod
    def new(name:str, email:str) -> 'User':
        usr = User()
        usr.name = name
        usr.email = email
        db.session.add(usr)
        db.session.commit()
        return usr
    @staticmethod
    def get_user_or_none(email:str) -> 'User|None':
        return User.query.filter_by(email=email).first()
    @staticmethod
    def fetch(uuid:str) -> 'User':
        usr = User.query.filter_by(uuid=uuid).first()
        if not usr:
            raise APIModelException('User doesn\'t exist.')
        return usr
    def toDict(self, sensitive=False):
        ret = {
            'id'        : self.id,
            'name'      : self.name,
        }
        if sensitive:
            ret['uuid']     = self.uuid
            ret['email']    = self.email
            ret['channels'] = [chn.toDict() for chn in self.channels]
        return ret

class Channel(db.Model):
    __tablename__ = 'channels'
    id          = db.Column(db.Integer, primary_key=True)
    uuid        = db.Column(db.String(32), default=get_uuid, unique=True)
    alias       = db.Column(db.String(128), nullable=False)
    img_res     = db.Column(db.String(32), unique=True)
    admin_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    messages    = db.relationship('Message', backref='channel', lazy=True)
    admin       = db.relationship('User', lazy=True, viewonly=True)
    @staticmethod
    def new(alias:str, admin:str|User, img_b64:str|None = None) -> 'Channel':
        adm = User.fetch(admin) if type(admin) == str else admin
        chn = Channel()
        chn.alias = alias
        chn.admin_id = adm.id
        try:
            chn.img_res = store_pic_from_base64(img_b64)
        except APIResException as e:
            raise APIModelException(str(e))
        db.session.add(chn)
        db.session.commit()
        return chn
    @staticmethod
    def fetch(uuid:str) -> 'Channel':
        chn = Channel.query.filter_by(uuid=uuid).first()
        if not chn:
            raise APIModelException('Channel doesn\'t exist.')
        return chn
    def toDict(self):
        return {
            'id'        : self.id,
            'uuid'      : self.uuid,
            'alias'     : self.alias,
            'img_res'   : self.img_res,
            'admin'     : self.admin.toDict(),
            'messages'  : [msg.toDict() for msg in self.messages]
        }

class Message(db.Model):
    __tablename__ = 'messages'
    id          = db.Column(db.Integer, primary_key=True)
    channel_id  = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text        = db.Column(db.String(2048), nullable=False)
    creation_ts = db.Column(db.DateTime, default=func.now())
    user        = db.relationship('User', lazy=True)
    @staticmethod
    def new(channel:str|Channel, text:str, user:str|User) -> 'Message':
        chn = Channel.fetch(channel) if type(channel) == str else channel
        usr = User.fetch(user) if type(user) == str else user
        msg = Message()
        msg.channel_id = chn.id
        msg.user_id = usr.id
        msg.text = text
        db.session.add(msg)
        db.session.commit()
        return msg
    def toDict(self):
        return {
            'id'         : self.id,
            'channel_id' : self.channel_id,
            'text'       : self.text,
            'creation_ts': self.creation_ts,
            'user'       : self.user.toDict()
        }
