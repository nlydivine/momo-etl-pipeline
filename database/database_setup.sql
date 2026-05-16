CREATE DATABASE momo_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_names TEXT NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    user_email VARCHAR(25) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transactions_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL (10,2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    transaction_status TEXT DEFAULT 'pending',
    reference_code TEXT ,
    sms_raw_text TEXT
);


CREATE TABLE transaction_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name TEXT,
    category_desc TEXT
);

CREATE TABLE transaction_parties (
    party_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    party_role TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE RESTRICT
);

CREATE TABLE system_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL UNIQUE,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logged_level TEXT,
    log_message TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE RESTRICT
);