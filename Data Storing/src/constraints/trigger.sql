-- Relational integrity:
-- Ketika memasukkan step_number baru, harus increment dari yang sebelumnya. 
DELIMITER //
CREATE TRIGGER validate_step_number
BEFORE INSERT ON step
FOR EACH ROW
BEGIN
    DECLARE expected_step INT;
    DECLARE step_exists INT;

    SELECT COUNT(*) INTO step_exists
    FROM step
    WHERE workout_name = NEW.workout_name
      AND step_number = NEW.step_number;

    IF step_exists = 0 THEN
        SELECT COALESCE(MAX(step_number), 0) + 1 INTO expected_step
        FROM step
        WHERE workout_name = NEW.workout_name;

        IF NEW.step_number <> expected_step THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Step harus increment dari nomor berikutnya';
        END IF;
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_step_number_update
BEFORE UPDATE ON step
FOR EACH ROW
BEGIN
    IF OLD.workout_name <> NEW.workout_name OR OLD.step_number <> NEW.step_number THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'workout_name dan step_number tidak boleh diubah. Hapus dan insert ulang step secara berurutan';
    END IF;
END//
DELIMITER ;

-- Database integrity:
-- Menjaga aturan antar tabel workout dengan tabel target_area. 
-- Di mana category_name `Recovery` harus memiliki target_type `Joint`,
-- dan sebaliknya category_name selain Recovery harus memiliki target_type `Muscle` 
DELIMITER //
CREATE TRIGGER trg_validate_workout_target
BEFORE INSERT ON workout_target
FOR EACH ROW
BEGIN
    DECLARE v_category_name VARCHAR(100);
    DECLARE v_target_type VARCHAR(20);

    SELECT category_name INTO v_category_name
    FROM workout
    WHERE workout_name = NEW.workout_name;

    SELECT target_type INTO v_target_type
    FROM target_area
    WHERE target_name = NEW.target_name;

    IF v_category_name = 'Recovery'
       AND v_target_type <> 'Joint' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Workout Recovery hanya boleh memiliki target bertipe Joint';
    END IF;

    IF v_category_name <> 'Recovery'
       AND v_target_type <> 'Muscle' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Workout Non-Recovery hanya boleh memiliki target bertipe Muscle';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_validate_workout_target_update
BEFORE UPDATE ON workout_target
FOR EACH ROW
BEGIN
    DECLARE v_category_name VARCHAR(100);
    DECLARE v_target_type VARCHAR(20);

    SELECT category_name INTO v_category_name
    FROM workout
    WHERE workout_name = NEW.workout_name;

    SELECT target_type INTO v_target_type
    FROM target_area
    WHERE target_name = NEW.target_name;

    IF v_category_name = 'Recovery'
       AND v_target_type <> 'Joint' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Workout Recovery hanya boleh memiliki target bertipe Joint';

    ELSEIF v_category_name <> 'Recovery'
       AND v_target_type <> 'Muscle' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Workout non-Recovery hanya boleh memiliki target bertipe Muscle';
    END IF;
END//
DELIMITER ;

-- Database integrity:
-- Program tidak boleh berisi workout dengan difficulty yang lebih tinggi daripada difficulty program.
DELIMITER //
CREATE TRIGGER trg_validate_program_workout_insert
BEFORE INSERT ON program_workout
FOR EACH ROW
BEGIN
    DECLARE v_program_difficulty VARCHAR(20);
    DECLARE v_workout_difficulty VARCHAR(20);
    DECLARE v_program_level INT;
    DECLARE v_workout_level INT;

    SELECT difficulty INTO v_program_difficulty
    FROM program
    WHERE program_name = NEW.program_name;

    SELECT difficulty INTO v_workout_difficulty
    FROM workout
    WHERE workout_name = NEW.workout_name;

    SET v_program_level =
        CASE v_program_difficulty
            WHEN 'Beginner' THEN 1
            WHEN 'Novice' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Advanced' THEN 4
        END;

    SET v_workout_level =
        CASE v_workout_difficulty
            WHEN 'Beginner' THEN 1
            WHEN 'Novice' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Advanced' THEN 4
        END;

    IF v_workout_level > v_program_level THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Difficulty workout tidak boleh lebih tinggi daripada difficulty program';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_validate_program_workout_update
BEFORE UPDATE ON program_workout
FOR EACH ROW
BEGIN
    DECLARE v_program_difficulty VARCHAR(20);
    DECLARE v_workout_difficulty VARCHAR(20);
    DECLARE v_program_level INT;
    DECLARE v_workout_level INT;

    SELECT difficulty INTO v_program_difficulty
    FROM program
    WHERE program_name = NEW.program_name;

    SELECT difficulty INTO v_workout_difficulty
    FROM workout
    WHERE workout_name = NEW.workout_name;

    SET v_program_level =
        CASE v_program_difficulty
            WHEN 'Beginner' THEN 1
            WHEN 'Novice' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Advanced' THEN 4
        END;

    SET v_workout_level =
        CASE v_workout_difficulty
            WHEN 'Beginner' THEN 1
            WHEN 'Novice' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Advanced' THEN 4
        END;

    IF v_workout_level > v_program_level THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Difficulty workout tidak boleh lebih tinggi daripada difficulty program';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_validate_program_difficulty_update
BEFORE UPDATE ON program
FOR EACH ROW
BEGIN
    DECLARE v_new_program_level INT;
    DECLARE v_max_workout_level INT;

    SET v_new_program_level =
        CASE NEW.difficulty
            WHEN 'Beginner' THEN 1
            WHEN 'Novice' THEN 2
            WHEN 'Intermediate' THEN 3
            WHEN 'Advanced' THEN 4
        END;

    SELECT COALESCE(
        MAX(
            CASE w.difficulty
                WHEN 'Beginner' THEN 1
                WHEN 'Novice' THEN 2
                WHEN 'Intermediate' THEN 3
                WHEN 'Advanced' THEN 4
            END
        ),
        0
    )
    INTO v_max_workout_level
    FROM program_workout pw
    JOIN workout w ON w.workout_name = pw.workout_name
    WHERE pw.program_name = OLD.program_name;

    IF v_new_program_level < v_max_workout_level THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Difficulty program tidak boleh lebih rendah dari workout tersulit';
    END IF;
END//
DELIMITER ;