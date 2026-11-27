CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (PRICE >= 0),
    discount NUMERIC(10, 2) CHECK (PRICE >= 0),
    photo_url TEXT,
    gender VARCHAR(20) NOT NULL CHECK (gender IN ('masculino', 'feminino')),
    product_type VARCHAR(20) NOT NULL CHECK (product_type IN ('roupa', 'calcado')),
    season VARCHAR(20) CHECK (season IN ('inverno', 'verao')),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CHECK (discount IS NULL OR discount <= price),
    CHECK (
        (product_type = 'roupa' AND season IS NOT NULL)
        or (product_type = 'calcado' AND season IS NULL)
    )
);

CREATE TABLE product_variants (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    size INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    UNIQUE (product_id, size)
);