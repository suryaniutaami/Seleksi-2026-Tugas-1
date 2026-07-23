CREATE TABLE IF NOT EXISTS workout_grip (
    workout_name VARCHAR(255) NOT NULL,
    grip VARCHAR(20) NOT NULL,
    
    PRIMARY KEY (workout_name, grip)
);