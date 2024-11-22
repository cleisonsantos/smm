-- List of tables
--SELECT * FROM sqlite_master WHERE type='table';

--SELECT * FROM customer;

--SELECT * FROM manufacturer m JOIN customer c ON m.customer_id = c.id;
SELECT * FROM component c JOIN solution s ON c.solution_id = s.id JOIN manufacturer m ON s.manufacturer_id = m.id;