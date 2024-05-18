CREATE TABLE Game (
  id SERIAL PRIMARY KEY,
  away_team VARCHAR,
  full_price INTEGER,
  game_date TIMESTAMP,
  tickets_away INTEGER,
  tickets_home INTEGER,
  fk_Club_id INTEGER
);
ALTER TABLE Game ADD CONSTRAINT FK_Game_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
