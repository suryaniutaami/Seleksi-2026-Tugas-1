# Untuk mengambil data filter pencarian yang ada di web

from playwright.sync_api import sync_playwright
from datetime import datetime
from zoneinfo import ZoneInfo
from src.helpers.constant import *
from src.helpers.json_io import *

def scrape_filters(OUTPUT_PATH: str) -> None:
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

        print(f"Membuka: {BASE_URL}")
        page.goto(
            BASE_URL,
            wait_until="domcontentloaded",
            timeout=60_000,
        )

        print("Title:", page.title())
        print("Final URL:", page.url)

        page.wait_for_timeout(5_000)

        print("\n--- SCRAPE FILTERS ---")

        filters_locator = page.locator(SELECTOR_FILTERS)
        print("\nJumlah seluruh filter:", filters_locator.count())

        data: list[dict] = []
        seen: set[str] = set()

        filters_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

        for index in range(filters_locator.count()):
            f = filters_locator.nth(index)

            filter_id = f.get_attribute("for")  
            name = f.inner_text().strip()   #eg: 'Barbell'
            if not filter_id or not name:   
                continue
            filter_id = filter_id.strip()   #eg: 'filter-equipments-0'

            if filter_id in seen:
                continue

            seen.add(filter_id)

            data.append(
                {
                    "name": name,
                    "scrape_metadata": {
                        "dom_index": index,
                        "filter_id": filter_id,
                        "selector": SELECTOR_FILTERS,
                        "scraped_at": filters_scraped_at,
                    },
                }
            )
        
        print(f"\nTotal filter tersimpan: {len(data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, data)

        context.close()
        browser.close()


