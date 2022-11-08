DROP TABLE IF EXISTS Organizations CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Accounts CASCADE;
DROP TABLE IF EXISTS Contacts CASCADE;
DROP TABLE IF EXISTS Tags CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;
DROP TABLE IF EXISTS Transactions CASCADE;
DROP TABLE IF EXISTS Tagged_As CASCADE;

-- CREATE ALL TABLES
CREATE  TABLE IF NOT EXISTS Organizations (
	id serial,
	name text NOT NULL,
	location text,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Users (
	id serial,
	name text NOT NULL,
	email text NOT NULL,
	password text NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
	date_of_birth DATE,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS  Accounts (
	id serial,
	type text,
	name text,
	balance float,
  account_number text NOT NULL,
	org_id int NOT NULL,
	uid int NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (org_id) REFERENCES Organizations
		ON DELETE CASCADE,
	FOREIGN KEY (uid) REFERENCES Users
		ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Contacts (
	id serial,
	uid int NOT NULL,
	name text NOT NULL,
	email text,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (uid) REFERENCES Users(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  Tags (
	id serial,
	name text NOT NULL,
	uid int NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (uid) REFERENCES Users(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  Categories (
	id serial,
	uid int NOT NULL,
	name text NOT NULL,
	"group" text,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP,
	PRIMARY KEY (id),
			CHECK("group" in ('income', 'expense', 'investment')),
	FOREIGN KEY (uid) REFERENCES Users(id)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transactions (
	id serial,
	amount float NOT NULL,
	date TIMESTAMP NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP,
	account_id int NOT NULL,
	contact_id int,
    category_id int,
	memo text,
	PRIMARY KEY (id),
	FOREIGN KEY (account_id) REFERENCES Accounts(id)
		ON DELETE CASCADE,
	FOREIGN KEY (contact_id) REFERENCES Contacts(id),
	FOREIGN KEY (category_id) REFERENCES Categories(id)
);

CREATE TABLE IF NOT EXISTS Tagged_As (
	tag_id int REFERENCES Tags(id)
		ON DELETE CASCADE,
	txn_id int REFERENCES Transactions(id)
		ON DELETE CASCADE,
	PRIMARY KEY (tag_id, txn_id)
);


-- POPULATE Organizations
INSERT INTO Organizations(name, location)  VALUES
('JP Morgan Chase', 'New York'),
('Wells Fargo', 'Washington DC'),
('TD', 'New Jersey'),
('Capital one', 'Boston'),
('Citi', 'Pennsylvania'),
('Bank of America', 'Atlanta'),
('ICICI', 'Bangalore'),
('HDFC', 'Delhi'),
('Bank of Baroda', 'Chennai'),
('Columbia Bank', 'New York');


-- POPULATE USERS

INSERT INTO Users(name, email, date_of_birth, password) VALUES
('John Smith', 'john.smith@mockemail.com', TO_DATE('15 Nov 2000', 'DD Mon YYYY'), 'p1'),
('Alina Loxley', 'alina.loxley@mockemail.com', TO_DATE('12 Jan 1989', 'DD Mon YYYY'),'p2'),
('Harper Stokes', 'harper.stokes@mockemail.com', TO_DATE('11 Mar 1998', 'DD Mon YYYY'),'p3'),
('Barnaby Bradley', 'barnaby.bradley@mockemail.com', TO_DATE('02 Nov 1993', 'DD Mon YYYY'),'p4'),
('Ash Dickinson', 'ash.dickinson@mockemail.com', TO_DATE('18 Feb 2001', 'DD Mon YYYY'),'p5'),
('Phoebe Reed', 'phoebe.reed@mockemail.com', TO_DATE('01 Jun 1990', 'DD Mon YYYY'),'p6'),
('Myrtle Cole', 'myrtle.cole@mockemail.com', TO_DATE('07 Jul 1987', 'DD Mon YYYY'),'p7'),
('Molly Haynes', 'moll.haynes@mockemail.com', TO_DATE('10 Apr 2000', 'DD Mon YYYY'),'p8'),
('Heath Nguyen', 'heath.nguyen@mockemail.com', TO_DATE('21 Dec 1991', 'DD Mon YYYY'),'p9'),
('Halbert Elliott', 'halbert.elliott@mockemail.com', TO_DATE('14 Oct 1972', 'DD Mon YYYY'),'p10');


-- POPULATE CATEGORIES
INSERT INTO Categories(uid, name, "group") VALUES
(1, 'groceries', 'expense'),
(1, 'dining out', 'expense'),
(1, 'salary', 'income'),
(2, 'rent', 'expense'),
(2, 'groceries', 'expense'),
(2, 'dividends', 'income'),
(3, 'grocery shopping', 'expense'),
(3, 'wages', 'income'),
(3, 'reimbursements', 'income'),
(4, 'stocks', 'investment'),
(4, 'nfts', 'investment'),
(4, 'mortgage payment', 'expense'),
(5, 'rent', 'expense'),
(6, 'utilities', 'expense'),
(7, 'dividends', 'income'),
(8, 'grocery shopping', 'expense'),
(9, 'wages', 'income'),
(10, 'reimbursements', 'income'),
(8, 'stocks', 'investment'),
(7, 'nfts', 'investment'),
(6, 'mortgage payment', 'expense');

-- POPULATE TAGS
INSERT INTO Tags(name, uid) VALUES
('vegas trip', 1),
('work expenses', 1),
('holiday decorations', 2),
('secret santa gift', 2),
('bahamas trip', 3),
('gifts for friends', 3),
('supplies for work', 4),
('parking ticket from July', 4),
('gifts for friends', 5),
('school expenses', 5),
('new paint and brushes', 6),
('streaming services', 6),
('trip to aruba', 7),
('expenses while visiting parents', 7),
('furniture for apartment', 8),
('gambling losses', 8),
('school expenses', 10),
('money i will never see again', 10),
('bribery funds', 9),
('presidential election campaign', 9);

-- POPULATE ACCOUNTS

INSERT INTO Accounts(type, name, account_number, balance, org_id, uid) VALUES
('savings', 'my chase account',CAST(1000000000 + floor(random() * 9000000000) AS text), 100, 1,1),
('checking', 'chase_checking',CAST(1000000000 + floor(random() * 9000000000) AS text), -100, 1,1),
('credit', 'bank of america',CAST(1000000000 + floor(random() * 9000000000) AS text), 100000, 6,2),
('savings', 'local savins',CAST(1000000000 + floor(random() * 9000000000) AS text), -999, 8,3),
('savings', 'global savings',CAST(1000000000 + floor(random() * 9000000000) AS text), 0, 8,3),
('savings', 'emergency account',CAST(1000000000 + floor(random() * 9000000000) AS text), -10000, 9,4),
('checking', 'my normal account', CAST(1000000000 + floor(random() * 9000000000) AS text), 100, 3,4),
('credit', 'stolen credit card',CAST(1000000000 + floor(random() * 9000000000) AS text), 8888, 4,5),
('salary', 'moonlighting account',CAST(1000000000 + floor(random() * 9000000000) AS text), 100, 7,7),
('savings', 'secret bribery account',CAST(1000000000 + floor(random() * 9000000000) AS text), 10000000000, 7,9),
('checking', 'columbia student account',CAST(1000000000 + floor(random() * 9000000000) AS text), -9999999999, 10, 10),
('checking','main checking', CAST(1000000000 + floor(random() * 9000000000) AS text), 100000, 1, 2)
;

-- POPULATE Contacts
INSERT INTO Contacts(uid, name, email) VALUES
(1,'Jacob', 'jacob@aol.com'),
(2, 'landlord kenny', 'hungryformoney@landlords.com'),
(2,'Ram', 'ram@gmail.com'),
(3, 'shady craigslist guy', 'counterfeit_goods@gmail.com'),
(4,'Mom', 'jenny@yahoo.com'),
(4, 'Dad', 'johnny@yahoo.com'),
(5,'Grace', 'grace@lionmail.com'),
(6, 'Priya', 'priya.thakur@zoho.com'),
(7, 'Dad', 'jeff@google.com'),
(9,'Xi', 'xijinping@ccp.com'),
(9, 'Putin', 'warmonger@kgb.com'),
(9, 'Kim', 'kim@nukes.com'),
(10, 'Bezos', 'jeff@rainforest.com');

-- POPULATE Transactions
INSERT INTO Transactions(amount, date, account_id, contact_id, category_id, memo) VALUES
(2024.12, TO_DATE('01 Sep 2022', 'DD Mon YYYY'), 1,NULL,3, 'salary'),
(2024.12, TO_DATE('15 Sep 2022', 'DD Mon YYYY'), 2,NULL,3, 'salary'),
(-50.21, TO_DATE('12 Sep 2022', 'DD Mon YYYY'), 2,1,2,NULL),
(-95.10, TO_DATE('02 Sep 2022', 'DD Mon YYYY'),2,NULL,1,NULL),
(-3000.00, TO_DATE('01 Sep 2022', 'DD Mon YYYY'),12,2,4,NULL),
(-150.25, TO_DATE('05 Sep 2022', 'DD Mon YYYY'), 3,NULL,5,NULL),
(1800.01, TO_DATE('01 Sep 2022', 'DD Mon YYYY'), 4,NULL,8,NULL),
(1800.01, TO_DATE('15 Sep 2022', 'DD Mon YYYY'), 4,NULL,8,NULL),
(-50.09, TO_DATE('16 Sep 2022', 'DD Mon YYYY'), 4,NULL,7,NULL),
(-2000, TO_DATE('06 Oct 2022', 'DD Mon YYYY'), 7,NULL,10,NULL),
(-1000, TO_DATE('06 Oct 2022', 'DD Mon YYYY'), 7,NULL,11,NULL),
(-2999.99, TO_DATE('09 Aug 2022', 'DD Mon YYYY'), 8,NULL,NULL,NULL),
(1000.98, TO_DATE('01 Sep 2022', 'DD Mon YYYY'), 9,NULL,NULL,NULL),
(10.15, TO_DATE('30 Sep 2022', 'DD Mon YYYY'), 9,NULL,15,NULL),
(-5000000, TO_DATE('14 Aug 2022', 'DD Mon YYYY'), 10,10,NULL, 'bribery'),
(-5000000, TO_DATE('14 Sep 2022', 'DD Mon YYYY'), 10,11,NULL, 'bribery'),
(-5000000, TO_DATE('14 Oct 2022', 'DD Mon YYYY'), 10,12,NULL, 'bribery'),
(-20000, TO_DATE('02 Sep 2022', 'DD Mon YYYY'), 11,NULL,NULL, 'tuition')
;


-- POPULATE Tagged_As
INSERT INTO Tagged_As(tag_id, txn_id) VALUES
(19,15),
(19,16),
(19,17),
(20,15),
(20,16),
(20,17),
(3,6),
(4,6),
(17,18),
(18,18)
;
