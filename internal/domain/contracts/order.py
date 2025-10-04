from abc import ABC, abstractmethod
from uuid import UUID
from ..products_in_orders import ProductInOrder

class OrderServiceInterface(ABC):

    @abstractmethod
    def add_product_to_order(self, order_id: UUID, product_id: str, quantity: int) -> ProductInOrder:
        pass
