from src.helpers.constant import *
from src.seeder.seeder import *

OUTPUT_PATH = DATA_STORING_DIR / "src" / "seed" / "seed.sql"

def main() -> None:
    print("\n--- BUILD SQL SEEDERS ---")

    output: list[str] = []

    output.extend(seed_category())
    output.extend(seed_target_area())
    output.extend(seed_workout())
    output.extend(seed_step())
    output.extend(seed_workout_grip())
    output.extend(seed_workout_tag())
    output.extend(seed_workout_target())
    output.extend(seed_program())
    output.extend(seed_program_workout())

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(output))

    print(f"Total query tersimpan: {len(output)}")
    print(f"Output: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()