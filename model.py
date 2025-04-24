import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.create_all()

class APIModelException(Exception):
    def __init__(self, msg='API Model Exception'):
        super().__init__(msg)

class Channel(db.Model):
    __tablename__ = 'channels'
    id          = db.Column(db.Integer, primary_key=True)
    uuid        = db.Column(db.String(32), default=uuid.uuid4().hex)
    alias       = db.Column(db.String(128), nullable=False)
    pic_res     = db.Column(db.String(32))
    admin_id    = db.Column(db.Integer, nullable=False)
    messages    = db.relationship('Message', backref='channel', lazy=True)
    @staticmethod
    def new(alias:str) -> 'Channel':
        chn = Channel()
        chn.alias = alias
        chn.admin_id = 1
        db.session.add(chn)
        db.session.commit()
        return chn
    def toDict(self):
        return {
            'id'        : self.id,
            'uuid'      : self.uuid,
            'alias'     : self.alias,
            'pic_res'   : self.pic_res,
            'admin_id'  : self.admin_id,
            'messages'  : [msg.toDict() for msg in self.messages]
        }

class Message(db.Model):
    __tablename__ = 'messages'
    id          = db.Column(db.Integer, primary_key=True)
    channel_id  = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    user_id     = db.Column(db.Integer, nullable=False)
    text        = db.Column(db.String(2048), nullable=False)
    creation_ts = db.Column(db.DateTime, default=func.now())    
    @staticmethod
    def new(channel_uuid:str, text:str) -> 'Message':
        chn = Channel.query.filter_by(uuid=channel_uuid).first()
        if not chn:
            raise APIModelException('Channel doesn\'t exist.')
        msg = Message()
        msg.channel_id = chn.id
        msg.user_id = 1
        msg.text = text
        db.session.add(msg)
        db.session.commit()
        return msg
    def toDict(self):
        return {
            'id'         : self.id,
            'channel_id' : self.channel_id,
            'user_id'    : self.user_id,
            'text'       : self.text,
            'creation_ts': self.creation_ts
        }
