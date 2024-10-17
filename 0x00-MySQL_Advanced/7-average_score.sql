-- A Procedure that computes average score for users
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser $$

CREATE PROCEDURE ComputeAverageScoreForUser(
       IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate the average score for the given user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Set average score for the given user
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;

END $$

DELIMITER ;
