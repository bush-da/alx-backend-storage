-- Script to create procedure ComputeAverageWeightedScoreForUser
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser()
BEGIN
    DECLARE done FLOAT DEFAULT 0;
    DECLARE user_id INT;

    DECLARE user_cursor CURSOR FOR
    SELECT id FROM users;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1

    OPEN user_cursor;


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
