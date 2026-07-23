CREATE TABLE IF NOT EXISTS program_workout (
    program_name VARCHAR(100) NOT NULL,
    workout_name VARCHAR(100) NOT NULL,
    order_number INT NOT NULL,
    duration VARCHAR(20),
    
    PRIMARY KEY (program_name, workout_name)
);