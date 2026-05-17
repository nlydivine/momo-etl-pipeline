-- CREATE USER
INSERT INTO users (user_names, phone_number, user_email) 
VALUES ('Test', '0723141331', 'test@gmail.com');

INSERT INTO transactions (amount, transaction_date, transaction_status, reference_code, sms_raw_text)
VALUES (7500.00, NOW(), 'completed', '76662021700', 'You have received 7500 RWF from Jane Smith.on your mobile money account at 2024-05-10 16:30:51.');

-- READ FROM TABLES
SELECT * FROM users;

SELECT * FROM transactions WHERE transaction_status = 'completed';

SELECT transaction_status, SUM(amount) AS total_amount
FROM transactions
GROUP BY transaction_status;

-- UPDATE TABLES
UPDATE transactions 
SET transaction_status = 'completed'
WHERE transactions_id = 4;

UPDATE users
SET user_email = 'new@gmail.com'
WHERE user_id = 3;

-- DELETE
DELETE FROM users 
WHERE user_id = 3;