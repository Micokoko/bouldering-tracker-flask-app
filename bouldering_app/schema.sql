DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS boulder;
DROP TABLE IF EXISTS attempt;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    gender TEXT NOT NULL,
    age TEXT NOT NULL
);

CREATE TABLE boulder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    numberofmoves INTEGER NOT NULL,
    set_date DATE 
);

CREATE TABLE attempt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    boulder_id INTEGER NOT NULL,
    numberofmoves INTEGER NOT NULL,
    status TEXT CHECK(status IN ('incomplete', 'completed')) NOT NULL,
    attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (boulder_id) REFERENCES boulder(id)
);
