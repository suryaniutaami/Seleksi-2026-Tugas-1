from typing import Any
from src.helpers.constant import *
from src.helpers.json_io import *
from src.transform.normalize import *
from src.transform.deduplicate import *
from src.transform.parse import *

# --- TABEL Workout ---
def build_workouts(workouts_raw: list[dict], listings_raw: list[dict]) -> list[dict]:
    workouts: list[dict] = []
    workout_category_map = build_workout_category_map(listings_raw)

    for raw_workout in workouts_raw:
        name = raw_workout.get("name")
        detail_url = raw_workout.get("detail_url")
        info = raw_workout.get("info", {})

        if name is None or detail_url is None:
            continue

        workouts.append(
            {
                "name": name,
                "url": detail_url,
                "difficulty": info.get("difficulty"),
                "mechanic": info.get("mechanic"),
                "force": info.get("force"),
                "category_name": workout_category_map.get(name),
            }
        )

    return deduplicate_by_keys(workouts, ("name",))

# --- TABEL TargetArea ---
def build_target_areas(target_areas_raw: list[dict]) -> list[dict]:
    target_areas: list[dict] = []

    for raw_target in target_areas_raw:
        name = normalize_target_name(raw_target.get("name"))
        target_type = normalize_target_type(raw_target.get("class"))

        if name is None or target_type is None:
            continue

        target_areas.append(
            {
                "name": name,
                "type": target_type,
            }
        )

    return deduplicate_by_keys(target_areas, ("name", "type"))

# --- TABEL WorkoutTarget ---
def build_workout_targets(
    workouts_raw: list[dict],
    listings_raw: list[dict],
) -> list[dict]:
    workout_targets: list[dict] = []

    workout_target_map = build_workout_target_map(listings_raw)
    workout_role_map = build_workout_role_map(workouts_raw)

    for raw_workout in workouts_raw:
        workout_name = raw_workout.get("name")

        workout_name = workout_name.strip()

        if not workout_name:
            continue

        target_names = workout_target_map.get(
            workout_name,
            set(),
        )

        for target_name in target_names:
            role = workout_role_map.get(
                (workout_name, target_name)
            )

            workout_targets.append(
                {
                    "workout_name": workout_name,
                    "target_area_name": target_name,
                    "role": role,
                }
            )

    return deduplicate_by_keys(
        workout_targets,
        ("workout_name", "target_area_name"),
    )

# --- TABEL Category ---
def build_categories(filters_raw: list[dict]) -> list[dict]:
    categories: list[dict] = []

    for raw_filter in filters_raw:
        name = raw_filter.get("name")
        filter_id = raw_filter.get("scrape_metadata", {}).get("filter_id")

        if name is None or filter_id is None:
            continue

        category_type = "Exercise Type" if filter_id in EXERCISE_TYPE_IDS else "Equipment"

        categories.append(
            {
                "name": name,
                "type": category_type,
            }
        )

    return deduplicate_by_keys(categories, ("name",))

# --- TABEL WorkoutGrip ---
def build_workout_grips(workouts_raw: list[dict]) -> list[dict]:
    workout_grips: list[dict] = []

    for raw_workout in workouts_raw:
        name = raw_workout.get("name")
        info = raw_workout.get("info", {})

        if not name:
            continue

        grips = parse_grips(info.get("grips"))

        for grip in grips:
            workout_grips.append(
                {
                    "workout_name": name,
                    "grip": grip,
                }
            )

    return deduplicate_by_keys(workout_grips, ("workout_name", "grip"))

# --- TABEL Step ---
def build_steps(workouts_raw: list[dict]) -> list[dict]:
    steps: list[dict] = []

    for raw_workout in workouts_raw:
        name = raw_workout.get("name")
        raw_steps = raw_workout.get("step", [])
        if name is None:
            continue

        for raw_step in raw_steps:
            number = raw_step.get("no")
            description = raw_step.get("description")

            if not isinstance(number, int) or number <= 0 or description is None:
                continue

            steps.append(
                {
                    "workout_name": name,
                    "no": number,
                    "description": description,
                }
            )

    return deduplicate_by_keys(steps, ("workout_name", "no"))

# --- TABEL WorkoutTag ---
def build_workout_tags(workouts_raw: list[dict]) -> list[dict]:
    workout_tags: list[dict] = []

    for raw_workout in workouts_raw:
        name = raw_workout.get("name")
        raw_tags = raw_workout.get("tag", [])

        if name is None:
            continue

        for raw_tag in raw_tags:
            tag_name = raw_tag.get("tag")
            tag_name = normalize_tag_name(tag_name)

            if tag_name is None:
                continue

            workout_tags.append(
                {
                    "workout_name": name,
                    "tag": tag_name,
                }
            )

    return deduplicate_by_keys(workout_tags, ("workout_name", "tag"))

# --- TABEL Program ---
def build_programs(programs_raw: list[dict]) -> list[dict]:
    workout_programs: list[dict] = []

    for raw_program in programs_raw:
        name = raw_program.get("name")

        if name is None:
            continue
        name = normalize_program_name(name)
        url = raw_program.get("detail_url")
        difficulty = raw_program.get("difficulty")
        goal = raw_program.get("goal")
        description = raw_program.get("description")

        workout_programs.append(
            {
                "name": name,
                "url": url,
                "difficulty": difficulty,
                "goal": goal,
                "description": description
            }
        )

    return deduplicate_by_keys(workout_programs, ("name",))

# --- TABEL ProgramWorkout ---
def build_program_workouts(programs_workout_raw: list[dict], workouts: list[dict]) -> list[dict]:
    workout_programs: list[dict] = []
    workout_names = [workout.get("name") for workout in workouts if workout.get("name")]

    for raw_program_workout in programs_workout_raw:
        program_name = raw_program_workout.get("name")
        raw_workouts = raw_program_workout.get("workout", [])

        if program_name is None:
            continue

        program_name = normalize_program_name(program_name)

        for raw_workout in raw_workouts:
            raw_workout_name = raw_workout.get("name")
            if raw_workout_name is None:
                continue
            
            workout_name = resolve_workout_name(raw_workout_name, workout_names)
            if workout_name is None:
                continue

            series = raw_workout.get("series")
            metadata = raw_workout.get("scrape_metadata", {})
            dom_index = metadata.get("dom_index")

            workout_programs.append(
                {
                    "program_name": program_name,
                    "workout_name": workout_name,
                    "series": series,
                    "order_number": dom_index + 1,
                }
            )

    return deduplicate_by_keys(workout_programs, ("program_name", "workout_name"))

def build_workout_category_map(listings_raw: list[dict]) -> dict[str, str]:
    """Melakukan mapping workout<->category (one-to-one)"""
    workout_category_map: dict[str, str] = {}

    for listing in listings_raw:
        category_name = listing.get("filter_name")
        workouts = listing.get("workouts", [])

        if category_name is None:
            continue

        for workout in workouts:
            name = workout.get("name")

            if name is None:
                continue

            existing_category = workout_category_map.get(name)

            if existing_category is not None and existing_category != category_name:
                raise ValueError(
                    f"Workout {name} ditemukan pada lebih dari satu category: "
                    f"{existing_category} dan {category_name}"
                )

            workout_category_map[name] = category_name

    return workout_category_map

def build_workout_target_map(
    listings_raw: list[dict],
) -> dict[str, set[str]]:
    """Melakukan mapping workout-target area (many-to-many)."""
    workout_target_map: dict[str, set[str]] = {}

    for listing in listings_raw:
        target_name = normalize_target_name(
            listing.get("target_name")
        )
        workouts = listing.get("workouts", [])

        if target_name is None:
            continue

        for workout in workouts:
            workout_name = workout.get("name")
            workout_name = workout_name.strip()
            if not workout_name:
                continue

            if workout_name not in workout_target_map:
                workout_target_map[workout_name] = set()

            workout_target_map[workout_name].add(target_name)

    return workout_target_map

def build_workout_role_map(workouts_raw: list[dict]) -> dict[tuple[str, str], str]:
    """
    Mapping:
    (workout_name, target_name) -> role
    """
    workout_role_map: dict[tuple[str, str], str] = {}

    for raw_workout in workouts_raw:
        workout_name = raw_workout.get("name")
        raw_targets = raw_workout.get("role_target_muscle",[],)
        workout_name = workout_name.strip()
        if not workout_name:
            continue

        for raw_target in raw_targets:
            target_name = normalize_target_name(raw_target.get("name_muscle"))
            role = normalize_muscle_role(raw_target.get("class"))

            if target_name is None or role is None:
                continue

            workout_role_map[(workout_name, target_name)] = role
    return workout_role_map

def resolve_workout_name(raw_name: str, workout_names: list[str]) -> str | None:
    """Helper karena terdapat inkonsistensi nama antara nama workout dari page workout dengan nama workout dari page program di web"""
    if raw_name in WORKOUT_NAME_ALIASES:
        return WORKOUT_NAME_ALIASES[raw_name]
