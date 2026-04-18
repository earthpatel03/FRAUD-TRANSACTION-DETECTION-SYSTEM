CREATE DATABASE IF NOT EXISTS fraud_db;
USE fraud_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    city VARCHAR(50)
);


-- Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount DECIMAL(10,2),
    location VARCHAR(50),
    txn_time DATETIME,
    is_fraud INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Dummy Users
INSERT INTO users (name, city) VALUES
('Rahul', 'Mumbai'),
('Amit', 'Delhi'),
('Priya', 'Surat'),
('Neha', 'Ahmedabad');

select * from users;

select * from transactions;