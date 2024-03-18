PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    username    varchar(50) not null,
    password    varchar(50) not null,
    fname       varchar(50) not null,
    lname       varchar(50) not null,
    PRIMARY KEY (username)
);

DROP TABLE IF EXISTS products;
CREATE TABLE products (
    name        varchar(50) not null,
    artist      varchar(50) not null,
    price       REAL not null,
    quantity    int(1) not null,
    image       varchar(50) not null,
    PRIMARY KEY (name)
);

DROP TABLE IF EXISTS history;
CREATE TABLE history (
    uname   varchar(50) not null,
    pname   varchar(50) not null, 
    price   int(1) not null,
    FOREIGN KEY (uname) REFERENCES users(username)
);

PRAGMA foreign_keys=on;

INSERT INTO users VALUES ('testuser', 'testpass', 'Test', 'User');

--products
INSERT INTO products VALUES('4:44', 'JAY-Z', 34.99, 5, 'static/assets/products/444.png');
INSERT INTO products VALUES('And Then You Pray For Me', 'Westside Gunn', 17.99, 20, 'static/assets/products/And_Then_You_Pray_for_Me.png');
INSERT INTO products VALUES('CALL ME IF YOU GET LOST', 'Tyler, The Creator', 29.99, 5, 'static/assets/products/CMIYGL.png');
INSERT INTO products VALUES('DAMN.', 'Kendrick Lamar', 29.99, 1, 'static/assets/products/damn.png');
INSERT INTO products VALUES('DiCaprio 2', 'JID', 22.99, 10, 'static/assets/products/DiCaprio2.png');
INSERT INTO products VALUES('Die Lit', 'Playboi Carti', 29.99, 3, 'static/assets/products/DieLit.png');
INSERT INTO products VALUES('HEROES & VILLIANS', 'Metro Boomin', 34.99, 3, 'static/assets/products/Hereos&Villains.png');
INSERT INTO products VALUES('Flower Boy', 'Tyler, The Creator', 20.99, 5, 'static/assets/products/FlowerBoy.png');
INSERT INTO products VALUES('Let''s Start Here.', 'Lil Yachty', 22.99, 15, 'static/assets/products/Lets_Start_Here.png');
INSERT INTO products VALUES('Lil Uzi Vert vs. The World', 'Lil Uzi Vert', 24.99, 10, 'static/assets/products/LilUziVertVsTheWorld.png');
INSERT INTO products VALUES('Rodeo', 'Travis Scott', 24.99, 2, 'static/assets/products/Rodeo.png');
INSERT INTO products VALUES('The Melodic Blue', 'Baby Keem', 29.99, 10, 'static/assets/products/TheMelodicBlue.png');
INSERT INTO products VALUES('Classic Black Turntable', 'Turntablers', 49.99, 10, 'static/assets/products/turntable1.png');
INSERT INTO products VALUES('Classic Red Turntable', 'Turntablers', 54.99, 10, 'static/assets/products/turntable2.png');
INSERT INTO products VALUES('Portable Turntable', 'Dolby', 79.99, 15, 'static/assets/products/turntable3.png');
INSERT INTO products VALUES('Cartoon Headphones', 'Disney', 49.99, 30, 'static/assets/products/headphones1.png'); 
INSERT INTO products VALUES('Beats Headphones', 'Apple', 129.99, 20, 'static/assets/products/headphones2.png'); 
INSERT INTO products VALUES('Bose Headphones', 'Bose', 249.99, 4, 'static/assets/products/headphones3.png'); 

 

