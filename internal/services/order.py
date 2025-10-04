from fastapi import HTTPException
from ..domain.contracts.order import OrderServiceInterface
from ..domain.products_in_orders import ProductInOrder
from ..repository.order.order_repository import OrderRepository


class OrderService(OrderServiceInterface):

    def __init__(self, repository: OrderRepository):
        self.repo = repository

    def add_product_to_order(self, order_id, product_id: str, quantity: int) -> ProductInOrder:
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")

        product = self.repo.get_product_for_update(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.quantity < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")

        order = self.repo.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        pio = self.repo.get_product_in_order(order_id, product_id)
        if pio:
            self.repo.update_product_quantity_in_order(pio, quantity)
        else:
            pio = self.repo.add_product_in_order(order_id, product, quantity)

        product.quantity -= quantity

        self.repo.save_changes()
        self.repo.refresh(pio)

        return pio
