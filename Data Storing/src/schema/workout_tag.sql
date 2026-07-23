CREATE TABLE IF NOT EXISTS workout_tag (
    workout_name VARCHAR(255) NOT NULL,
    tag VARCHAR(100) NOT NULL,
    
    PRIMARY KEY (workout_name, tag)
);