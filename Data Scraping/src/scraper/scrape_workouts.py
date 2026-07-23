# Untuk mengambil data detail setiap workout di web 
# (difficulty, force, grips, mechanic)
# (steps, tags)
# (primary, secondary, tertiary target area)

from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from src.helpers.constant import *
from src.helpers.json_io import *

def scrape_workouts(OUTPUT_PATH: str) -> None:
    print("\n--- SCRAPE WORKOUT DETAILS. Estimasi waktu 3 jam ---")
    
    # Baca seluruh data workout unik yang ada dari listings.json
    unique_workouts = get_unique_workouts(OUTPUT_DIR_RAW / "listings.json")
    total_workouts = len(unique_workouts) 
    print(f"Jumlah unik workouts: {total_workouts}\n")

    workouts_data: list[dict] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 "
                "(Educational Web Scraping Project; "
                "Institut Teknologi Bandung; "
                "contact: 13524042@std.stei.itb.ac.id)"
            ),
        )
        page = context.new_page()
        
        # Untuk setiap workout yang ada, buka page dan scrape informasi
        count_workout = 0
        for w_index in range(len(unique_workouts)):
            workout_name = unique_workouts[w_index]["name"]
            url = unique_workouts[w_index]["detail_url"]

            count_workout += 1
            print(f"\nWorkout {count_workout}/{total_workouts}") #progress status
            
            print(f"\n--- Membuka: {url}")
            try:
                response = page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )
            except PlaywrightTimeoutError:
                print(
                    f"[TIMEOUT] Gagal membuka {url}. "
                    "Lanjut ke kombinasi berikutnya."
                )
                continue
            except PlaywrightError as error:
                print(
                    f"[ERROR] Gagal membuka {url}: "
                    f"{error}"
                )
                continue
            if response is None:
                print(
                    f"[NO RESPONSE] Tidak menerima response dari "
                    f"{url}."
                )
                continue
            if response.status >= 400:
                print(
                    f"[HTTP {response.status}] "
                    f"Gagal membuka {url}."
                )
                continue

            page.wait_for_timeout(2_000)

            print("\n--- SCRAPE WORKOUT INFO ---")
            winfo_locator = page.locator(SELECTOR_ROWS).filter(has=page.locator(SELECTOR_WORKOUT_INFO))
            
            winfo_data: dict = {
                "difficulty": None,
                "force": None,
                "grips": None,
                "mechanic": None,
                "scrape_metadata": {
                            "selector": SELECTOR_ROWS,
                            "filter_selector": SELECTOR_WORKOUT_INFO, 
                        }
            }
            seen_info: set[str] = set()

            for index in range(winfo_locator.count()):
                w = winfo_locator.nth(index)

                label = w.locator("dt").inner_text().strip().lower()    #eg: 'difficulty', 'force', ...
                value = w.locator("dd").inner_text().strip()     

                if not label or label not in winfo_data:
                    continue

                if label in seen_info:
                    continue
                seen_info.add(label)

                winfo_data[label] = value or None
                # print(f"{label}: {winfo_data[label]}\n")
            print(f"Jumlah info: {len(seen_info)}")

            print("\n--- SCRAPE WORKOUT STEPS ---")
            step_locator = page.locator(SELECTOR_ROWS)
            
            step_data: list[dict] = []
            for index in range(step_locator.count()):
                s = step_locator.nth(index)

                number_text = s.locator("dt").inner_text().strip()
                description = s.locator("dd").inner_text().strip()

                if not number_text.isdigit() or not description:
                    continue

                step_data.append(
                    {
                        "no": int(number_text),
                        "description": description,
                        "scrape_metadata": {
                            "dom_index": index,
                            "selector": SELECTOR_ROWS, 
                        }
                    }
                )
            print(f"Jumlah step: {len(step_data)}")

            print("\n--- SCRAPE WORKOUT TAGS ---")
            tag_locator = page.locator(SELECTOR_WORKOUT_TAGS)
            
            tag_data: list[dict] = []
            seen_tag: set[str] = set()

            for index in range(tag_locator.count()):
                t = tag_locator.nth(index)

                tag = t.get_attribute("aria-label")
                if not tag:
                    continue
                tag = tag.strip()   #eg: "Lats Exercise"

                if not tag or tag in seen_tag:
                    continue

                seen_tag.add(tag)

                tag_data.append(
                    {
                        "tag": tag,
                        "scrape_metadata": {
                            "dom_index": index,
                            "selector": SELECTOR_WORKOUT_TAGS, 
                        }
                    }
                )
            print(f"Jumlah tag: {len(tag_data)}")

            print("\n--- SCRAPE WORKOUT ROLE TARGET MUSCLE ---")
            role_locator = page.locator(SELECTOR_WORKOUT_ROLE)
            
            role_data: list[dict] = []
            seen_role: set[tuple[str, str]] = set()

            for index in range(role_locator.count()):
                r = role_locator.nth(index)

                name_muscle = r.get_attribute("id")
                role = r.get_attribute("class")
                if not name_muscle or not role:
                    continue
                name_muscle = name_muscle.strip()   #eg: "glutes"
                role = role.strip()   #eg: "bodymap text-muscle-primary"

                role_key = (name_muscle, role)
                if role_key in seen_role:
                    continue

                seen_role.add(role_key)
             
                role_data.append(
                    {
                        "name_muscle": name_muscle,
                        "scrape_metadata": {
                            "dom_index": index,
                            "selector": SELECTOR_WORKOUT_ROLE, 
                        },
                        "class": role
                    }
                )
            print(f"Jumlah role target muscle: {len(role_data)}")

            workout_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")
            
            workouts_data.append(
                {
                    "name":  workout_name,
                    "detail_url": url,
                    "info": winfo_data,
                    "count_step": len(step_data),
                    "count_tag": len(tag_data),
                    "count_role_target_muscle": len(role_data),
                    "step": step_data,
                    "tag": tag_data,
                    "role_target_muscle": role_data,
                    "scrape_metadata": {
                        "source_index": w_index,
                        "scraped_at": workout_scraped_at,
                    }
                }
            )
        print(f"\nTotal workouts data tersimpan: {len(workouts_data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, workouts_data)

        context.close()
        browser.close()

def get_unique_workouts(file_path: str | Path) -> list[dict[str, str]]:
    """Mengambil workout dengan detail_url dan name yang unik."""
    listings = read_json(file_path)
  
    unique_workouts: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_names: set[str] = set()

    for listing in listings:
        workouts = listing.get("workouts", [])
        for workout in workouts:
            name = workout.get("name")
            detail_url = workout.get("detail_url")

            name = name.strip()
            detail_url = detail_url.strip()
            if not name or not detail_url:
                continue

            normalized_name = name.casefold()

            if detail_url in seen_urls or normalized_name in seen_names:
                continue

            seen_urls.add(detail_url)
            seen_names.add(normalized_name)

            unique_workouts.append(
                {
                    "name": name,
                    "detail_url": detail_url,
                }
            )

    return unique_workouts

