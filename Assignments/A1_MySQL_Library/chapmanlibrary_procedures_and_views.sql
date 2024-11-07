DELIMITER $$
CREATE PROCEDURE check_in_book(IN u_id INT, IN i_id INT, OUT late_fee_due FLOAT)
BEGIN
    DECLARE curr_late_fee_daily FLOAT;
    DECLARE curr_return_date DATE;
    DECLARE curr_checkout_duration INT;
    DECLARE curr_late_fee FLOAT;
    DECLARE curr_payment_outstanding BOOL;

    SET curr_late_fee_daily = (SELECT late_fee_daily FROM Inventory WHERE inventory_id = i_id);
    SET curr_return_date = CAST(NOW() AS DATE);
    SET curr_checkout_duration = (SELECT DATEDIFF(curr_return_date, checkout_date)
                      FROM Checkouts
                      WHERE user_id = u_id
                        AND inventory_id = i_id
                        AND is_returned = false);
    IF curr_checkout_duration > 14 THEN
        SET curr_late_fee = curr_late_fee_daily * curr_checkout_duration;
        SET curr_payment_outstanding = true;
    ELSE
        SET curr_late_fee = 0;
        SET curr_payment_outstanding = false;
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

    SELECT ROUND(curr_late_fee, 2) INTO late_fee_due;
END$$

DELIMITER $$
CREATE PROCEDURE check_out_book(IN u_id INT, IN isbn_in INT, OUT message TEXT)
BEGIN
    DECLARE curr_inventory_id INT;

    SELECT Inventory.inventory_id INTO curr_inventory_id
    FROM Inventory
    INNER JOIN Checkouts
    ON Inventory.inventory_id = Checkouts.inventory_id
    WHERE Inventory.isbn = isbn_in
    AND Checkouts.is_returned = true
    LIMIT 1;

    IF curr_inventory_id IS NULL THEN
        SET message = 'Book not available at this time';
    ELSE
        INSERT INTO Checkouts(inventory_id, user_id, checkout_date, checkout_duration,
            est_return_date, actual_return_date, is_returned, total_late_fee, payment_outstanding)
        VALUES (curr_inventory_id, u_id, CAST(NOW() AS DATE), NULL,
                CAST(NOW() AS DATE) + INTERVAL 14 DAY, NULL, false, NULL, false);
        SET message = CONCAT('Inventory item ', curr_inventory_id, ' checked out to user ', u_id);
    END IF;
END$$

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