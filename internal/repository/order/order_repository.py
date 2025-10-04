from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from ...domain import product, order, products_in_orders


class OrderRepository(ABC):

    @abstractmethod
    def get_product_for_update(self, product_id: str) -> Optional[product.Product]:
        pass

    @abstractmethod
    def get_order(self, order_id: UUID) -> Optional[order.Order]:
        pass

    @abstractmethod
    def get_product_in_order(self, order_id: UUID, product_id: str) -> Optional[products_in_orders.ProductInOrder]:
        pass

    @abstractmethod
    def add_product_in_order(self, order_id: UUID, product: product.Product, quantity: int) -> products_in_orders.ProductInOrder:
        pass

    @abstractmethod
    def update_product_quantity_in_order(self, pio: products_in_orders.ProductInOrder, add_qty: int) -> products_in_orders.ProductInOrder:
        pass

    @abstractmethod
    def save_changes(self) -> None:
        pass

    @abstractmethod
    def refresh(self, entity) -> None:
        pass