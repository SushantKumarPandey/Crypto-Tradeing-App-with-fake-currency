DROP TABLE IF EXISTS user;

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
    last_updated DATE NOT NULL,
);

INSERT INTO user (username, password, email)
    VALUES ('kiki','quack', 'bsp1@gmail.com'),
           ('marcel','duck', 'bsp2@gmail.com');
