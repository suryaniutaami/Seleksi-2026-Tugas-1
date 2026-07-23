# Untuk mengambil data listing workout untuk setiap target tubuh dan filter 

from playwright.sync_api import (
    Error as PlaywrightError,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)
from datetime import datetime
from zoneinfo import ZoneInfo
import re
from src.helpers.constant import *
from src.helpers.json_io import *

# Scrape listing workout kombinasi target area × filter × page
def scrape_listings(OUTPUT_PATH: str) -> None:
    print("\n--- SCRAPE LISTINGS. Estimasi waktu 2 jam ---")
    
    print("\n--- Buat kombinasi url berdasarkan pasangan (target_area, filter) ---")
    target_areas = read_json(OUTPUT_DIR_RAW / "target_areas.json")
    filters = read_json(OUTPUT_DIR_RAW / "filters.json")

    # Validasi kombinasi
    valid_combinations: list[tuple[str, str]] = []
    for target in target_areas:
        target_name = target.get("name")
        target_type = get_target_type(target)

        if not target_name or not target_type:
            continue

        for filter_data in filters:
            filter_name = filter_data.get("name")

            if not filter_name:
                continue

            if is_valid_combination(target_type, filter_name):
                valid_combinations.append((target_name, filter_name))
    total_listing = len(valid_combinations)
    print(f"Jumlah kombinasi URL valid: {total_listing}\n")

    listings_data: list[dict] = []

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

        # Untuk setiap listing yang ada
        count_listing = 0
        for target_name, filter_name in valid_combinations:
            filter_slug = create_slug(filter_name)

            count_listing += 1
            print(f"\nListing {count_listing}/{total_listing}") # progress status

            listing_url = (f"{BASE_URL}/exercises/{target_name}/{filter_slug}")
            print(f"\n--- Membuka: {listing_url}")
            try:
                response = page.goto(
                    listing_url,
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )
            except PlaywrightTimeoutError:
                print(
                    f"[TIMEOUT] Gagal membuka {listing_url}. "
                    "Lanjut ke kombinasi berikutnya."
                )
                continue
            except PlaywrightError as error:
                print(
                    f"[ERROR] Gagal membuka {listing_url}: "
                    f"{error}"
                )
                continue
            if response is None:
                print(
                    f"[NO RESPONSE] Tidak menerima response dari "
                    f"{listing_url}."
                )
                continue
            if response.status >= 400:
                print(
                    f"[HTTP {response.status}] "
                    f"Gagal membuka {listing_url}."
                )
                continue

            page.wait_for_timeout(2_000)

            # Untuk setiap page pada listing 
            last_page = get_last_page_number(page)
            print(f"Jumlah halaman terdeteksi: {last_page}")

            for pn in range(1, last_page+1):
                if pn == 1:
                    page_url = listing_url
                else:
                    page_url = f"{listing_url}/{pn}"

                if (pn > 1):
                    try:
                        response = page.goto(
                            page_url,
                            wait_until="domcontentloaded",
                            timeout=60_000,
                        )

                    except PlaywrightTimeoutError:
                        print(
                            f"[TIMEOUT] {page_url}"
                        )
                        continue

                    except PlaywrightError as error:
                        print(
                            f"[ERROR] {page_url}: "
                            f"{error}"
                        )
                        continue

                    if (
                        response is None
                        or response.status >= 400
                    ):
                        print(
                            f"[GAGAL] {page_url}"
                        )
                        continue

                    page.wait_for_timeout(2_000)

                # Scrape workouts pada page tersebut
                workouts_data = extract_workouts(page)

                listing_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

                listings_data.append(
                    {
                        "target_name": target_name,
                        "filter_name": filter_name,
                        "page_number": pn,
                        "workout_count": len(workouts_data),
                        "workouts": workouts_data,
                        "scrape_metadata": {
                            "url": listing_url,
                            "page_url": page_url,
                            "scraped_at": listing_scraped_at
                        },
                    }
                )

                print(f"Mencatat dari {page_url} sebanyak: {len(workouts_data)} workout")


        print(f"\nTotal listing page tersimpan: {len(listings_data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, listings_data)

        context.close()
        browser.close()

def extract_workouts(page: Page) -> list[dict]:
    """Mengambil workout yang tampil pada satu halaman listing"""

    workouts_locator = page.locator(SELECTOR_WORKOUTS)

    workouts_data: list[dict] = []

    for index in range(workouts_locator.count()):
        w = workouts_locator.nth(index)

        link = w.get_attribute("href")
        name = w.locator("h2").inner_text().strip()   #eg: 'Chin Ups'

        if not link or not name:
            continue

        link = link.strip() #eg: "/exercise/chin-ups"

        detail_url = f"{BASE_URL}{link}"

        workouts_data.append(
            {
                "name": name,
                "detail_url": detail_url,
                "scrape_metadata": {
                    "dom_index": index,
                    "selector": SELECTOR_WORKOUTS,
                }
            }
        )

    return workouts_data

def create_slug(name: str) -> str:
    """Helper untuk listing_url, convert filter name ke format lowercase dan spasi pakai '-'"""
    slug = name.strip().casefold()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)

    return slug.strip("-")

def get_last_page_number(page: Page) -> int:
    """Helper untuk paginasi, mencari no page terakhir"""
    page_number_buttons = page.locator(
        "nav[aria-label='Pagination'] button"
    )

    page_numbers: list[int] = []

    for index in range(page_number_buttons.count()):
        text = page_number_buttons.nth(index).inner_text().strip()

        if text.isdigit():  # Contoh: "41".isdigit() = True
            page_numbers.append(int(text))

    return max(page_numbers, default=1)

def is_valid_combination(target_type: str, filter_name: str) -> bool:
    """Helper untuk cek validitas url, karena di web mode target Joint hanya memiliki filter Recovery
       dan sebaliknya. Kombinasi Recovery dengan selain target bertype Joint selalu menghasilkan tampilan default 55 halaman.
    """
    if filter_name.strip().casefold() == "recovery":
        return target_type == "Joint"

    return target_type == "Muscle"

def get_target_type(target: dict) -> str | None:
    raw_class = target.get("class", "")
    if "joints" in raw_class.split():
        return "Joint"
    if "bodymap" in raw_class.split():
        return "Muscle"

    return None

