CREATE TABLE IF NOT EXISTS workout (
    workout_name VARCHAR(100) NOT NULL,
    workout_url VARCHAR(255) UNIQUE NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    `force` VARCHAR(20),
    mechanic VARCHAR(20),
    category_name VARCHAR(100) NOT NULL,
    
    PRIMARY KEY (workout_name)
);