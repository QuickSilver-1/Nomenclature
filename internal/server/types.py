from pydantic import BaseModel
from uuid import UUID


class AddItemRequest(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    order_id: UUID
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True
