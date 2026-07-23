ALTER TABLE workout
ADD CONSTRAINT fk_workout_category
FOREIGN KEY (category_name) 
REFERENCES category(category_name)
ON UPDATE CASCADE
ON DELETE RESTRICT;

ALTER TABLE step
ADD CONSTRAINT fk_workout_step
FOREIGN KEY (workout_name) 
REFERENCES workout(workout_name) 
ON DELETE CASCADE;

ALTER TABLE workout_grip
ADD CONSTRAINT fk_workout_grip
FOREIGN KEY (workout_name) 
REFERENCES workout(workout_name) 
ON DELETE CASCADE;

ALTER TABLE workout_tag
ADD CONSTRAINT fk_workout_tag
FOREIGN KEY (workout_name) 
REFERENCES workout(workout_name)
ON DELETE CASCADE;

ALTER TABLE workout_target
ADD CONSTRAINT fk_workout_target_workout
FOREIGN KEY (workout_name) REFERENCES workout(workout_name)
ON DELETE CASCADE,
ADD CONSTRAINT fk_workout_target_target_area
FOREIGN KEY (target_name) REFERENCES target_area(target_name)
ON DELETE CASCADE;

ALTER TABLE program_workout
ADD CONSTRAINT fk_program_workout_program
FOREIGN KEY (program_name) REFERENCES program(program_name)
ON DELETE CASCADE,
ADD CONSTRAINT fk_program_workout_workout
FOREIGN KEY (workout_name) REFERENCES workout(workout_name)
ON DELETE CASCADE;



