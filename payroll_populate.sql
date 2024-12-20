create database tfn_data;
GO

use tfn_data;
Go

create table payrollData (
	PaymentID INT NOT NULL IDENTITY(1,1) PRIMARY KEY, 
	TFN INT,
    DateIssued DATE,
	GrossPay FLOAT,
	NetPay FLOAT,
	TaxWitheld FLOAT
);
GO

SET IDENTITY_INSERT payrollData ON

insert into payrollData(PaymentID, TFN, DateIssued, GrossPay, NetPay, TaxWitheld) values (1, 123456789, '2023-11-01', 7000.0, 4892.0, 2108.0);


