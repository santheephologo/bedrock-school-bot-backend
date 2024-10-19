import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hologo(db.Model):
    __tablename__ = 'hologo'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    tkns_remaining = db.Column(db.Integer, default=0)
    tkn_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"<Hologo {self.username}>"

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "Remaining tokens": self.tkns_remaining,
            "tokens used": self.tkn_used,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# from mongoengine import Document, StringField, EmailField, DateTimeField, IntField, BooleanField
# import datetime

# class Hologo(Document):
#     meta = {'collection': 'hologo'}  # Collection name in MongoDB

#     username = StringField(required=True, unique=True, max_length=50)
#     tkns_remaining = IntField(default=0)
#     tkn_used = IntField(default=0)
#     created_at = DateTimeField(default=datetime.datetime.utcnow)

#     def __str__(self):
#         return f"<Hologo {self.username}>"

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "username": self.username,
#             "Remaining tokens": self.tkns_remaining ,
#             "tokens used": self.tkn_used ,
#             "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         }
