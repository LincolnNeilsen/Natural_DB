-- Books database schema (from REF/init.jpg)
-- ponytail: SQLite types instead of the diagram's placeholder bigint for every column

DROP TABLE IF EXISTS book_to_author;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Publisher;

CREATE TABLE Publisher (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE Author (
    id         INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL
);

CREATE TABLE Review (
    id          INTEGER PRIMARY KEY,
    rating      INTEGER CHECK (rating BETWEEN 1 AND 5),
    description TEXT
);

CREATE TABLE Book (
    id             INTEGER PRIMARY KEY,
    title          TEXT NOT NULL,
    publisher_id   INTEGER REFERENCES Publisher(id),
    genre          TEXT,
    review_id      INTEGER REFERENCES Review(id),
    published_date TEXT  -- ISO 8601, YYYY-MM-DD
);

CREATE TABLE book_to_author (
    id        INTEGER PRIMARY KEY,
    book_id   INTEGER NOT NULL REFERENCES Book(id),
    author_id INTEGER NOT NULL REFERENCES Author(id)
);
