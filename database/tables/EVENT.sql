CREATE TABLE Event (
  id SERIAL PRIMARY KEY,
  event_name VARCHAR,
  description VARCHAR,
  image VARCHAR,
  full_price INTEGER,
  event_date TIMESTAMP,
  tickets_away INTEGER,
  tickets_home INTEGER,
  fk_Club_id INTEGER
);
ALTER TABLE Event ADD CONSTRAINT FK_Event_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
