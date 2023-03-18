import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text

from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from src.db import Base


class Chat(Base):
    __tablename__ = "chats"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    messages = relationship("models.tables.message.Message", back_populates="chat")
    users = relationship("models.tables.user_chat.UserChatAssociation", back_populates="chat")

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
