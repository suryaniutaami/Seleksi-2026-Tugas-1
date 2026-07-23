CREATE TABLE IF NOT EXISTS step (
    workout_name VARCHAR(255) NOT NULL,
    step_number INT NOT NULL,
    step_description TEXT NOT NULL,
    
    PRIMARY KEY (workout_name, step_number)
);