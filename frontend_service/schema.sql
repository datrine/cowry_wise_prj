/*DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;*/

CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) UNIQUE NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/*Avoid joins for performance, accept some data reduncancy and reconcile with eventual consistency*/
CREATE TABLE IF NOT EXISTS borrow_list (
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    loan_date TEXT NULL,
    return_date TEXT NULL
);
/*
*/