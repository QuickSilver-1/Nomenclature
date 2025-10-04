from fastapi import APIRouter, Depends
from uuid import UUID
from .types import AddItemRequest, OrderItemResponse
from ..repository.db.postgres.connection import get_db
from ..domain.contracts.order import OrderServiceInterface

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/{order_id}/items", response_model=OrderItemResponse)
def add_item_to_order(
    order_id: UUID,
    request: AddItemRequest,
    service: OrderServiceInterface = Depends(),
):
    item = service.add_product_to_order(order_id, request.product_id, request.quantity)
    return item

@router.get("/health")
def health_check():
    return {"status": "ok"}
