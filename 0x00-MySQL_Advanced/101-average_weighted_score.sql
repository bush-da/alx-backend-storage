-- Script to create procedure ComputeAverageWeightedScoreForUsers
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    
    -- Declare a cursor for iterating through all users
    DECLARE user_cursor CURSOR FOR 
    SELECT id FROM users;
    
    -- Declare a handler to detect when the cursor reaches the end
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    -- Open the cursor
    OPEN user_cursor;
    
    -- Cursor loop to iterate through all users
    read_loop: LOOP
        -- Fetch the next user_id from the cursor
        FETCH user_cursor INTO user_id;
        
        -- If there are no more rows, exit the loop
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Call the ComputeAverageWeightedScoreForUser for each user
        CALL ComputeAverageWeightedScoreForUser(user_id);

    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END$$

DELIMITER ;
