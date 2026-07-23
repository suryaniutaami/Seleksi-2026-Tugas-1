-- Cukup jalankan file ini sekali di awal, pastikan seed/ sudah berisi seed.sql
DROP DATABASE IF EXISTS exercise;
CREATE DATABASE exercise;
USE exercise;

-- Schema
SOURCE ./schema/category.sql;
SOURCE ./schema/target_area.sql;
SOURCE ./schema/workout.sql;
SOURCE ./schema/step.sql;
SOURCE ./schema/workout_grip.sql;
SOURCE ./schema/workout_tag.sql;
SOURCE ./schema/workout_target.sql;
SOURCE ./schema/program.sql;
SOURCE ./schema/program_workout.sql;

-- -- Integrity Constraints
SOURCE ./constraints/types.sql;
SOURCE ./constraints/attributes.sql;
SOURCE ./constraints/trigger.sql;
SOURCE ./constraints/referential.sql;

-- Seed data
SOURCE ./seed/seed.sql;