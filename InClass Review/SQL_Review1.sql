-- Q1
CREATE TABLE Sales (
    sale_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    item_quantity INT,
    submitted_by VARCHAR(30),
    # making a sale total as float might be better
    sale_total DECIMAL (10, 2)
    # add a foreign key
    # FOREIGN KEY (submitted_by) REFERENCES Employee(employee_id)
);

ALTER TABLE Sales AUTO_INCREMENT = 230000;
ALTER TABLE Sales (submitted_by) REFERENCES E

-- Q2
INSERT INTO Sales VALUES
    (NULL, 5, 'Sierra Clibourne', 29.99),
    (NULL, 2, 'Alex Smith', 34.95),
    (NULL, 1, 'Harris Johnson', 100.92),
    (NULL, 1, 'Alex Smith', 22.45),
    (NULL, 1, 'Alex Smith', 10.03);

SELECT * FROM Sales;

-- Q3.a
SELECT sale_id, item_quantity, submitted_by AS Employee, sale_total, location_name AS Location
FROM Sales
    INNER JOIN Employee
        ON Sales.submitted_by = CONCAT(Employee.first_name, ' ', Employee.last_name)
    INNER JOIN Department
        ON Employee.department = Department.department_id
    INNER JOIN location
        ON Department.location = location.location_id;

-- Q3.b
SELECT *, (sale_total/item_quantity) AS AveragePrice
FROM Sales
ORDER BY AveragePrice DESC;

-- Q3.c
SELECT department_name as DepartmentName
FROM Sales
    INNER JOIN Employee
        ON Sales.submitted_by = CONCAT(Employee.first_name, ' ', Employee.last_name)
    INNER JOIN Department
        ON Employee.department = Department.department_id
ORDER BY sale_total DESC
LIMIT 1

