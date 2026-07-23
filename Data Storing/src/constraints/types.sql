ALTER TABLE workout_grip
ADD CONSTRAINT chk_workout_grip
CHECK (grip IN ('Overhand', 'Underhand', 'Pinch Grip', 'Rotating', 'Mixed', 'Neutral', 'None'));

ALTER TABLE workout
ADD CONSTRAINT chk_workout_difficulty
CHECK (difficulty IN ('Beginner', 'Novice', 'Intermediate', 'Advanced')),
ADD CONSTRAINT chk_workout_force
CHECK (`force` IN ('Push', 'Hold', 'Pull', 'None')),
ADD CONSTRAINT chk_workout_mechanic
CHECK (mechanic IN ('Isolation', 'Compound', 'None'));

ALTER TABLE workout_target
ADD CONSTRAINT chk_target_role
CHECK (role_target IN ('Primary', 'Secondary', 'Tertiary'));

ALTER TABLE target_area
ADD CONSTRAINT chk_target_type
CHECK (target_type IN ('Muscle', 'Joint'));

ALTER TABLE category
ADD CONSTRAINT chk_category_type
CHECK (category_type IN ('Equipment', 'Exercise Type'));

ALTER TABLE program
ADD CONSTRAINT chk_program_difficulty
CHECK (difficulty IN ('Beginner', 'Novice', 'Intermediate', 'Advanced'));