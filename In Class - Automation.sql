CREATE TABLE employee_salary_log (
    log_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user VARCHAR(50),
    event_time DATETIME,
    old_value FLOAT,
    new_value FLOAT
);


-- TRIGGER
-- create trigger
DELIMITER $$
CREATE TRIGGER  after_employee_salary_update
    AFTER UPDATE ON Employee
    FOR EACH ROW
    BEGIN
        IF NEW.salary != OLD.salary THEN
            INSERT INTO employee_salary_log(user, event_time, old_value, new_value)
                -- stores current user logged in, current time, old salary, new salary
                VALUES (USER(), NOW(), OLD.salary, NEW.salary);
        END IF;
    END$$

-- test out trigger
UPDATE Employee
SET salary = 1000000
WHERE employee_id = 60000;


-- STORED PROCEDURE
-- build stored procedure to fire someone
DELIMITER $$
CREATE PROCEDURE terminate_employee(
    IN user_id INT,
    OUT pto_paid_out INT
)
BEGIN
    UPDATE Department
    SET manager = NULL
    WHERE manager = user_id;

    SELECT pto_accrued INTO pto_paid_out
    FROM Employee
    WHERE employee_id = user_id;

    UPDATE Employee
    SET active_status = false,
        salary = 0,
        term_date = CAST(NOW() AS DATETIME ),
        weekly_hours = 0,
        pto_accrued = 0
    WHERE employee_id = user_id;
END$$

-- create new employee to fire
INSERT INTO Employee VALUES
    (NULL, 'Roger', 'BadGuy', 'Evil Dude', NULL, NULL, 1,
     CAST(NOW() AS DATETIME ), NULL, true, 100000, 'PART-TIME', 20, 50);

SELECT employee_id INTO @new_id
FROM Employee
ORDER BY employee_id DESC
LIMIT 1;

CALL terminate_employee(@new_id, @pto_out);
SELECT @pto_out AS pto_paid;

SHOW PROCEDURE STATUS;

-- FUNCTIONS
-- create a function to return how many direct reports some employee has as a manager
DELIMITER $$
CREATE FUNCTION get_direct_report_count(user_id INT)
RETURNS INT DETERMINISTIC
    BEGIN
        DECLARE direct_report_count INT;
        SELECT COUNT(*) INTO direct_report_count
        FROM Employee
        INNER JOIN Department
            ON Employee.department = Department.department_id
        WHERE Department.manager = user_id
        OR (user_ID IS NULL AND Department.manager IS NULL);
        RETURN direct_report_count;
    END$$


SELECT employee_id, first_name, last_name,
       get_direct_report_count(employee_id) AS direct_reports
FROM Employee
WHERE active_status = true;


-- EVENTS
SHOW PROCESSLIST;
SET GLOBAL event_scheduler = ON;

-- create table event for employee manager audit
CREATE TABLE employee_manager_audit (
    recorded_at DATETIME,
    employee_with_no_manager INT
);

SELECT get_direct_report_count(NULL);

CREATE EVENT audit_employees_with_no_manager
ON SCHEDULE
    -- run the event 5 seconds in the future upon creating
    AT CURRENT_TIMESTAMP + INTERVAL 5 SECOND
DO
    INSERT INTO employee_manager_audit VALUES
        (NOW(), get_direct_report_count(NULL));


