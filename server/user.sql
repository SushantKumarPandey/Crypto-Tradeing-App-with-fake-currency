DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS coin;
DROP TABLE IF EXISTS holding;
DROP TABLE IF EXISTS guides;
DROP TABLE IF EXISTS tutorial;


CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE guides(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nameG TEXT UNIQUE NOT NULL,
    info TEXT UNIQUE NOT NULL
);

CREATE TABLE tutorial(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nameT TEXT UNIQUE NOT NULL,
    info TEXT UNIQUE NOT NULL
);


CREATE TABLE coin(
    id INTEGER PRIMARY KEY,
    price FLOAT,
    name TEXT,
    supply INTEGER,
    symbol TEXT ,
    market_cap FLOAT ,
    last_updated DATE
);

CREATE TABLE holding(
    user_id INTEGER NOT NULL,
    coin_symbol TEXT NOT NULL,
    amount INTEGER,
    value Float,
    PRIMARY KEY(user_id, coin_symbol)
);

INSERT INTO user (username, password, email)
    VALUES ('kiki','quack', 'bsp1@gmail.com'),
           ('test','a','a'),
           ('marcel','duck', 'bsp2@gmail.com');

INSERT INTO holding (user_id, coin_symbol, amount, value)
    VALUES (2, 'BTC', 3,25.5);


INSERT INTO guides (nameG, info)
    VALUES ('GA', 'ALorem ipsum dolor sit amet, '),
('GB', 'BLorem ipsum dolor sit amet, '),
('GC', 'CLorem ipsum dolor sit amet, ');

INSERT INTO tutorial (nameT, info)
    VALUES ('What is Bitcoin?', 'It ia a cryptocurrency, which was launched in 2009. It is Interessting for Investors, because the price is very volatile.'),

('Where to start?', 'The best start would be, to look at the top list and check the data of the current market.'),

('Your first invest:', 'Befor your first invest take into account, that the amount of the value will be transformed into the coin value. \n When you want to sell, make sure to sell to a higher value'),

('where to follow your invests?', 'In your Portfolio you can monitor you invests, with the current value and if yoou would make plus or minus'),

('Now Try yourself!', 'for completing this boring tutorial you get 10.000 coins! Good Luck!');

