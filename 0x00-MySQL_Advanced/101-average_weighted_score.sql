-- Script to create procedure ComputeAverageWeightedScoreForUser
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
)
BEGIN
    DECLARE weighted_avg FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the weighted sum of scores and the total weight
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weighted_avg, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id

    -- If the total weight is greater than 0, calculate the average, otherwise set to 0
    IF total_weight > 0 THEN
        SET weighted_avg = weighted_avg / total_weight;
    ELSE
        SET weighted_avg = 0;
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_avg

END$$

DELIMITER ;
