import datetime
from main.models.bot import Bot
from main.models.client import Client
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ClientBot(db.Model):
    __tablename__ = 'client_bots'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    # bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    bot_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    tkns_remaining = db.Column(db.Integer, default=0)
    tkns_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # # Define relationships
    # client = db.relationship(Client, backref='client_bots')  
    # bot = db.relationship(Bot, backref='client_bots')   
            
    def to_json(self):
        return {
            "id": self.bot_id,
            "client_id":self.client_id,
            "bot_id":self.bot_id,
            "name": self.name,
            "tkns_remaining": self.tkns_remaining,
            "tkns_used": self.tkns_used,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
