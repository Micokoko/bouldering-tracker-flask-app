DROP TABLE IF EXISTS attempt;
DROP TABLE IF EXISTS boulder;
DROP TABLE IF EXISTS user;

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
    set_date DATE,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by) REFERENCES user(id)
);

CREATE TABLE attempt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number_of_attempts INTEGER NOT NULL,
    status TEXT CHECK(status IN ('incomplete', 'completed', 'flashed')) NOT NULL,
    attempt_date DATE DEFAULT (DATE('now')),
    user_id INTEGER NOT NULL,
    boulder_id INTEGER NOT NULL,
    moves_completed INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (boulder_id) REFERENCES boulder(id)
);


CREATE VIEW boulder_ranking AS
SELECT 
    boulder.id AS boulder_id,
    boulder.name AS boulder_name,
    user.username AS climber,
    attempt.number_of_attempts,
    RANK() OVER (
        PARTITION BY boulder.id 
        ORDER BY attempt.number_of_attempts ASC
    ) AS rank
FROM 
    attempt
JOIN 
    boulder ON attempt.boulder_id = boulder.id
JOIN 
    user ON attempt.user_id = user.id
WHERE 
    attempt.status = 'completed';
