-- convert to bml and diagram with https://dbdiagram.io/d
-- use this as example and dont use comments and ignore checks
/*Table suppliers {
  id integer [pk, increment]
  name text [not null]
  current_permit_id integer [not null, ref: > supplier_permits.id]
  address text
  phone text
  email text
  website text
}*/
-- rebuild insert examples if necesary to match the schema

DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS FieldUsages;
DROP TABLE IF EXISTS AuthorizedBuyingQuantities;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS TransactionItems;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS SupplierPermits;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS field_event;
DROP TABLE IF EXISTS field_items;
DROP TABLE IF EXISTS authorized_buying_quantities;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS transaction_items;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS product_types;
DROP TABLE IF EXISTS supplier_permits;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS locations;

-- Suppliers Table
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT
);

CREATE TABLE IF NOT EXISTS supplier_permits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    permit TEXT NOT NULL UNIQUE,
    issue_date TEXT NOT NULL CHECK (issue_date LIKE '____-__-__'),
    updated_date TEXT NOT NULL CHECK (updated_date LIKE '____-__-__'), 
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE TABLE IF NOT EXISTS product_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS product_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category_id TEXT,
    type_id TEXT,
    package_size REAL NOT NULL DEFAULT 1,
    supplier_package_size REAL NOT NULL DEFAULT 1,
    supplier_id INTEGER NOT NULL,
    unit TEXT NOT NULL DEFAULT 'u',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (type_id) REFERENCES product_types(id)
    FOREIGN KEY (category_id) REFERENCES product_categories(id)
);

CREATE TABLE IF NOT EXISTS product_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_name TEXT,
    sap_name TEXT,
    balance_name TEXT,
    product_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice TEXT NOT NULL UNIQUE,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    status TEXT NOT NULL DEFAULT 'pending',
    supplier_id INTEGER,
    comments TEXT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    barcode TEXT UNIQUE,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (type IN ('in', 'out', 'return')),
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    comments TEXT
);

CREATE TABLE IF NOT EXISTS transaction_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    barcode TEXT UNIQUE,     
    order_item_id INTEGER,
    field_usage_id INTEGER,
    quantity REAL NOT NULL DEFAULT 1,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (order_item_id) REFERENCES order_items(id),
    FOREIGN KEY (field_usage_id) REFERENCES field_usages(id)
);

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    previous_existence REAL NOT NULL,
    bought REAL NOT NULL,
    consumed REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS authorized_buying_quantities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    authorized_quantity INTEGER NOT NULL,
    year INTEGER NOT NULL,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    FOREIGN KEY (category_id) REFERENCES product_categories(id),
    UNIQUE (category_id, authorized_quantity, year, date)
);


CREATE TABLE IF NOT EXISTS field_event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    location_id INTEGER NOT NULL,
    comments TEXT,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS field_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    barcode TEXT UNIQUE,
    quantity REAL NOT NULL DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES field_event(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    observations TEXT NOT NULL,
    representative TEXT NOT NULL,
    place TEXT NOT NULL,
    comments TEXT
);

create TABLE IF NOT EXISTS authorized_quantity_modifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    modification INTEGER NOT NULL,
    reason TEXT,
    date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
    FOREIGN KEY (category_id) REFERENCES product_categories(id)
);

INSERT INTO product_types (type) VALUES 
('Explosivos'), 
('Accesorios');

INSERT INTO locations (name) VALUES 
('Cantera Grava Alta'), 
('Cantera Grava Baja');
