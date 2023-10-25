-- CREATE DATABASE
CREATE DATABASE AUTOFORM;

-- CREATE TABLES
CREATE TABLE RANGER_INFO (
    RangerID int NOT NULL,
    RangerFirst varchar(50),
    RangerLast varchar(50),
    RangerMI char(1),
    RangerDODID int(10),
    RangerRank varchar(5),
    RangerOther varchar(255),
    PRIMARY KEY (RangerID)
);
CREATE TABLE FORMS (

);
CREATE TABLE EQUIPMENT (
    ItemID int NOT NULL,
    SerialNumber varchar(50),
    ItemDescription varchar(255),
    ItemQuantity int,
    PRIMARY KEY (ItemID)
);
