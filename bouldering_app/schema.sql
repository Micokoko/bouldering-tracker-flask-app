DROP TABLE IF EXISTS attempt;
DROP TABLE IF EXISTS boulder;
DROP TABLE IF EXISTS user;
DROP VIEW IF EXISTS boulder_ranking;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    gender TEXT NOT NULL,
    age TEXT NOT NULL,
    profile_picture TEXT,
    highest_grade_climbed INTEGER DEFAULT 0,  
    highest_grade_flashed INTEGER DEFAULT 0   
);

CREATE TABLE boulder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    numberofmoves INTEGER NOT NULL,
    set_date DATE,
    description TEXT,  
    image TEXT,  
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
    difficulty INTEGER NOT NULL,  -- Store the difficulty of the boulder when this attempt was made
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (boulder_id) REFERENCES boulder(id)
);

CREATE VIEW boulder_ranking AS
SELECT 
    boulder.id AS boulder_id,
    boulder.name AS boulder_name,
    COALESCE(user.username, 'No Attempts') AS climber,
    COALESCE(attempt.number_of_attempts, 0) AS number_of_attempts,
    RANK() OVER (
        PARTITION BY boulder.id 
        ORDER BY COALESCE(attempt.number_of_attempts, 0) ASC, MIN(attempt.attempt_date) ASC
    ) AS rank
FROM 
    boulder
LEFT JOIN 
    attempt ON boulder.id = attempt.boulder_id AND attempt.status IN ('completed', 'flashed')
LEFT JOIN 
    user ON attempt.user_id = user.id
WHERE 
    boulder.difficulty >= 6
GROUP BY 
    boulder.id, user.username
ORDER BY 
    boulder.name;
