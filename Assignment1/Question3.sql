CREATE TABLE IF NOT EXISTS Suppliers
	(sid INTEGER NOT NULL,
	sname TEXT NOT NULL,
	address TEXT NOT NULL,
	PRIMARY KEY (sid));

CREATE TABLE IF NOT EXISTS Parts
	(pid INTEGER NOT NULL,
	pname TEXT NOT NULL,
	color TEXT NOT NULL,
	PRIMARY KEY (pid));

CREATE TABLE IF NOT EXISTS Catalog
	(sid INTEGER NOT NULL,
	pid INTEGER NOT NULL,
	cost REAL NOT NULL,
	PRIMARY KEY (sid, pid));

-- Question 1. b) i)
WITH R1 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R2 AS
	(
		SELECT *
		FROM R1 NATURAL JOIN Catalog
	),
	R3 AS
	(
		SELECT sid
		FROM R2
	),
	R4 AS
	(
		SELECT *
		FROM R3 NATURAL JOIN Suppliers
	),
	R5 AS
	(
		SELECT sname
		FROM R4
	)
SELECT *
From R5;

--Question 1. b) ii)
WITH R1 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R2 AS
	(
		SELECT *
		FROM R1 NATURAL JOIN Catalog
	),
	R3 AS
	(
		SELECT sid
		FROM R2
	),
	R4 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Green')
	),
	R5 AS
	(
		SELECT *
		FROM R4 NATURAL JOIN Catalog
	),
	R6 AS
	(
		SELECT sid
		FROM R5
	),
	R7 AS
	(
		SELECT *
		FROM (SELECT * FROM R3 UNION SELECT * FROM R6)
	)
SELECT *
FROM R7;

--Question 1. b) iii)
WITH R1 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R2 AS
	(
		SELECT *
		FROM R1 NATURAL JOIN Catalog
	),
	R3 AS
	(
		SELECT sid
		FROM R2
	),
	R4 AS
	(
		SELECT *
		FROM Suppliers
		WHERE upper(Suppliers.address) = upper('1065 Military Trail')
	),
	R5 AS
	(
		SELECT sid
		FROM R4
	),
	R6 AS
	(
		SELECT *
		FROM (SELECT * FROM R3 UNION SELECT * FROM R5)
	)
SELECT*
FROM R6;

--Question 1. b) iv)
WITH R1 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R2 AS
	(
		SELECT R1.pid
		FROM R1
	),
	R3 AS
	(
		SELECT *
		FROM R2 NATURAL JOIN Catalog
	),
	R4 AS
	(
		SELECT R3.sid
		FROM R3
	),
	R5 AS
	(
		SELECT *
		FROM R4
	),
	R6 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Green')
	),
	R7 AS
	(
		SELECT R6.pid
		FROM R6
	),
	R8 AS
	(
		SELECT *
		FROM R7 NATURAL JOIN Catalog
	),
	R9 AS
	(
		SELECT R8.sid
		FROM R8
	),
	R10 AS
	(
		SELECT *
		FROM R9
	),
	R11 AS
	(
		SELECT *
		FROM (SELECT * FROM R5 INTERSECT SELECT * FROM R10)
	)
SELECT *
FROM R11;

--Question 1. b) v)
WITH R1 AS
	(
		SELECT sid, pid
		FROM Catalog
	),
	R2 AS
	(
		SELECT pid
		FROM Parts
	),
	R3 AS
	(
		SELECT sid
		FROM R1
	),
	R4 AS
	(
		SELECT *
		FROM (R3 INNER JOIN R2)
	),
	R5 AS
	(
		SELECT *
		FROM R4 EXCEPT SELECT * FROM R1
	),
	R6 AS
	(
		SELECT sid
		FROM R5
	),
	R7 AS
	(
		SELECT *
		FROM R3 EXCEPT SELECT * FROM R6
	)
SELECT *
FROM R7;
	
--Question 1. b) vi)
WITH R1 AS
	(
		SELECT sid, pid
		FROM Catalog
	),
	R2 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R3 AS
	(
		SELECT pid
		FROM R2
	),
	R4 AS
	(
		SELECT sid
		FROM R1
	),
	R5 AS
	(
		SELECT *
		FROM (R4 INNER JOIN R3)
	),
	R6 AS
	(
		SELECT *
		FROM R5 EXCEPT SELECT * FROM R1
	),
	R7 AS
	(
		SELECT sid
		FROM R6
	),
	R8 AS
	(
		SELECT *
		FROM R4 EXCEPT SELECT * FROM R7
	)
SELECT *
FROM R8;

--Question 1. b) vii)
WITH R1 AS
	(
		SELECT sid, pid
		FROM Catalog
	),
	R2 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R3 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Green')
	),
	R4 AS
	(
		SELECT *
		FROM (SELECT * FROM R2 UNION SELECT * FROM R3)
	),
	R5 AS
	(
		SELECT pid
		FROM R4
	),
	R6 AS
	(
		SELECT sid
		FROM R1
	),
	R7 AS
	(
		SELECT *
		FROM (R6 INNER JOIN R5)
	),
	R8 AS
	(
		SELECT *
		FROM R7 EXCEPT SELECT * FROM R1
	),
	R9 AS
	(
		SELECT sid
		FROM R8
	),
	R10 AS
	(
		SELECT *
		FROM R6 EXCEPT SELECT * FROM R9
	)
SELECT *
FROM R10;

--Question 1. b) viii)
WITH R1 AS
	(
		SELECT sid, pid
		FROM Catalog
	),
	R2 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Red')
	),
	R3 AS
	(
		SELECT pid
		FROM R2
	),
	R4 AS
	(
		SELECT sid
		FROM R1
	),
	R5 AS
	(
		SELECT *
		FROM (R4 INNER JOIN R3)
	),
	R6 AS
	(
		SELECT *
		FROM R5 EXCEPT SELECT * FROM R1
	),
	R7 AS
	(
		SELECT sid
		FROM R6
	),
	R8 AS
	(
		SELECT *
		FROM R4 EXCEPT SELECT * FROM R7
	),
	R9 AS
	(
		SELECT sid, pid
		FROM Catalog
	),
	R10 AS
	(
		SELECT *
		FROM Parts
		WHERE upper(Parts.color) = upper('Green')
	),
	R11 AS
	(
		SELECT pid
		FROM R10
	),
	R12 AS
	(
		SELECT DISTINCT sid
		FROM R9
	),
	R13 AS
	(
		SELECT *
		FROM (R12 INNER JOIN R11)
	),
	R14 AS
	(
		SELECT *
		FROM R13 EXCEPT SELECT * FROM R9
	),
	R15 AS
	(
		SELECT sid
		FROM R14
	),
	R16 AS
	(
		SELECT *
		FROM R12 EXCEPT SELECT * FROM R15
	),
	R17 AS
	(
		SELECT *
		FROM (SELECT * FROM R8 UNION SELECT * FROM R16)
	)
SELECT *
FROM R17;

--Question 1. b) ix)
WITH R1 AS
	(
		SELECT *
		FROM Catalog
	),
	R2 AS
	(
		SELECT *
		FROM Catalog
	),
	R3 AS
	(
		SELECT R1.sid AS sid_1, R1.pid AS pid_1, R1.cost AS cost_1, R2.sid AS sid_2, R2.pid AS pid_2, R2.cost AS cost_2
		FROM R1 INNER JOIN R2
	),
	R4 AS
	(
		SELECT *
		FROM R3
		WHERE (R3.cost_1 > R3.cost_2 AND R3.sid_1 <> R3.sid_2 AND R3.pid_1 = R3.pid_2)
	),
	R5 AS
	(
		SELECT R4.sid_1, R4.sid_2
		FROM R4
	)
SELECT *
FROM R5;

--Question 1. b) x)
WITH R1 AS
	(
		SELECT *
		FROM Catalog
	),
	R2 AS
	(
		SELECT *
		FROM Catalog
	),
	R3 AS
	(
		SELECT R1.sid AS sid_1, R1.pid AS pid_1, R1.cost AS cost_1, R2.sid AS sid_2, R2.pid AS pid_2, R2.cost AS cost_2
		FROM R1 INNER JOIN R2
	),
	R4 AS
	(
		SELECT *
		FROM R3
		WHERE (R3.sid_1 <> R3.sid_2 AND R3.pid_1 = R3.pid_2)
	),
	R5 AS
	(
		SELECT DISTINCT R4.pid_1
		FROM R4
	)
SELECT *
FROM R5;

--Question 1. b) xi)
WITH R1 AS
	(
		SELECT *
		FROM Suppliers
		WHERE upper(Suppliers.sname) = upper('Canada Suppliers')
	),
	R2 AS
	(
		SELECT R1.sid
		FROM R1
	),
	R3 AS
	(
		SELECT *
		FROM R2 NATURAL JOIN Catalog
	),
	R4 AS
	(
		SELECT *
		FROM R3
	),
	R5 AS
	(
		SELECT *
		FROM R4
	),
	R6 AS
	(
		SELECT *
		FROM R4
	),
	R7 AS
	(
		SELECT R5.sid AS sid_5, R5.pid AS pid_5, R5.cost AS cost_5, R6.sid AS sid_6, R6.pid AS pid_6, R6.cost AS cost_6
		FROM R5 INNER JOIN R6
	),
	R8 AS
	(
		SELECT *
		FROM R7
		WHERE cost_5 < cost_6
	),
	R9 AS
	(
		SELECT sid_5, pid_5, cost_5
		FROM R8
	),
	R10 AS
	(
		SELECT *
		FROM R9
	),
	R11 AS
	(
		SELECT *
		FROM (SELECT * FROM R4 EXCEPT SELECT * FROM R10)
	),
	R12 AS
	(
		SELECT R11.pid
		FROM R11
	)
SELECT *
FROM R12;

--Question 1. b) xii)
WITH R1 AS
	(
		SELECT *
		FROM Catalog
		WHERE Catalog.cost <200
	),
	R2 AS
	(
		SELECT R1.sid, R1.pid
		FROM R1
	),
	R3 AS
	(
		SELECT sid
		FROM Suppliers
	),
	R4 AS
	(
		SELECT pid
		FROM R2
	),
	R5 AS
	(
		SELECT *
		FROM (R4 INNER JOIN R3)
	),
	R6 AS
	(
		SELECT *
		FROM R5 EXCEPT SELECT * FROM R2
	),
	R7 AS
	(
		SELECT pid
		FROM R6
	),
	R8 AS
	(
		SELECT *
		FROM R4 EXCEPT SELECT * FROM R7
	)
SELECT *
FROM R8;
