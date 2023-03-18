import uuid

from sqlalchemy import Column, String, Enum, DateTime, func, Text, ForeignKey

from sqlalchemy import UUID

from src.db import Base


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    text = Column(String(10000), nullable=False)

    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'

