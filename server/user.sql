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


INSERT INTO guides (nameG, info)
    VALUES ('GA', 'ALorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet'),
('GB', 'BLorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet'),
('GC', 'CLorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet');

INSERT INTO tutorial (nameT, info)
    VALUES ('TA', 'ALorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet'),
('TB', 'BLorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet'),
('TC', 'CLorem ipsum dolor sit amet, ' ||
                  'consetetur sadipscing elitr, sed diam nonumy eirmod ' ||
                  'tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, ' ||
                  'no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing ' ||
                  'elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. ' ||
                  'At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est ' ||
                  'Lorem ipsum dolor sit amet');
