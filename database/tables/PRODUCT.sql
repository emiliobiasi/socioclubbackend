CREATE TABLE Product (
  id SERIAL PRIMARY KEY ,
  name VARCHAR,
  description VARCHAR,
  price FLOAT,
  fk_Club_id INTEGER,
  fk_ProductCategory_id INTEGER
);
ALTER TABLE Product ADD CONSTRAINT FK_Product_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
ALTER TABLE Product ADD CONSTRAINT FK_Product_3 FOREIGN KEY (fk_ProductCategory_id) REFERENCES ProductCategory (id) ON DELETE RESTRICT;
