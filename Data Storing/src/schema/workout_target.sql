CREATE TABLE IF NOT EXISTS workout_target (
    workout_name VARCHAR(255) NOT NULL,
    target_name VARCHAR(100) NOT NULL,
    role_target VARCHAR(20),
    
    PRIMARY KEY (workout_name, target_name)
);