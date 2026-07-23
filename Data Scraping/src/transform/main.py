from src.helpers.constant import OUTPUT_DIR_PROCESSED, OUTPUT_DIR_RAW
from src.helpers.json_io import read_json, write_json
from src.transform.build_relations import *


def main() -> None:
    print("\n--- BUILD RELATIONAL DATA ---")

    OUTPUT_DIR_PROCESSED.mkdir(parents=True, exist_ok=True)

    filters_raw = read_json(OUTPUT_DIR_RAW / "filters.json")
    target_areas_raw = read_json(OUTPUT_DIR_RAW / "target_areas.json")
    listings_raw = read_json(OUTPUT_DIR_RAW / "listings.json")
    workouts_raw = read_json(OUTPUT_DIR_RAW / "workouts.json")
    programs_raw = read_json(OUTPUT_DIR_RAW / "programs.json")
    program_workouts = read_json(OUTPUT_DIR_RAW / "program_workouts.json")

    categories = build_categories(filters_raw)
    target_areas = build_target_areas(target_areas_raw)
    workouts = build_workouts(workouts_raw, listings_raw)
    workout_grips = build_workout_grips(workouts_raw)
    steps = build_steps(workouts_raw)
    workout_tags = build_workout_tags(workouts_raw)
    workout_targets = build_workout_targets(workouts_raw, listings_raw)
    programs = build_programs(programs_raw)
    program_workouts = build_program_workouts(program_workouts, workouts)
    

    write_json(OUTPUT_DIR_PROCESSED / "categories.json", categories)
    write_json(OUTPUT_DIR_PROCESSED / "target_areas.json", target_areas)
    write_json(OUTPUT_DIR_PROCESSED / "workouts.json", workouts)
    write_json(OUTPUT_DIR_PROCESSED / "workout_grips.json", workout_grips)
    write_json(OUTPUT_DIR_PROCESSED / "steps.json", steps)
    write_json(OUTPUT_DIR_PROCESSED / "workout_tags.json", workout_tags)
    write_json(OUTPUT_DIR_PROCESSED / "workout_targets.json", workout_targets)
    write_json(OUTPUT_DIR_PROCESSED / "programs.json", programs)
    write_json(OUTPUT_DIR_PROCESSED / "program_workouts.json", program_workouts)

    print(f"Category: {len(categories)}")
    print(f"TargetArea: {len(target_areas)}")
    print(f"Workout: {len(workouts)}")
    print(f"WorkoutGrip: {len(workout_grips)}")
    print(f"Step: {len(steps)}")
    print(f"WorkoutTag: {len(workout_tags)}")
    print(f"WorkoutTarget: {len(workout_targets)}")
    print(f"Program: {len(programs)}")
    print(f"ProgramWorkout: {len(program_workouts)}")
    print(f"\nData processed tersimpan di: {OUTPUT_DIR_PROCESSED}")


if __name__ == "__main__":
    main()