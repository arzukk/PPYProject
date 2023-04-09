-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-04-09 10:23:54.806

-- tables
-- Table: Members
CREATE TABLE Members (
    Username varchar(50)  NOT NULL,
    Password varchar(50)  NOT NULL,
    Email varchar(50)  NOT NULL,
    Recovery_Code int  NOT NULL,
    CONSTRAINT Members_pk PRIMARY KEY  (id)
);

-- End of file.

