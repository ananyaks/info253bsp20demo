CREATE TABLE tasks (
    id int unsigned not null auto_increment primary key,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL,
    zipcode VARCHAR(5) NOT NULL
);
