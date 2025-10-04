from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class Nomenclature(Base):
    __tablename__ = 'nomenclature'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('nomenclature.id'), nullable=True)
    name = Column(String, unique=True)
    is_leaf = Column(Boolean)
    created_at = Column(TIMESTAMP)

    children = relationship("Nomenclature", remote_side=[id])
    products = relationship("Product", back_populates="nomenclature")
