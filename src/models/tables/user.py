import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text

from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from src.db import Base

from src.models.enums.role import UserRole

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    avatar_id = Column(UUID(as_uuid=True), nullable=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    patronymic = Column(String(64), nullable=True)
    department = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    chats = relationship("models.tables.user_chat.UserChatAssociation", back_populates="user")
    messages = relationship("models.tables.message.Message", back_populates="owner")

    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
