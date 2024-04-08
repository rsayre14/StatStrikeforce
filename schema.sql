CREATE TABLE user
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    TEXT NOT NULL,
    prediction INTEGER CHECK (prediction BETWEEN 1 AND 10 OR prediction IS NULL)
);