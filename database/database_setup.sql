CREATE DATABASE momo_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_names TEXT NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    user_email VARCHAR(25) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transaction_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name TEXT,
    category_desc TEXT
);

CREATE TABLE transactions (
    transactions_id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    transaction_date DATETIME NOT NULL,
    transaction_status TEXT CHECK (transaction_status IN ('pending', 'completed', 'failed')),
    reference_code TEXT COMMENT 'Unique reference code from MoMo SMS',
    sms_raw_text TEXT COMMENT 'Raw SMS text received from MoMo'
);

CREATE TABLE transaction_parties (
    party_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    party_role TEXT CHECK (party_role IN ('sender', 'receiver')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transactions_id) ON DELETE RESTRICT
);

CREATE TABLE system_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logged_level TEXT CHECK (logged_level IN ('INFO', 'WARNING', 'ERROR')),
    log_message TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transactions_id) ON DELETE RESTRICT
);

CREATE INDEX idx_transaction_status ON transactions(transaction_status);
CREATE INDEX idx_user_email ON users(user_email);
CREATE INDEX idx_phone_number ON users(phone_number);