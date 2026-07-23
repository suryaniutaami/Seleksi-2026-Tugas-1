from pathlib import Path

DATA_STORING_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = DATA_STORING_DIR.parent
DATA_SCRAPING_DIR = PROJECT_ROOT / "Data Scraping"

INPUT_DIR = DATA_SCRAPING_DIR / "data" / "processed"
OUTPUT_DIR = DATA_STORING_DIR / "export"

CATEGORY_PATH = INPUT_DIR / "categories.json"
TARGET_AREA_PATH = INPUT_DIR / "target_areas.json"
WORKOUT_PATH = INPUT_DIR / "workouts.json"
WORKOUT_GRIP_PATH = INPUT_DIR / "workout_grips.json"
STEP_PATH = INPUT_DIR / "steps.json"
WORKOUT_TAG_PATH = INPUT_DIR / "workout_tags.json"
WORKOUT_TARGET_PATH = INPUT_DIR / "workout_targets.json"
PROGRAM_PATH = INPUT_DIR / "programs.json"
PROGRAM_WORKOUT_PATH = INPUT_DIR / "program_workouts.json"