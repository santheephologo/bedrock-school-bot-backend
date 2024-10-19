import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bot(db.Model):
    __tablename__ = 'bots' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    agent_id = db.Column(db.String, nullable=False)
    alias_id = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True) 
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"<Bot {self.name}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "agent_id": self.agent_id,
            "alias_id": self.alias_id,
            "is_active": self.is_active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# MONGODB SETUP

# from mongoengine import Document, StringField, DateTimeField, BooleanField
# import datetime

# class Bot(Document):
#     meta = {'collection': 'bots'}  # Collection name in MongoDB

#     name = StringField(required=True, unique=True)
#     agent_id = StringField(required=True)
#     alias_id = StringField(required=True)
#     is_active = BooleanField(default=True) 
#     # version = IntField(default=0) 
#     created_at = DateTimeField(default=datetime.datetime.utcnow)

#     def __str__(self):
#         return f"<Bot {self.name}>"
    
#     # def save(self, *args, **kwargs):
#     #     self.version += 1
#     #     super(Client, self).save(*args, **kwargs)

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "name": self.name,
#             "agent_id": self.agent_id,
#             "alias_id": self.alias_id,
#             "is_active": self.is_active,
#             "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         }
