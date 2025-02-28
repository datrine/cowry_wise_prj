CREATE TABLE IF NOT EXISTS books (
    title VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 1,
    loan_date TEXT NULL,
    return_date TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);