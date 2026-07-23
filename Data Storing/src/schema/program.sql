CREATE TABLE IF NOT EXISTS program (
    program_name VARCHAR(100) NOT NULL,
    program_url VARCHAR(255) UNIQUE NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    goal VARCHAR(20) NOT NULL,
    program_description TEXT,
    
    PRIMARY KEY (program_name)
);