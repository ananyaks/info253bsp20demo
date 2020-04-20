CREATE TABLE tasks (
    id BIGINT serial primary KEY,
    title VARCHAR(500) NOT NULL,
    is_completed BOOLEAN NOT NULL
);