-- Mock data for the books database

INSERT INTO Publisher (id, name) VALUES
    (1, 'Penguin Books'),
    (2, 'Tor Books'),
    (3, 'Tor Books'),
    (4, 'Vintage House'),
    (5, 'Blue Lantern Press');

INSERT INTO Author (id, first_name, last_name) VALUES
    (1, 'Jane', 'Austen'),
    (2, 'Robert', 'Jordon'),
    (3, 'Ursula', 'Le Guin'),
    (4, 'Isaac', 'Asimov'),
    (5, 'Toni', 'Morrison'),
    (6, 'Chimamanda', 'Adichie'),
    (7, 'Terry', 'Pratchett'),
    (8, 'Neil', 'Gaiman'),
    (9, 'Octavia', 'Butler'),
    (10, 'Kazuo', 'Ishiguro');

INSERT INTO Review (id, rating, description) VALUES
    (1, 5, 'A witty, sharp social comedy.'),
    (2, 5, 'Peak fantasy. Will never be beaten'),
    (3, 5, 'Rich worldbuilding and quiet depth.'),
    (4, 3, 'Clever ideas, uneven pacing.'),
    (5, 5, 'Haunting and beautifully written.'),
    (6, 4, 'Powerful story with a strong voice.'),
    (7, 5, 'Hilarious and endlessly rereadable.'),
    (8, 4, 'Atmospheric and imaginative.'),
    (9, 5, 'Gripping and unforgettable.'),
    (10, 2, 'Slow to start, slightly dull.'),
    (11, 4, 'Melancholy and elegant.'),
    (12, 3, 'Good premise, rough execution.');

INSERT INTO Book (id, title, publisher_id, genre, review_id, published_date) VALUES
    (1, 'Pride and Prejudice', 1, 'Romance', 1, '1813-01-28'),
    (2, 'Wheel of Time', 2, 'Fantasy', 2, '1990-01-15'),
    (3, 'The Left Hand of Darkness', 3, 'Science Fiction', 3, '1969-03-01'),
    (4, 'Foundation', 3, 'Science Fiction', 4, '1951-06-01'),
    (5, 'Beloved', 4, 'Literary Fiction', 5, '1987-09-02'),
    (6, 'Half of a Yellow Sun', 4, 'Historical Fiction', 6, '2006-09-01'),
    (7, 'Good Omens', 5, 'Fantasy', 7, '1990-05-01'),
    (8, 'American Gods', 5, 'Fantasy', 8, '2001-06-19'),
    (9, 'Kindred', 1, 'Science Fiction', 9, '1979-06-01'),
    (10, 'Never Let Me Go', 2, 'Literary Fiction', 10, '2005-02-03'),
    (11, 'The Dispossessed', 3, 'Science Fiction', 11, '1974-05-01'),
    (12, 'Guards! Guards!', 5, 'Fantasy', 12, '1989-04-01');

-- book_to_author: includes co-authored Good Omens (Pratchett + Gaiman)
INSERT INTO book_to_author (id, book_id, author_id) VALUES
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3),
    (4, 4, 4),
    (5, 5, 5),
    (6, 6, 6),
    (7, 7, 7),
    (8, 7, 8),
    (9, 8, 8),
    (10, 9, 9),
    (11, 10, 10),
    (12, 11, 3),
    (13, 12, 7);
