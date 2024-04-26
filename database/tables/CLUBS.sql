CREATE TABLE CLUBS (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(50) UNIQUE,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    description VARCHAR(200) NOT NULL,
    address VARCHAR(50) NOT NULL,
    primary_color VARCHAR(7) NOT NULL,
    secondary_color VARCHAR(7) NOT NULL,
    logo BYTEA NOT NULL,
    background BYTEA NOT NULL,
);