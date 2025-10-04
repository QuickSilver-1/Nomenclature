from sqlalchemy import Column, UUID, String, TIMESTAMP
from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    address = Column(String)
    updated_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
