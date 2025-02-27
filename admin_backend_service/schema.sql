DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS book_loans;

CREATE TABLE users (
    email VARCHAR(255) UNIQUE NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_book_loans (
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    loan_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
/*
*/