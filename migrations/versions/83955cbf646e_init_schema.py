"""init schema

Revision ID: 83955cbf646e
Revises: 
Create Date: 2025-10-04 18:52:45.827914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83955cbf646e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""
        CREATE TYPE order_status AS ENUM ('created', 'paid', 'delivered');

        CREATE TABLE nomenclature (
          id INTEGER PRIMARY KEY,
          parent_id INTEGER REFERENCES nomenclature(id),
          name VARCHAR UNIQUE,
          is_leaf BOOLEAN,
          created_at TIMESTAMP
        );

        CREATE TABLE products (
          id INTEGER PRIMARY KEY,
          name VARCHAR,
          nom_id INTEGER REFERENCES nomenclature(id),
          price FLOAT,
          quantity INTEGER,
          created_at TIMESTAMP
        );

        CREATE TABLE users (
          id UUID PRIMARY KEY,
          name VARCHAR,
          address VARCHAR,
          updated_at TIMESTAMP,
          created_at TIMESTAMP
        );

        CREATE TABLE orders (
          id UUID PRIMARY KEY,
          user_id UUID REFERENCES users(id),
          status order_status,
          created_at TIMESTAMP
        );

        CREATE TABLE products_in_orders (
          product_id INTEGER REFERENCES products(id),
          order_id UUID REFERENCES orders(id),
          quantity INTEGER,
          unit_price FLOAT,
          PRIMARY KEY (product_id, order_id)
        );

        CREATE VIEW top_5_products_last_month AS
        SELECT
            p.name AS product_name,
            nc1.name AS top_level_category,
            SUM(pio.quantity) AS total_quantity_sold
        FROM
            products_in_orders pio
        JOIN
            products p ON p.id = pio.product_id
        JOIN
            orders o ON o.id = pio.order_id
        JOIN
            nomenclature nc ON nc.id = p.nom_id
        LEFT JOIN
            nomenclature nc1 ON (
                CASE
                    WHEN nc.parent_id IS NULL THEN nc.id
                    ELSE nc.parent_id
                END
            ) = nc1.id
        WHERE
            o.created_at >= CURRENT_DATE - INTERVAL '1 month'
        GROUP BY
            p.name, nc1.name
        ORDER BY
            total_quantity_sold DESC
        LIMIT 5;

        CREATE INDEX idx_orders_created_at ON orders(created_at);
        CREATE INDEX idx_product_nom_id ON products(nom_id);
        CREATE INDEX idx_products_in_orders_order_id ON products_in_orders(order_id);
        CREATE INDEX idx_products_in_orders_product_id ON products_in_orders(product_id);
        CREATE INDEX idx_nomenclature_parent_id ON nomenclature(parent_id);
    """)


def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS idx_nomenclature_parent_id;
        DROP INDEX IF EXISTS idx_products_in_orders_product_id;
        DROP INDEX IF EXISTS idx_products_in_orders_order_id;
        DROP INDEX IF EXISTS idx_product_nom_id;
        DROP INDEX IF EXISTS idx_orders_created_at;

        DROP VIEW IF EXISTS top_5_products_last_month;

        DROP TABLE IF EXISTS products_in_orders;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS nomenclature;

        DROP TYPE IF EXISTS order_status;
    """)