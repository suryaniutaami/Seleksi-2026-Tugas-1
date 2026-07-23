# Untuk mengambil data detail setiap program di web 
# (daftar workout)
# (series/duration)

from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)
from datetime import datetime
from zoneinfo import ZoneInfo
from src.helpers.constant import *
from src.helpers.json_io import *

def scrape_program_workouts(OUTPUT_PATH: str) -> None:
    print("\n--- SCRAPE PROGRAM DETAILS ---")
    
    # Baca seluruh data program unik yang ada dari programs.json
    unique_programs = get_unique_programs(OUTPUT_DIR_RAW / "programs.json")
    total_programs = len(unique_programs) 
    print(f"Jumlah unik program: {total_programs}\n")

    programs_data: list[dict] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            slow_mo=300,
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

        # Untuk setiap program yang ada, buka page dan scrape informasi
        count_program = 0
        for p_index in range(len(unique_programs)):
            program_name = unique_programs[p_index]["name"]
            url = unique_programs[p_index]["detail_url"]

            count_program += 1
            print(f"\nProgram {count_program}/{total_programs}") #progress status
            
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

            print("\n--- SCRAPE PROGRAM INFO ---")
            workout_button = page.locator(SELECTOR_PROGRAM_WORKOUT_NAMES)
            
            workout_data: list[dict] = []
            for index in range(workout_button.count()):
                button = workout_button.nth(index)

                workout_name = button.inner_text().strip()
                if not workout_name:
                    continue

                button.click()
                page.wait_for_timeout(1_000)
                
                series = None
                series_locator = page.locator(SELECTOR_ROWS).filter(has=page.locator(SELECTOR_PROGRAM_WORKOUT_SERIES))
                for row_index in range(series_locator.count()):
                    row = series_locator.nth(row_index)
                    value = row.locator("dd").inner_text().strip()
                    series = value or None

                workout_data.append(
                    {
                        "name": workout_name,
                        "series": series,
                        "scrape_metadata": {
                            "dom_index": index,
                            "selector_workout": SELECTOR_PROGRAM_WORKOUT_NAMES, 
                            "selector_series": SELECTOR_PROGRAM_WORKOUT_SERIES
                        }
                    }
                )

            program_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

            programs_data.append(
                {
                    "name": program_name,
                    "workout_count": len(workout_data),
                    "workout": workout_data,
                    "scrape_metadata": {
                        "url": url,
                        "scraped_at": program_scraped_at,
                    }
                }
            )
            print(f"Mencatat program \"{program_name}\" terdiri atas {len(workout_data)} workout")
        
        print(f"\nTotal program tersimpan: {len(programs_data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, programs_data)

        context.close()
        browser.close()

def get_unique_programs(file_path: str | Path) -> list[dict[str, str]]:
    """Mengambil program dengan detail_url dan name yang unik."""

    programs_raw = read_json(file_path)
    
    unique_programs: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_names: set[str] = set()

    for program in programs_raw:
        name = program.get("name")
        detail_url = program.get("detail_url")
        
        name = name.strip()
        detail_url = detail_url.strip()
        if not name or not detail_url:
            continue

        normalized_name = name.casefold()

        if (
            detail_url in seen_urls
            or normalized_name in seen_names
        ):
            continue

        seen_urls.add(detail_url)
        seen_names.add(normalized_name)

        unique_programs.append(
            {
                "name": name,
                "detail_url": detail_url,
            }
        )

    return unique_programs

