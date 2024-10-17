-- Script that calculate weighted average for all students
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare necessary variables
    DECLARE total_weight FLOAT;
    DECLARE weighted_score FLOAT;

    -- Loop through all users to calculate their weighted average score
    UPDATE users u
    SET u.average_score = (
        -- Calculate weighted score for each user
        SELECT SUM(c.score * p.weight) / SUM(p.weight)
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = u.id
    );
END$$

DELIMITER ;
