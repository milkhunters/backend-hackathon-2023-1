from sqlalchemy.orm import relationship

from src.db import Base

from sqlalchemy import Column, ForeignKey

from sqlalchemy import UUID


class UserChatAssociation(Base):
    __tablename__ = "user_chat"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, primary_key=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False, primary_key=True)

    user = relationship("models.tables.user.User", back_populates="chats")
    chat = relationship("models.tables.chat.Chat", back_populates="users")
