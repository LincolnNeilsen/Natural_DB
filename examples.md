# Example Questions

Each example shows the zero_shot result (from `responses.json` and `responses_zero_shot.json`) and the few_shot result (from `responses_few_shot.json`, run against the current `setupData.sql`). Several zero_shot logs were generated against earlier data, so the two strategies are not perfectly comparable. Re-running zero_shot on the current data would make it fair.

## 1. What is the oldest book? (both worked)

- **zero_shot SQL:** `SELECT * FROM Book ORDER BY published_date ASC LIMIT 1;`
- **few_shot SQL:** `SELECT title FROM Book ORDER BY published_date ASC LIMIT 1;`
- **Response (both):** The oldest book is "Pride and Prejudice," published on January 28, 1813.

Both correct. The date column is ISO text, so sorting by it works.

## 2. What is the highest rated book? (both worked)

- **zero_shot SQL:** `SELECT Book.title, MAX(Review.rating) ... GROUP BY Book.id ORDER BY highest_rating DESC LIMIT 1;`
- **few_shot SQL:** `SELECT b.title FROM Book b JOIN Review r ON r.id = b.review_id ORDER BY r.rating DESC LIMIT 1;`
- **Response (both):** "Pride and Prejudice."

Several books have a 5, so the answer depends on which row comes first. Neither query handles ties.

## 3. How many books are by Robert Jordan? (both did not work)

- **zero_shot SQL:** filters on `first_name = 'Robert' AND last_name = 'Jordan'`
- **few_shot SQL:** filters on `last_name = 'Jordan'` only
- **Response (both):** There are no books by Robert Jordan in the database.

The data stores the author as "Jordon" (typo in `setupData.sql`), so neither query matches. The few_shot version dropped the first-name filter, but that didn't matter here. The model can't see the data, so it can't catch the typo.

## 4. What is the best fiction book? (both did not work)

- **zero_shot SQL:** filters on `genre = 'Fiction'`
- **few_shot SQL:** filters on `genre = 'Fiction'`
- **Response (zero_shot):** There are no fiction books in the database with ratings.
- **Response (few_shot):** There is no available data on the best fiction book.

No book has the genre "Fiction." Both strategies guessed a value that isn't in the data.

## 5. What is the most popular publisher? (few_shot better)

- **zero_shot SQL:** `SELECT publisher_id, COUNT(*) ... GROUP BY publisher_id ...`
- **few_shot SQL:** `SELECT p.name FROM Publisher p JOIN Book b ... JOIN Review r ... GROUP BY p.id ORDER BY COUNT(r.rating) DESC LIMIT 1;`
- **zero_shot response:** "the one with the ID 5, which has published 3 books." (ID only, no name)
- **few_shot response:** "Blue Lantern Press."

few_shot joined `Publisher` and returned a name, which is what the user wants. Its SQL counts review rows rather than books, and two publishers have 3 books each, so the winner is a tie and the answer is arbitrary.

## 6. What is an author's favorite genre? (zero_shot better)

- **zero_shot SQL:** groups by genre across all authors and returns the most common genre.
- **few_shot SQL:** `WHERE a.first_name = 'AuthorFirstName' AND a.last_name = 'AuthorLastName'`
- **zero_shot response:** "The author's favorite genre is Fantasy." (Confident, but ignores the missing author name.)
- **few_shot response:** "The author's favorite genre is not available in the database."

few_shot copied the placeholder names `AuthorFirstName` and `AuthorLastName` into the query, so it looked for an author who doesn't exist. This is a few_shot-specific failure: the model imitated the example's shape too literally and filled in made-up values.

## 7. Whatis an author's favorite genre? (both did not work)

- **zero_shot:** wrote `?` placeholders with no parameters passed. Error: `Incorrect number of bindings supplied.`
- **few_shot:** same placeholder issue as #6 (`AuthorFirstName`). Response: "not available in the database."

The same question phrased with a different spelling got a valid query from zero_shot, so the zero_shot output was not stable across phrasings.

## 8. What is the most popular genre? (both worked)

- **zero_shot SQL:** `SELECT genre, COUNT(*) AS genre_count FROM Book GROUP BY genre ORDER BY genre_count DESC LIMIT 1;`
- **few_shot SQL:** `SELECT genre FROM Book GROUP BY genre ORDER BY COUNT(*) DESC LIMIT 1;`
- **Response (both):** "Science Fiction."

Both correct. Simple single-table query.

## 9. What is Brandon Sanderson's lowest rated book? (answers differ, both correct for their data)

- **zero_shot response (log):** "There are no reviews available for any of Brandon Sanderson's books."
- **few_shot response:** "There are no books by Brandon Sanderson in the database, so I cannot determine his lowest rated book."

The current `setupData.sql` has no Sanderson rows, so few_shot's answer is accurate. The zero_shot log came from an earlier data version, so the two answers aren't comparable.
