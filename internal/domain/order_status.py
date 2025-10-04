import enum


class OrderStatusEnum(enum.Enum):
    created = 'created'
    paid = 'paid'
    delivered = 'delivered'