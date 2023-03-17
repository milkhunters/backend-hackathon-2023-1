import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text, Boolean, ForeignKey

from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from src.db import Base


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String(1024), nullable=True)

    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    chat = relationship("models.tables.chat.Chat", back_populates="messages")

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("models.tables.user.User", back_populates="messages")

    files = relationship("models.tables.file.File", back_populates="message")
    is_read = Column(Boolean, default=False)

    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
