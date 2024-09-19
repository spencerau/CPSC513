SELECT USER, HOST
FROM mysql.user;

SHOW GRANTS
FOR 'dev_user'@'localhost';

SHOW GRANTS
FOR 'developer';

-- 1. A user from Human Resources would like to perform some audits on our employees and departments.
-- Create for them a view that contains all information about employees and their departments in one resulting
-- table output. Create a new user at localhost and grant them only access to select from this view.

-- create view for HR
CREATE VIEW HR_Audit AS
SELECT *
FROM Employee e
INNER JOIN Department d
    ON e.department = d.department_id;
-- create new user for HR
CREATE USER 'hr_user'@'localhost'
IDENTIFIED BY 'CPSC513!';
-- update permissions to access view
GRANT SELECT
ON hr_audit
TO 'hr_user'@'localhost';


-- 2. Log in as this user account and attempt to select from the view you created. What is the error/output
-- that occurs if any? (Remember to run the command USE MyCompany; first if running in command prompt/terminal
-- to select the correct database)

-- on CLI:
-- mysql -u hr_user -p
-- USE mycompany
-- QUERY SELECT * FROM hr_audit is successful
SELECT *
FROM hr_audit;

-- 3. Attempt to insert a new department to the Department table. What is the error/output that occurs if any?
INSERT INTO Department VALUES
    ('dept_name', 99, 99);

-- [42000][1142] INSERT command denied to user 'hr_user'@'localhost' for table 'department'


-- 4. Log back into your root user and grant the HR user all access to the employee and department tables explicitly,
-- and revoke their access to the view you created in part 1.

-- grant access to Employee Table
GRANT ALL
ON Employee
TO 'hr_user'@'localhost';
-- grant access to Department Table
GRANT ALL
ON Department
TO 'hr_user'@'localhost';
-- revoke access to VIEW hr_audit
REVOKE SELECT
ON hr_audit
FROM 'hr_user'@'localhost';


-- 5. Another user from Finance would like to be able to perform some data analysis on our sales based on location.
-- Create for them a view that ONLY contains information about our sales and which location they occurred in. Return no
-- information about employees or departments within this view. Create a user account for this user on localhost and
-- grant them the access to select this view.

-- create Finance_Sales VIEW
CREATE VIEW Finance_Sales AS
    SELECT s.sale_id, s.item_quantity, s.sale_total, l.*
    FROM Sales s
    INNER JOIN Employee e
        ON s.submitted_by = CONCAT(e.first_name, ' ', e.last_name)
    INNER JOIN Department d
        ON e.department = d.department_id
    INNER JOIN location l
        ON d.location = l.location_id;
-- create new user for Finance
CREATE USER 'finance_user'@'localhost'
IDENTIFIED BY 'CPSC513!';
-- update permissions to select view
GRANT SELECT
ON Finance_Sales
TO 'finance_user'@'localhost';
-- test out on finance_user
SELECT *
FROM Finance_Sales;


-- 6. A team of developers is building us a front end application that will allow employees to input sales.
-- Create a role that would allow them to perform all CRUD operations on our existing tables but not to create
-- any new tables or other database objects.

-- create developer role
CREATE ROLE 'developer';
-- grant CRUD permissions
GRANT USAGE, INSERT, SELECT, UPDATE, DELETE
ON mycompany.*
TO 'developer';

DROP USER 'dev_user'@'localhost';


-- 7. Create a new developer user and assign them to the new developer role.

-- create new user for developer and assign developer role to dev_user
CREATE USER 'dev_user'@'localhost'
IDENTIFIED BY 'CPSC513!'
DEFAULT ROLE 'developer';


-- 8. Show all granted access for the new developer account you created. What results/errors are returned?

SHOW GRANTS
FOR 'dev_user'@'localhost';
-- it returns:
-- GRANT USAGE ON *.* TO `dev_user`@`localhost`
-- GRANT `developer`@`%` TO `dev_user`@`localhost`


-- 9. Now, show all users that currently exist in the system. What is returned?
SELECT USER, HOST
FROM mysql.user;

-- when running as dev_user:
-- SELECT command denied to user 'dev_user'@'localhost' for table 'user'

-- when running as root:
# developer,%
# dev_user,localhost
# finance_user,localhost
# hr_user,localhost
# mysql.infoschema,localhost
# mysql.session,localhost
# mysql.sys,localhost
# root,localhost







