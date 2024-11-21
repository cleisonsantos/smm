-- List of tables
--SELECT * FROM sqlite_master WHERE type='table';

--SELECT * FROM customer;

SELECT * FROM manufacturer m JOIN customer c ON m.customer_id = c.id