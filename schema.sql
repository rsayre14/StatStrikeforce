DROP TABLE IF EXISTS user_stats;
DROP TABLE IF EXISTS user;

CREATE TABLE user_stats
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    TEXT UNIQUE NOT NULL,
    mse_attack REAL,
    mse_defend REAL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE user
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    r6_user_id    TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
