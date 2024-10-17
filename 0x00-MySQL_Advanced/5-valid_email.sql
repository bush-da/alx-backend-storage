-- Script that creates a trigger to reset valid_email row when email changes
DROP TRIGGER IF EXISTS reset_valid_email;

DELIMITER $$

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has changed
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END$$

DELIMITER ;
