import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # bots = db.relationship('ClientBot', backref='client', lazy=True)

    def __str__(self):
        return f"<Client {self.username}>"

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# from mongoengine import Document, StringField, EmailField, DateTimeField, IntField, BooleanField, ListField,  EmbeddedDocument, EmbeddedDocumentField
# import datetime
# import datetime

# class ClientBot(EmbeddedDocument):
#     id = StringField(required=True)
#     name = StringField(required=True, max_length=100)
#     tkns_remaining = IntField(default=0)
#     tkns_used = IntField(default=0)
    
# class Client(Document):
#     meta = {'collection': 'clients'}  # Collection name in MongoDB

#     username = StringField(required=True, unique=True, max_length=50)
#     email = EmailField(required=True)
#     password = StringField(required=True)
#     first_name = StringField(max_length=50)
#     last_name = StringField(max_length=50)
#     bots = ListField(EmbeddedDocumentField(ClientBot), default=list)  
#     # tkns_remaining = IntField(default=0)
#     # tkns_used = IntField(default=0)
#     is_active = BooleanField(default=True) 
#     # version = IntField(default=0) 
#     created_at = DateTimeField(default=datetime.datetime.utcnow)

#     def __str__(self):
#         return f"<Client {self.username}>"
    
#     # def save(self, *args, **kwargs):
#     #     self.version += 1
#     #     super(Client, self).save(*args, **kwargs)

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "username": self.username,
#             "email": self.email,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "bots": [
#                 {
#                     "id":bot.id,
#                     "name": bot.name,
#                     "tkns_remaining": bot.tkns_remaining,
#                     "tkns_used": bot.tkns_used
#                 } for bot in self.bots
#             ], 
#             "is_active": self.is_active,
#             "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         }
