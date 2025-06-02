DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS coin;
DROP TABLE IF EXISTS holding;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE coin(
    id INTEGER PRIMARY KEY,
    price FLOAT NOT NULL,
    name TEXT NOT NULL,
    supply INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    market_cap FLOAT NOT NULL,
    last_updated DATE NOT NULL
);

CREATE TABLE holding(
    user_id INTEGER NOT NULL,
    coin_symbol TEXT NOT NULL,
    amount INTEGER,
    PRIMARY KEY(user_id, coin_symbol)
);

INSERT INTO user (username, password, email)
    VALUES ('kiki','quack', 'bsp1@gmail.com'),
           ('marcel','duck', 'bsp2@gmail.com');

INSERT INTO holding (user_id, coin_symbol, amount)
    VALUES (2, 'BTC', 3);