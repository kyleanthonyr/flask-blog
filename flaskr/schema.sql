-- This file stores the SQL commands needed to create the USER and POST tables for the db

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE USER(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE POST(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) -- establishes relationship with user table
);