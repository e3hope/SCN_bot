from app.domain.repositories import MessageSender
from app.domain.entities import Message
from datetime import datetime

class NotifyUseCase:
    def __init__(self, sender: MessageSender):
        self.sender = sender

    def execute(self, chat_id: str, text: str):
        message = Message(
            chat_id=chat_id,
            text=text,
            sent_at=datetime.utcnow()
        )
        return self.sender.send_message(message)
