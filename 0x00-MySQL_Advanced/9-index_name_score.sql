-- Script that creates index on table names the first name
-- and score
CREATE INDEX idx_name_first_score ON names (name(1), score);
