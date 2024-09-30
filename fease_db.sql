DROP TABLE IF EXISTS gems_customers;

CREATE TABLE gems_customers (
    customer_name VARCHAR(255),
    account_type VARCHAR(100),
    account_number VARCHAR(50),
    balance DECIMAL(10, 2),
    created_at TIMESTAMP
);
