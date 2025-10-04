from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class ProductInOrder(Base):
    __tablename__ = 'products_in_orders'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='product_in_orders')
