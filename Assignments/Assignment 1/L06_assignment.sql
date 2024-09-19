-- name and info go here
-- Spencer Au
-- CPSC 513 - Database Implementation

-- 1. Create a query to return the most popular 10 books based on number of checkouts
SELECT b.title, COUNT(c.inventory_id) AS Num_Checkouts
FROM books b
INNER JOIN inventory i
    ON b.isbn = i.isbn
INNER JOIN checkouts c
    ON i.inventory_id = c.inventory_id
GROUP BY c.inventory_id
ORDER BY COUNT(c.inventory_id) DESC
LIMIT 10;


-- 2. Create a query to return the most popular 10 books based on days checked out
SELECT b.title, SUM(c.checkout_duration) AS Days_Checked_Out
FROM books b
INNER JOIN inventory i
    ON b.isbn = i.isbn
INNER JOIN checkouts c
    ON i.inventory_id = c.inventory_id
GROUP BY c.inventory_id
ORDER BY SUM(c.checkout_duration) DESC
LIMIT 10;


-- create a view that shows Inventory_ID with corresponding Days_Checked_Out
CREATE VIEW checkout_dur_per_book AS
    SELECT i.inventory_id, SUM(c.checkout_duration) AS Days_Checked_Out
    FROM inventory i
    INNER JOIN checkouts c
        ON i.inventory_id = c.inventory_id
    GROUP BY c.inventory_id;

SELECT *
FROM checkout_dur_per_book;


-- 3. Our librarians have indicated they want the system to automatically update
-- the physical condition of books in stock based off of how many days it has
-- been checked out. Our system has an existing stored procedure to check books
-- back in. Modify this stored procedure to update the physical condition of the
-- inventory item every time an item is turned back in with the following params
--     0-100 days: New
--     100-500 days: Good
--     500-1000 days: Fair
--     1000+ days: Poor

-- existing stored procedure
DELIMITER $$
CREATE PROCEDURE check_in_book_fixed(IN u_id INT, IN i_id INT, OUT late_fee_due FLOAT)
BEGIN
    DECLARE curr_late_fee_daily FLOAT;
    DECLARE curr_return_date DATE;
    DECLARE curr_checkout_duration INT;
    DECLARE curr_late_fee FLOAT;
    DECLARE curr_payment_outstanding BOOL;
    DECLARE p_condition VARCHAR(10);
    DECLARE total_checkout_duration INT;

    SET curr_late_fee_daily = (SELECT late_fee_daily FROM Inventory WHERE inventory_id = i_id);
    SET curr_return_date = CAST(NOW() AS DATE);
    SET curr_checkout_duration = (SELECT DATEDIFF(curr_return_date, checkout_date)
                      FROM Checkouts
                      WHERE user_id = u_id
                        AND inventory_id = i_id
                        AND is_returned = false);

    SET total_checkout_duration = ((SELECT Days_Checked_Out
                                FROM checkout_dur_per_book
                                WHERE inventory_id = i_id) + curr_checkout_duration);

    IF curr_checkout_duration > 14 THEN
        SET curr_late_fee = curr_late_fee_daily * curr_checkout_duration;
        SET curr_payment_outstanding = true;
    ELSE
        SET curr_late_fee = 0;
        SET curr_payment_outstanding = false;
    END IF;

    IF total_checkout_duration BETWEEN 0 AND 100 THEN
        SET p_condition = 'New';
    ELSEIF total_checkout_duration BETWEEN 100 AND 500 THEN
        SET p_condition = 'Good';
    ELSEIF total_checkout_duration BETWEEN 500 AND 1000 THEN
        SET p_condition = 'Fair';
    ELSEIF total_checkout_duration > 1000 THEN
        SET p_condition = 'Poor';
    END IF;

    UPDATE Checkouts
    SET actual_return_date = curr_return_date,
        is_returned = true,
        total_late_fee = curr_late_fee,
        payment_outstanding = curr_payment_outstanding,
        checkout_duration = curr_checkout_duration
    WHERE inventory_id = i_id
    AND user_id = u_id
    AND is_returned = false;

    UPDATE inventory
    SET physical_condition = p_condition
    WHERE inventory_id = i_id;

    SELECT ROUND(curr_late_fee, 2) INTO late_fee_due;
END$$


-- 4. Librarians are asking for more tools to be able to audit worn and
-- under-used books. Using your own best judgement of the data in this database,
-- create two views whose results a librarian could use to be able to perform
-- these audits (under used books, worn books). Explain your reasoning on why
-- you picked the queries to define these views.

-- view that returns a book, when it was acquired, and how many times it has been checked out
-- query so that a person can see how "popular" a book is depending on how many times it has been checked-out
-- vs when it was acquired
CREATE VIEW books_dates_checkout_num AS
    SELECT b.isbn, b.title, b.author, i.purchase_date, COUNT(c.inventory_id) AS Checkouts
    FROM inventory i
    INNER JOIN books b
        ON i.isbn = b.isbn
    INNER JOIN checkouts c
        ON i.inventory_id = c.inventory_id
    GROUP BY c.inventory_id;

-- testing out view
SELECT *
FROM books_dates_checkout_num;

-- view that gives the number of items that a user has checked out
-- can possibly be used to see how many items a user has checked out,
-- implement a max number of items they can check out, etc
CREATE VIEW num_books_user_checked_out AS
    SELECT u.user_id, u.username, u.email, u.phone_number, COUNT(c.user_id) AS BooksCheckedOut
    FROM checkouts c
    INNER JOIN users u
        ON c.user_id = u.user_id
    WHERE c.is_returned = 0
    GROUP BY c.user_id;

-- test out view
SELECT *
FROM num_books_user_checked_out;


-- 5. Create a function that will return the total amount of money a user owes
-- in late fees for all of their book checkouts.
-- Create a query that will display the user accounts with the top ten highest late fees owed,
-- using this function

-- create function
DELIMITER $$
CREATE FUNCTION get_total_amount_owed (u_id INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE total_amount_owed FLOAT;
    SELECT SUM(c.total_late_fee) INTO total_amount_owed
    FROM checkouts c
    WHERE c.user_id = u_id AND c.payment_outstanding = 1;
    RETURN total_amount_owed;
END$$

-- create a query using that function
#CREATE VIEW
SELECT u.*, get_total_amount_owed(u.user_id) AS Total_Amount_Owed
FROM users u
ORDER BY Total_Amount_Owed DESC
LIMIT 10;


-- 6. A user has informed us that they are running a view, publisher_audit, frequently
-- and it is running quite slow. Take a look at the view's definition below and
-- explain why you believe it may be running slow. Create a new proposed view
-- that you believe would be more optimized and still give the same result, and
-- explain your reasoning

-- original view
CREATE VIEW publisher_audit AS
SELECT distinct pubbies.publisher_name, count(*) AS answer
FROM Users q, Checkouts z
INNER JOIN chapmanlibrary.inventory f on z.inventory_id = f.inventory_id
-- CROSS JOIN users us_users maybe
INNER JOIN Books lol ON lol.isbn = f.isbn
cross join Publishers pubbies
WHERE z.inventory_id = z.inventory_id
AND pubbies.publisher_id = lol.publisher
and z.user_id IN (
    SELECT users_from_checkout_matching.user_id
    FROM Users users_from_checkout_matching
    INNER JOIN Checkouts C on users_from_checkout_matching.user_id = C.user_id
    CROSS JOIN books book, chapmanlibrary.inventory i, books b
    ) -- ??? -- delete later??? maybe doesn't work without??
AND q.user_id = z.user_id
GROUP BY pubbies.publisher_id
order by answer DESC;

-- original query seems to have a lot of (unnecessary) joins alongside tables that aren't needed, as well as sub-query
-- optimized view assuming we want the number of checkouts per publisher
CREATE VIEW checkouts_per_publisher_optimized AS
    SELECT p.publisher_name, COUNT(c.inventory_id) AS Checkout_Duration
    FROM publishers p
    INNER JOIN books b
        ON p.publisher_id = b.publisher
    INNER JOIN inventory i
        ON b.isbn = i.isbn
    INNER JOIN checkouts c
        ON i.inventory_id = c.inventory_id
    GROUP BY p.publisher_id
    ORDER BY Checkout_Duration DESC;


-- 6a. Run your proposed view in datagrip and observe its execution time on the output
-- tab. Is it actually faster than the existing solution? By how much?

-- optimized version: 500 rows retrieved starting from 1 in 287 ms (execution: 279 ms, fetching: 8 ms)
-- original version: 500 rows retrieved starting from 1 in 4 s 222 ms (execution: 4 s 212 ms, fetching: 10 ms)
-- the optimized version is significantly faster at over 4 sec (14.71x as fast)

