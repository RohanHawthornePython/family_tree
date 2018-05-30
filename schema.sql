DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS marriage;
DROP TABLE IF EXISTS child;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname TEXT UNIQUE NOT NULL,
  gender TEXT NOT NULL,
  dob TEXT
);

CREATE TABLE marriage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bride INTEGER NOT NULL,
  groom INTEGER NOT NULL,
  divorced INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE child (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  marriage INTEGER NOT NULL,
  child INTEGER NOT NULL
);
  