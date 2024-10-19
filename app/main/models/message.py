import datetime

class Message:
    def __init__(self,  message, sender, timestamp=None):
        self.message = message
        self.sender = sender
        self.timestamp = timestamp or datetime.datetime.utcnow()

    def to_json(self):
        return {
            "message": self.message,
            "sender": self.sender,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_json(data):
        """Creates a Message object from JSON data."""
        message = Message(
            message=data['message'],
            sender=data['sender']
        )
        message.timestamp = data['timestamp']  # Assuming timestamp is not recalculated
        return message