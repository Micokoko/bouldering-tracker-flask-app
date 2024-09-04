DROP TABLE IF EXISTS user;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    gender TEXT NOT NULL,
    height TEXT NOT NULL,
    age TEXT NOT NULL
);

CREATE TABLE boulder (
    name TEXT NOT NULL,
    color TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    numberofmoves INTEGER NOT NULL,
)