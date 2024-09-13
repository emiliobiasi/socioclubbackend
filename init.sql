CREATE TABLE Club (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    password VARCHAR,
    description VARCHAR,
    address VARCHAR,
    logo VARCHAR,
    email VARCHAR,
    cnpj VARCHAR,
    background VARCHAR,
    titles_color VARCHAR,
    subtitles_color VARCHAR,
    buttons_color VARCHAR,
    palette_1 VARCHAR,
    palette_2 VARCHAR,
    palette_3 VARCHAR,
    fk_ClubCategory_id INTEGER
);
CREATE TABLE ClubCategory (id SERIAL PRIMARY KEY, name VARCHAR);
CREATE TABLE News (
    id SERIAL PRIMARY KEY,
    text VARCHAR,
    image VARCHAR,
    author VARCHAR,
    title VARCHAR,
    publish_date TIMESTAMP,
    fk_Club_id INTEGER
);
CREATE TABLE Plan (
    id SERIAL PRIMARY KEY,
    price FLOAT,
    discount INTEGER,
    priority INTEGER,
    image VARCHAR,
    description VARCHAR,
    name VARCHAR,
    fk_Club_id INTEGER
);
CREATE TABLE Product (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    price INTEGER,
    image VARCHAR,
    fk_Club_id INTEGER,
    fk_ProductCategory_id INTEGER
);
CREATE TABLE Client (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    cpf VARCHAR,
    password VARCHAR,
    email VARCHAR
);
CREATE TABLE Event (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR,
    full_price FLOAT,
    tickets_away INTEGER,
    tickets_home INTEGER,
    event_date TIMESTAMP,
    image VARCHAR,
    description VARCHAR,
    fk_Club_id INTEGER
);
CREATE TABLE Ticket (qr_code VARCHAR PRIMARY KEY, fk_Event_id INTEGER);
CREATE TABLE ProductCategory (id SERIAL PRIMARY KEY, name VARCHAR);
CREATE TABLE Associate (
    fk_Club_id INTEGER,
    fk_Client_id INTEGER,
    fk_Plan_id INTEGER
);
CREATE TABLE Buy (
    fk_Client_id INTEGER,
    fk_Product_id INTEGER,
    fk_Ticket_qr_code VARCHAR
);
CREATE TABLE Follow (fk_Client_id INTEGER, fk_Club_id INTEGER);
ALTER TABLE Club
ADD CONSTRAINT FK_Club_2 FOREIGN KEY (fk_ClubCategory_id) REFERENCES ClubCategory (id) ON DELETE RESTRICT;
ALTER TABLE News
ADD CONSTRAINT FK_News_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
ALTER TABLE Plan
ADD CONSTRAINT FK_Plan_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
ALTER TABLE Product
ADD CONSTRAINT FK_Product_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
ALTER TABLE Product
ADD CONSTRAINT FK_Product_3 FOREIGN KEY (fk_ProductCategory_id) REFERENCES ProductCategory (id) ON DELETE RESTRICT;
ALTER TABLE Event
ADD CONSTRAINT FK_Event_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
ALTER TABLE Ticket
ADD CONSTRAINT FK_Ticket_2 FOREIGN KEY (fk_Event_id) REFERENCES Event (id) ON DELETE RESTRICT;
ALTER TABLE Associate
ADD CONSTRAINT FK_Associate_1 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE NO ACTION;
ALTER TABLE Associate
ADD CONSTRAINT FK_Associate_2 FOREIGN KEY (fk_Client_id) REFERENCES Client (id) ON DELETE NO ACTION;
ALTER TABLE Associate
ADD CONSTRAINT FK_Associate_3 FOREIGN KEY (fk_Plan_id) REFERENCES Plan (id) ON DELETE RESTRICT;
ALTER TABLE Buy
ADD CONSTRAINT FK_Buy_1 FOREIGN KEY (fk_Client_id) REFERENCES Client (id) ON DELETE NO ACTION;
ALTER TABLE Buy
ADD CONSTRAINT FK_Buy_2 FOREIGN KEY (fk_Product_id) REFERENCES Product (id) ON DELETE NO ACTION;
ALTER TABLE Buy
ADD CONSTRAINT FK_Buy_3 FOREIGN KEY (fk_Ticket_qr_code) REFERENCES Ticket (qr_code) ON DELETE NO ACTION;
ALTER TABLE Follow
ADD CONSTRAINT FK_Follow_1 FOREIGN KEY (fk_Client_id) REFERENCES Client (id) ON DELETE RESTRICT;
ALTER TABLE Follow
ADD CONSTRAINT FK_Follow_2 FOREIGN KEY (fk_Club_id) REFERENCES Club (id) ON DELETE RESTRICT;
INSERT INTO ClubCategory (name)
VALUES ('Futebol');
INSERT INTO ProductCategory (name)
VALUES ('Roupa');
INSERT INTO Club (
        name,
        password,
        description,
        address,
        logo,
        email,
        cnpj,
        background,
        titles_color,
        subtitles_color,
        buttons_color,
        palette_1,
        palette_2,
        palette_3,
        fk_ClubCategory_id
    )
VALUES (
        'São Paulo',
        '$2b$12$PvqUEBF2FDX4fe/1qzWfF.9OwxcOPsaLg3M5.mW8sKQ2v3fT0G6ba',
        'Soberano',
        'Rua São Paulo',
        'https://storage.googleapis.com/socioclub/club/sao-paulo/logo.png',
        'saopaulo@email.com',
        '123456789',
        'https://storage.googleapis.com/socioclub/club/sao-paulo/background.jpeg',
        '#FFFFFF',
        '#FFFFFF',
        '#000000',
        '#9e0100',
        '#fc2221',
        '#460101',
        1
    );
INSERT INTO Client (cpf, name, email, password)
VALUES (
        '123456789',
        'Emílio Biasi',
        'emilio@email.com',
        '$2b$12$naI2qHn6/ibCeQvwLNkuNuamH5G9fSk/lwI7V.gawjWSeUcI3BujO'
    );
INSERT INTO News (
        text,
        image,
        author,
        fk_Club_id,
        publish_date,
        title
    )
VALUES (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'https://storage.googleapis.com/socioclub/news/sao-paulo/1.jpg',
        'Thiago Santos',
        1,
        NOW (),
        'Nova Contratação Chegando'
    );
INSERT INTO Plan (
        price,
        discount,
        priority,
        image,
        description,
        name,
        fk_Club_id
    )
VALUES (
        10.99,
        5,
        1,
        'https://storage.googleapis.com/socioclub/plan/1/1.jpeg',
        'Básico Tricolor, o clube dos verdadeiros apaixonados pelo futebol, tem como objetivo oferecer aos nossos sócios a melhor experiência possível, dentro e fora dos campos. Como sócio, você tem direito a descontos especiais na compra de ingressos para todos os jogos em casa, com 20% de desconto em arquibancada, 15% em cadeiras superiores e 10% em áreas VIP e camarotes. Além disso, você pode garantir seu lugar no estádio antes de todo mundo com a pré-venda exclusiva, iniciando 48 horas antes da abertura para o público geral, pacotes promocionais para temporadas completas com condições especiais de pagamento e acesso prioritário em jogos decisivos e eventos especiais.',
        'Básico Tricolor',
        1
    );
INSERT INTO Product (
        name,
        description,
        price,
        fk_Club_id,
        fk_ProductCategory_id
    )
VALUES (
        'Camisa Oficial - Jogo',
        'Camisa Oficial de jogo do São Paulo',
        300,
        1,
        1
    );
INSERT INTO Event (
        event_name,
        description,
        image,
        full_price,
        event_date,
        tickets_away,
        tickets_home,
        fk_Club_id
    )
VALUES (
        'SÃO PAULO x CRUZEIRO - AMISTOSO',
        'Partida emocionante entre São Paulo e Cruzeiro no Morumbi',
        'https://storage.googleapis.com/socioclub/event/1/3/3.png',
        150,
        '2024-06-15 16:00:00',
        500,
        5000,
        1
    );