import unicodedata
import re

# --- Normalisasi TargetArea ---
def normalize_target_type(class_value: str) -> str | None:
    """ 
        Akan dibuat atribut `type` dari atribut `class` pada raw target_areas.json:
        - `class = "bodymap text-mw-gray active:text-mw-red-700 lg:hover:text-mw-red-100" -> type = "Muscle"`
        - `class = "joints text-mw-red stroke-[#484a68] hover:text-mw-green hover:stroke-gray-900" -> type = "Joint"` 
    """
    classes = class_value.split()

    if "bodymap" in classes:
        return "Muscle"

    if "joints" in classes:
        return "Joint"

    return None

# --- Normalisasi WorkoutTarget ---
def normalize_muscle_role(class_value: str) -> str | None:
    """ 
        Akan dibuat atribut `role` dari atribut `class` yang terdapat di dalam `role_target_muscle` pada raw workouts.json:
        - `class = "bodymap text-muscle-primary" -> role = "Primary"`
        - `class = "bodymap text-muscle-secondary" -> role = "Secondary"` 
        - `class = "bodymap text-muscle-tertiary" -> role = "Tertiary"` 
    """
    classes = class_value.split()

    if "text-muscle-primary" in classes:
        return "Primary"

    if "text-muscle-secondary" in classes:
        return "Secondary"

    if "text-muscle-tertiary" in classes:
        return "Tertiary"

    return None

# --- Normalisasi Category ---
EXERCISE_TYPE_IDS = {
    "filter-equipments-6",   #Stretches
    "filter-equipments-11",  #Yoga
    "filter-equipments-13",  #Cardio
    "filter-equipments-15",  #Recovery
    "filter-equipments-16",  #Pilates
}
def normalize_category_type(filter_id: str) -> str:
    """
    Secara heuristik, memisahkan data filter menjadi `Equipment` dan `Exercise Type`
    """
    if filter_id in EXERCISE_TYPE_IDS:
        return "Exercise Type"

    return "Equipment"

# --- Normalisasi nama target ---
def normalize_target_name(name: str) -> str:
    """
    Dilakukan formatting atribut `name` target pada raw target_areas.json dan pada raw workouts.json
    
    Supaya sama dgn format `name` pada filter, workout, dll.
    
    Yaitu kapitalisasi pada setiap awal kata dan antar dua kata dipisahkan dengan spasi.

    Contoh:
    - `front-shoulders -> Front Shoulders`
    - `traps-middle -> Traps Middle`
    - `lowerback -> Lowerback`
    """
    return name.replace("-", " ").strip().title()


def normalize_tag_name(value: str) -> str:
    """Normalisasi atribut '`name` pada tag supaya jadi lower case dan bebas dari unicode"""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(
        char for char in normalized
        if not unicodedata.combining(char)
    )
    return without_accents.strip().casefold()

def normalize_program_name(value: str) -> str:
    """
    Normalisasi atribut `name` pada program supaya tidak menampilkan string teknis
    
    Contoh: 
    -`"View Full Body Novice Bodybuilding - Day 1 workout details" -> "Full Body Novice Bodybuilding - Day 1" `
    -`"View The 1 Dumbbell Workout workout details" -> "The 1 Dumbbell Workout"`
    """
    normalized = value.strip()
    # Hapus "View" yang berada di awal string, dipisahkan oleh spasi
    normalized = re.sub(r"^View\s+",
                        "",
                        normalized,
                        flags=re.IGNORECASE,
    )
    # Hapus "workout details" yang berada di akhir string, dipisahkan oleh spasi di antaranya
    normalized = re.sub(r"\s+workout\s+details$",
                        "",
                        normalized,
                        flags=re.IGNORECASE,
    )

    return normalized.strip()
