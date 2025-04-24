from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.create_all()

class Message(db.Model):
    __tablename__ = 'messages'
    id          = db.Column(db.Integer, primary_key=True)
    channel_id  = db.Column(db.Integer, nullable=False)
    user_id     = db.Column(db.Integer, nullable=False)
    text        = db.Column(db.String(2048), nullable=False)
    creation_ts = db.Column(db.DateTime, default=func.now())    
    @staticmethod
    def new(text:str) -> 'Message':
        msg = Message()
        msg.channel_id = 1
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
