import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text, ForeignKey

from sqlalchemy import UUID
from sqlalchemy.orm import relationship

from src.db import Base


class File(Base):
    __tablename__ = "files"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(255), default="file")
    file_id = Column(UUID(as_uuid=True))

    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    message = relationship("models.tables.message.Message", back_populates="files")

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
