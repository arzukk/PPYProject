-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-04-09 10:21:24.342

-- tables
-- Table: Books
CREATE TABLE Books (
    id int  NOT NULL,
    Name varchar(50)  NOT NULL,
    Writer varchar(50)  NOT NULL,
    Publisher varchar(50)  NOT NULL,
    Type varchar(50)  NOT NULL,
    Number_of_Page int  NOT NULL,
    Edition int  NOT NULL,
    CONSTRAINT Books_pk PRIMARY KEY  (id)
);

-- End of file.

