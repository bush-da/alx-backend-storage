-- Script that creates a function to calculate weighted average
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
       IN user_id INT
)
BEGIN
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE weight_avg INT DEFAULT 0;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO weight_avg, total_weight
    FROM corrections c
    JOIN projects p ON p.id = c.project_id
    WHERE c.user_id = user_id

    IF weight_avg > 0 THEN
       SET weight_avg = weight_avg / total_weight;
    ELSE
       SET weight_avg = 0;
    END IF;

    UPDATE users
    SET average_score = weight_avg
    WHERE id = user_id;

END $$

DELIMITER ;

