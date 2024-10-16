-- script that make items tables item quantity decrease
-- when ordered item inserted in order table
DROP TRIGGER IF EXISTS decrease_item_quantity;

CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE items.name = NEW.item_name
END;
