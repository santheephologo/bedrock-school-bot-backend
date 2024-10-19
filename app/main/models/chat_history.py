import datetime
import uuid
from main.models.message import Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

db = SQLAlchemy()

class ChatHistory(db.Model):
    __tablename__ = 'chat_histories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # messages = db.Column(db.JSON, nullable=False, default=[])
    messages = db.Column(MutableList.as_mutable(JSON), nullable=False, default=[])
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    def __str__(self):
        return f"ChatHistory(id={self.id}, session_id={self.session_id})"

    def to_json(self):
        return {
            "id": str(self.id),
            "session_id": self.session_id,
            "messages": [message for message in self.messages] ,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def from_json(data):
        """Helper method to create a ChatHistory object from JSON data."""
        created_at = datetime.datetime.strptime(data['created_at'], "%Y-%m-%d %H:%M:%S")
        chat_history = ChatHistory(
            session_id=data['session_id'],
            messages=data['messages'],
            created_at = created_at
        )
        # Rebuild the messages list from JSON
        chat_history.messages = [Message.from_json(m) for m in data['messages']]
        return chat_history
    
# from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField
# import datetime
# import uuid

# class Message(EmbeddedDocument):
#     message = StringField(required=True)
#     timestamp = DateTimeField(default=datetime.datetime.utcnow)
#     sender = StringField(required=True, choices=["User", "Bot"])

#     def to_json(self):
#         return {
#             "message": self.message,
#             "timestamp": self.timestamp.isoformat(),
#             "sender": self.sender
#         }

# class ChatHistory(Document):
#     meta = {'collection': 'chatHistory'}  # Collection name in MongoDB
    
#     session_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
#     username = StringField(required=True, max_length=100)  # Increased max_length to accommodate date and time
#     messages = ListField(EmbeddedDocumentField(Message))

#     def __str__(self):
#         return f"{self.username}>"

#     def add_message(self, message, sender):
#         print("running add_message")
#         message = Message(message=message, sender=sender)
#         self.messages.append(message)
#         self.save()

#     def to_json(self):
#         return {
#             "id": str(self.id),
#             "session_id": self.session_id,
#             "username": self.username,
#             "messages": [message.to_json() for message in self.messages]
#         }
