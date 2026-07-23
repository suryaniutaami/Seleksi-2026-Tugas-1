from pathlib import Path

BASE_URL = "https://musclewiki.com"

DATA_SCRAPING_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR_RAW = DATA_SCRAPING_DIR / "data" / "raw"

OUTPUT_DIR_PROCESSED = DATA_SCRAPING_DIR / "data" / "processed"

# --- Kebutuhan Scrapping Web ---
SELECTOR_ROWS = "dl > div:has(dt):has(dd)"
"""Berguna untuk SELECTOR_WORKOUT_INFO, SELECTOR_WORKOUT_STEPS, dan SELECTOR_PROGRAM_WORKOUT_SERIES"""

# TARGET AREA TUBUH
SELECTOR_MUSCLES = "g.bodymap[id]"
"""Target Area Tubuh: Muscles

Format HTML:
- `<g id="calves" class="bodymap …">`
- `<g id="hands" class="bodymap …">`
- `...`"""

SELECTOR_JOINTS = "g.joints[id]"
"""Target Area Tubuh: Joints

Format HTML:
- `<g id="shoulders" class="joints …”>`
- `<g id="knees" class="joints …”>`
- `...`"""

# FILTER
SELECTOR_FILTERS = "label[for^='filter-equipments-']"
"""Filter Pencarian

Format HTML:
- `<label for="filter-equipments-0">Barbell</label>`
- `<label for="filter-equipments-1">Dumbbells</label>`
- `<label for="filter-equipments-2">Bodyweight</label>`
- `...`"""

# WORKOUT
SELECTOR_WORKOUTS = "a[href^='/exercise/']:has(h2)"
"""Listing Workouts per Page

Format HTML:
- `<a href="/exercise/chin-ups"><h2>Chin Ups</h2></a>`
- `<a href="/exercise/cable-lat-prayer"><h2>Cable Lat Prayer</h2></a>`
- `<a href="/exercise/dumbbell-row-unilateral"><h2>Dumbbell Row Unilateral</h2></a>`
- `...`"""

SELECTOR_PAGINATION = "nav[aria-label='Pagination'] button"
"""Berguna untuk SELECTOR_WORKOUTS supaya dapat scraping all pages

Format HTML:
```
<nav aria-label="Pagination">
<button>1</button>
<button>2</button>
<span>...</span>
<button>41</button>
</nav>
```"""

# DETAIL WORKOUT

SELECTOR_WORKOUT_INFO = "dt:text-is('Difficulty'), " "dt:text-is('Force'), ""dt:text-is('Grips'), ""dt:text-is('Mechanic')"
"""Detail Workout: Difficulity, Force, Grips, Mechanic

Format HTML:
```
<dl>
  <div>
    <dt>Difficulty</dt>
    <dd>....</dd>
  </div>

  <div>
    <dt>Force</dt>
    <dd>....</dd>
  </div>

  ...
</dl>
```"""

SELECTOR_WORKOUT_STEPS = "dt:text=/^\\d+$/"
"""Detail Workout: Steps

Format HTML:
```
<dl>
	<div>
		<dt><button>1</button></dt>
		<dd>Grasp the bar with an overhand grip.</dd>
	</div>
	
	<div>
		<dt><button>2</button></dt>
		<dd>Pull your body up until your chin is above the bar.</dd>
	</div>

	....
</dl>
```"""

SELECTOR_WORKOUT_TAGS = "div.flex.flex-1.flex-wrap a[aria-label]"
"""Detail Workout: Tags

Format HTML:
```
<div class="flex flex-1 flex-wrap">

	<a aria-label="Lats Exercise" href="">Lats Exercise</a>
	<a aria-label="intermediate Bodyweight exercise" href="">intermediate Bodyweight exercise</a>
	<a aria-label="How to do Pull Ups" href="">How to do Pull Ups</a>
	<a aria-label="Bodyweight Fitness" href="">Bodyweight Fitness</a>
	...

</div>
```"""

SELECTOR_WORKOUT_ROLE = (
    "g.bodymap[id].text-muscle-primary, "
    "g.bodymap[id].text-muscle-secondary, "
    "g.bodymap[id].text-muscle-tertiary"
)
"""Detail Workout: Role Muscle (Primary, Secondary, Tertiary)

Format HTML:
```
<g id="glutes" class="bodymap text-muscle-primary">
<g id="biceps" class="bodymap text-muscle-secondary">
...
```"""


# PROGRAM EXERCISE
SELECTOR_PROGRAMS = "a[href^='/workout/'][aria-label]"
"""Program Workout

Format HTML:
```
<a
aria-label="View Full Body Novice Bodybuilding - Day 1 workout details"
href="/workout/full-body-bodybuilding-workout-day-one">
</a>
```
"""

SELECTOR_PROGRAM_DIFFICULTY = "div.relative > div.absolute.top-2"
"""Program Workout: Difficulty 

Format HTML:

```
<div class="absolute top-2 ...">
    Novice
</div>
```

"""

SELECTOR_PROGRAM_GOAL = "div.relative > div.absolute.top-9"
"""Program Workout: Goal 

Format HTML:

```
<div class="absolute top-9 ...">
    Gain Muscle
</div>
```
"""

SELECTOR_PROGRAM_DESCRIPTION = "div:has(> dt:text-is('Description')):has(> dd)"
"""Program Workout: Description 

Format HTML:

```
<div>
	<dt>Description</dt>
	<dd>Beginner bodybuilding routine for those new to the gym.</dd>
</div>
```
"""

# DETAIL PROGRAM

SELECTOR_PROGRAM_WORKOUT_NAMES = "div.lg\\:grid.grid-flow-col.mt-6.hidden button"

"""Detail Program Workout: Daftar Workout

Format HTML:
```

<div class="lg:grid grid-flow-col mt-6 hidden ...">
    <button>Dumbbell Goblet Squat</button>
    <button>Bodyweight Knee Push Ups</button>
    <button>Band Pull Apart</button>
</div>
```
"""

SELECTOR_PROGRAM_WORKOUT_SERIES = "dt:text-is('Series'), ""dt:text-is('Duration')"
"""Detail Program Workout: Series/Duration, eg 3x12

Digunakan bersama SELECTOR_ROWS.

Format HTML:

```
<dl>
    <div>
        <dt>Series</dt>
        <dd>3x8-12</dd>
    </div>
</dl>
```

atau:

```
<dl>
    <div>
        <dt>Duration</dt>
        <dd>3x10</dd>
    </div>
</dl>
```

"""

# Helper karena terdapat inkonsistensi nama antara nama workout dari page workout dengan nama workout dari page program di web
WORKOUT_NAME_ALIASES = {
    "Hand Plank": "Bodyweight Hand Plank Jack",
}