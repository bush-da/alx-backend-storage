-- Script that creates a function SafeDiv that divides the first by
-- the second number or returns 0
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
DETERMINISTIC
BEGIN
    -- checks if the second number is 0
    IF b = 0 THEN
       RETURN 0;
    ELSE
       RETURN a / b;
END$$

DELIMITER ;
