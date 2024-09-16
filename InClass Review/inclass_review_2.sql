-- query to return total # of items we have sold on sales
SELECT SUM(item_quantity) AS TotalItemsSold
FROM Sales;

-- query to tell me how many dollars of sales each employee_id has sold.
SELECT employee_id, SUM(sale_total)
FROM Sales
INNER JOIN Employee
        ON Sales.submitted_by = CONCAT(Employee.first_name, ' ', Employee.last_name)
GROUP BY employee_id;

--
SELECT e.employee_id, e.first_name, e.last_name, SUM(s.sale_total) AS Sale_Total
FROM Sales s
INNER JOIN Employee e
    ON s.submitted_by = CONCAT(e.first_name, ' ', e.last_name)
GROUP BY e.employee_id;

# SELECT attribute, COUNT(*) AS RecordCount
# FROM table
# GROUP BY attribute
# HAVING RecordCount > 10

-- query to show me the first name of all employees with more than one sale
SELECT e.first_name, COUNT(*) AS countSales
FROM Sales s
INNER JOIN Employee e
    ON s.submitted_by = CONCAT(e.first_name, ' ', e.last_name)
GROUP BY e.employee_id
HAVING countSales > 1


# In this example, we are getting all sales made by active
# employees. We are only joining with employee to be able to filter
# on the active status value.
SELECT s.sale_id
FROM Sales s
INNER JOIN Employee e
    ON e.employee_id = s.submitted_by
WHERE e.active_status = TRUE;

# Inner joins are much more computationally complex than two
# select statements. This is now a more optimized query and will run quicker.
SELECT s.sale_id
FROM Sales s
WHERE s.submitted_by IN (
    SELECT CONCAT(e.first_name, ' ', e.last_name)
    FROM Employee e
    WHERE active_status = TRUE
);

# MySQL does not support full outer joins using common syntax.
# To emulate the same functionality, we must union a left join and a right join.
# SELECT X
# FROM table1
# LEFT JOIN table2
# UNION
# SELECT X
# FROM table1
# RIGHT JOIN table2;

# Say we wanted to get all employees and their departments.
# We could turn this into a view and never have to type it again:
CREATE VIEW Employee_Departments AS
SELECT e.first_name, e.last_name, d.department_name
FROM Employee e
INNER JOIN Department d
    ON e.department = d.department_id;

SELECT *
FROM Employee_Departments;