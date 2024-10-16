-- Drop the trigger if it exists (for development purposes)
DROP TRIGGER IF EXISTS decrease_item_quantity;

-- Change the delimiter to $$ to allow for multiple statements
DELIMITER $$

-- Create a trigger that executes after an insert on the orders table
CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$

-- Change the delimiter back to semicolon
DELIMITER ;
