from sqlalchemy.orm import Session
from .order_repository import OrderRepository
from ...domain import product, order, products_in_orders


class OrderManager(OrderRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_product_for_update(self, product_id: str):
        return (
            self.db.query(product.Product)
            .with_for_update(nowait=False)
            .filter(product.Product.id == product_id)
            .one_or_none()
        )

    def get_order(self, order_id):
        return self.db.query(order.Order).filter(order.Order.id == order_id).one_or_none()

    def get_product_in_order(self, order_id, product_id):
        return (
            self.db.query(products_in_orders.ProductInOrder)
            .filter(
                products_in_orders.ProductInOrder.order_id == order_id,
                products_in_orders.ProductInOrder.product_id == product_id,
            )
            .one_or_none()
        )

    def add_product_in_order(self, order_id, product, quantity):
        pio = products_in_orders.ProductInOrder(
            order_id=order_id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
        )
        self.db.add(pio)
        return pio

    def update_product_quantity_in_order(self, pio, add_qty):
        pio.quantity += add_qty
        return pio

    def save_changes(self):
        self.db.commit()

    def refresh(self, entity):
        self.db.refresh(entity)
