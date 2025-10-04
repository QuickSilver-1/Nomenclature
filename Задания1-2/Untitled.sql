CREATE TYPE order_status AS ENUM ('created', 'paid', 'delivered');

CREATE TABLE nomenclature (
  id INTEGER PRIMARY KEY,
  parent_id INTEGER REFERENCES nomenclature(id), -- Создает дерево из номенклатур, позволяет создавать произвольную вложенность
  name VARCHAR UNIQUE,
  is_leaf BOOLEAN, -- Это поле будет определять является ли номенклатура товаром или категорией (только если в бизнес требованиях будет разграничения между этими сущностями)
  created_at TIMESTAMP
);

CREATE TABLE products (
  id VARCHAR PRIMARY KEY,
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
  product_id VARCHAR REFERENCES products(id),
  order_id UUID REFERENCES orders(id),
  quantity INTEGER,
  unit_price FLOAT,
  PRIMARY KEY (product_id, order_id)
);

-- 2.1
SELECT users.name, SUM(products_in_orders.unit_price * products_in_orders.quantity)
FROM users LEFT JOIN orders
ON users.id = orders.user_id
LEFT JOIN products_in_orders
ON orders.id = products_in_orders.order_id
GROUP BY users.name

-- 2.2
SELECT parent_id, COUNT(*)
FROM nomenclature
WHERE parent_id IS NOT NULL
GROUP BY parent_id;

-- 2.3.1
CREATE VIEW top_5_products_last_month AS
SELECT
    p.name AS product_name,
    nc1.name AS top_level_category,
    SUM(pio.quantity) AS total_quantity_sold
FROM
    products_in_orders pio
JOIN
    product p ON p.id = pio.product_id
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

-- Проблемы при большом объеме данных:
-- JOIN по некскольким таблицам
-- Подзапрос с CASE для определения категории
-- Отсутствие индексов

CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_product_nom_id ON product(nom_id);
CREATE INDEX idx_products_in_orders_order_id ON products_in_orders(order_id);
CREATE INDEX idx_products_in_orders_product_id ON products_in_orders(product_id);
CREATE INDEX idx_nomenclature_parent_id ON nomenclature(parent_id);

-- Если необходимо часто использовать это представление, то статистику самых популярных товаров
-- можно вынести в отдельную таблицу и обновляь ее динамически при совершении заказа
-- Также можно использовать MATERIALIZED VIEW 