from sqlalchemy import Column, ForeignKey, TIMESTAMP, String, Integer, Float
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nom_id = Column(Integer, ForeignKey('nomenclature.id'))
    price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(TIMESTAMP)

    nomenclature = relationship("Nomenclature", back_populates="products")
    product_in_orders = relationship("ProductInOrder", back_populates="product")
