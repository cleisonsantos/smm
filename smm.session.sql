-- List of tables
--SELECT * FROM sqlite_master WHERE type='table';
--SELECT * FROM customer;
--SELECT * FROM manufacturer m JOIN customer c ON m.customer_id = c.id;
--SELECT * FROM component c JOIN solution s ON c.solution_id = s.id JOIN manufacturer m ON s.manufacturer_id = m.id;
--Template queries:
--SELECT * FROM template_section;
--SELECT * FROM template t JOIN template_section ts ON t.id = ts.template_id;
--Questions queries:
-- SELECT *
-- FROM template_section ts
--     JOIN template_question tq ON ts.id = tq.section_id;
-- CREATE TABLE tb_customers (id INTEGER PRIMARY KEY, name TEXT);
-- CREATE TABLE tb_components (
--     id INTEGER PRIMARY KEY,
--     vendor TEXT,
--     product TEXT,
--     cname TEXT
-- );
-- CREATE TABLE tb_itens (
--     id INTEGER PRIMARY KEY,
--     id_component INTEGER,
--     question TEXT,
--     impact TEXT,
--     probability TEXT,
--     criticality TEXT,
--     action TEXT,
--     FOREIGN KEY (id_component) REFERENCES tb_components (id)
-- );
-- CREATE TABLE tb_forms (
--     id INTEGER PRIMARY KEY,
--     num_form INTEGER,
--     customer_id INTEGER,
--     id_item INTEGER,
--     FOREIGN KEY (customer_id) REFERENCES tb_customers (id),
--     FOREIGN KEY (id_item) REFERENCES tb_itens (id)
-- );
-- CREATE TABLE tb_answers(
--     id INTEGER PRIMARY KEY,
--     id_component INTEGER,
--     num_form INTEGER,
--     answer TEXT,
--     FOREIGN KEY (id_component) REFERENCES tb_components (id),
--     FOREIGN KEY (num_form) REFERENCES tb_forms (num_form)
-- );
-- DROP TABLE customer_manufacturer;
-- DROP TABLE template_risk;
-- DROP TABLE alembic_version;
SELECT *
FROM template t
    JOIN template_section ts ON t.id = ts.template_id
    JOIN template_question tq ON ts.id = tq.section_id
    LEFT JOIN template_risk tr ON tq.id = tr.template_question_id
WHERE t.id = 1;