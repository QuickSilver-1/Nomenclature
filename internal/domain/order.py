from sqlalchemy import Column, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .order_status import OrderStatusEnum


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    status = Column(Enum(OrderStatusEnum, name='order_status'))
    created_at = Column(TIMESTAMP)

    items = relationship(
        'ProductInOrder',
        back_populates='order',
        cascade="all, delete-orphan"
    )
