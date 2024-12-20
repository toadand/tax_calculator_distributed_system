create database tfn_data;
GO

use tfn_data;
Go

create table tfnDataTable (
	personId INT NOT NULL IDENTITY(1,1) PRIMARY KEY, 
	TFN INT,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50)
);
GO

SET IDENTITY_INSERT tfnDataTable ON

insert into tfnDataTable(personId, TFN, first_name, last_name, email) values (1, 123456789, 'Phyllys', 'Milbank', 'phyllys@eou.edu.au');
insert into tfnDataTable(personId, TFN, first_name, last_name, email) values (1, 928467362, 'John', 'Chair', 'jchair@email.com.au');
insert into tfnDataTable(personId, TFN, first_name, last_name, email) values (1, 567109146, 'Paul', 'Lamp', 'paullamp@email.com.au');
insert into tfnDataTable(personId, TFN, first_name, last_name, email) values (1, 123571974, 'Amy', 'Long', 'amy_long@email.com.au');


