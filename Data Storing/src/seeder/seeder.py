from src.helpers.constant import *
from src.helpers.json_io import *
from src.helpers.formatter import *

def seed_category() -> list[str]:
    categories = read_json(CATEGORY_PATH)

    output: list[str] = []

    for i in categories:
        name = i.get("name")
        type = i.get("type")

        output.append(
            "INSERT INTO category (category_name, category_type) "
            f"VALUES ({format(name)}, {format(type)}) "
            "ON DUPLICATE KEY UPDATE "
            "category_type = VALUES(category_type);"
        )

    return output

def seed_step() -> list[str]:
    steps = read_json(STEP_PATH)

    output: list[str] = []

    for i in steps:
        workout_name = i.get("workout_name")
        no = i.get("no")
        description = i.get("description")

        output.append(
            "INSERT INTO step (workout_name, step_number, step_description) "
            f"VALUES ({format(workout_name)}, {format(no)}, {format(description)}) "
            "ON DUPLICATE KEY UPDATE "
            "step_description = VALUES(step_description);"
        )

    return output

def seed_target_area() -> list[str]:
    targets = read_json(TARGET_AREA_PATH)

    output: list[str] = []

    for i in targets:
        name = i.get("name")
        type = i.get("type")

        output.append(
            "INSERT INTO target_area (target_name, target_type) "
            f"VALUES ({format(name)}, {format(type)}) "
            "ON DUPLICATE KEY UPDATE "
            "target_type = VALUES(target_type);"
        )

    return output

def seed_workout_grip() -> list[str]:
    grips = read_json(WORKOUT_GRIP_PATH)

    output: list[str] = []

    for i in grips:
        workout_name = i.get("workout_name")
        grip = i.get("grip")

        output.append(
            "INSERT IGNORE INTO workout_grip (workout_name, grip) "
            f"VALUES ({format(workout_name)}, {format(grip)});"
        )

    return output

def seed_workout() -> list[str]:
    workouts = read_json(WORKOUT_PATH)

    output: list[str] = []

    for i in workouts:
        url = i.get("url")
        name = i.get("name")
        difficulty = i.get("difficulty")
        force = i.get("force")
        mechanic = i.get("mechanic")
        category_name = i.get("category_name")

        output.append(
            "INSERT INTO workout (workout_name, workout_url, difficulty, mechanic, `force`, category_name) "
            f"VALUES ({format(name)}, {format(url)}, {format(difficulty)}, "
            f"{format(mechanic)}, {format(force)}, {format(category_name)}) "
            "ON DUPLICATE KEY UPDATE "
            "workout_url = VALUES(workout_url), "
            "difficulty = VALUES(difficulty), "
            "mechanic = VALUES(mechanic), "
            "`force` = VALUES(`force`), "
            "category_name = VALUES(category_name);"
        )

    return output

def seed_workout_tag() -> list[str]:
    tags = read_json(WORKOUT_TAG_PATH)

    output: list[str] = []

    for i in tags:
        workout_name = i.get("workout_name")
        tag = i.get("tag")

        output.append(
            "INSERT IGNORE INTO workout_tag (workout_name, tag) "
            f"VALUES ({format(workout_name)}, {format(tag)});"
        )

    return output

def seed_workout_target() -> list[str]:
    targets = read_json(WORKOUT_TARGET_PATH)

    output: list[str] = []

    for i in targets:
        workout_name = i.get("workout_name")
        target_area_name = i.get("target_area_name")
        role = i.get("role")

        output.append(
            "INSERT INTO workout_target (workout_name, target_name, role_target) "
            f"VALUES ({format(workout_name)}, {format(target_area_name)}, {format(role)}) "
            "ON DUPLICATE KEY UPDATE "
            "role_target = VALUES(role_target);"
        )

    return output
def seed_program() -> list[str]:
    programs = read_json(PROGRAM_PATH)

    output: list[str] = []

    for i in programs:
        name = i.get("name")
        url = i.get("url")
        difficulty = i.get("difficulty")
        goal = i.get("goal")
        description = i.get("description")

        output.append(
            "INSERT INTO program (program_name, program_url, difficulty, goal, program_description) "
            f"VALUES ({format(name)}, {format(url)}, {format(difficulty)}, {format(goal)}, {format(description)}) "
            "ON DUPLICATE KEY UPDATE "
            "program_url = VALUES(program_url), "
            "difficulty = VALUES(difficulty), "
            "goal = VALUES(goal), "
            "program_description = VALUES(program_description);"
        )

    return output

def seed_program_workout() -> list[str]:
    program_workouts = read_json(PROGRAM_WORKOUT_PATH)

    output: list[str] = []

    for i in program_workouts:
        program_name = i.get("program_name")
        workout_name = i.get("workout_name")
        duration = i.get("series")
        order_number = i.get("order_number")

        output.append(
            "INSERT INTO program_workout (program_name, workout_name, duration, order_number) "
            f"VALUES ({format(program_name)}, {format(workout_name)}, {format(duration)}, {format(order_number)}) "
            "ON DUPLICATE KEY UPDATE "
            "duration = VALUES(duration), "
            "order_number = VALUES(order_number);"
        )

    return output