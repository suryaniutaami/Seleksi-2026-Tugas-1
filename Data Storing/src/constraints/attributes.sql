ALTER TABLE workout
ADD CONSTRAINT chk_workout_url
CHECK (workout_url REGEXP '^https://musclewiki\\.com/exercise/[A-Za-z0-9_-]+/?$');

ALTER TABLE program
ADD CONSTRAINT chk_program_url
CHECK (program_url REGEXP '^https://musclewiki\\.com/workout/[A-Za-z0-9_-]+/?$');

ALTER TABLE step
ADD CONSTRAINT chk_step_number
CHECK (step_number > 0);

ALTER TABLE category
ADD CONSTRAINT chk_category_name_not_blank
CHECK (CHAR_LENGTH(TRIM(category_name)) > 0);

ALTER TABLE target_area
ADD CONSTRAINT chk_target_name_not_blank
CHECK (CHAR_LENGTH(TRIM(target_name)) > 0);

ALTER TABLE workout
ADD CONSTRAINT chk_workout_name_not_blank
CHECK (CHAR_LENGTH(TRIM(workout_name)) > 0);

ALTER TABLE step
ADD CONSTRAINT chk_step_description_not_blank
CHECK (CHAR_LENGTH(TRIM(step_description)) > 0);

ALTER TABLE workout_grip
ADD CONSTRAINT chk_grip_not_blank
CHECK (CHAR_LENGTH(TRIM(grip)) > 0);

ALTER TABLE workout_tag
ADD CONSTRAINT chk_tag_not_blank
CHECK (CHAR_LENGTH(TRIM(tag)) > 0);

ALTER TABLE program
ADD CONSTRAINT chk_program_name_not_blank
CHECK (CHAR_LENGTH(TRIM(program_name)) > 0);