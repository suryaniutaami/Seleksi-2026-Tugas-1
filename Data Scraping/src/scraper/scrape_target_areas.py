# Untuk mengambil data target area tubuh, baik muscles maupun joints yang ada di web

from playwright.sync_api import sync_playwright
from datetime import datetime
from zoneinfo import ZoneInfo
from src.helpers.constant import *
from src.helpers.json_io import *

def scrape_target_areas(OUTPUT_PATH: str) -> None:
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

        print("\n--- SCRAPE MUSCLES ---")

        muscles_locator = page.locator(SELECTOR_MUSCLES)

        muscles_data: list[dict] = []
        seen_muscles: set[str] = set()

        muscles_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

        for index in range(muscles_locator.count()):
            m = muscles_locator.nth(index)

            name = m.get_attribute("id")    
            cl = m.get_attribute("class")
            if not name or not cl:
                continue
            name = name.strip() #eg: 'calves
            cl = cl.strip() #'bodymap' 

            if name in seen_muscles:
                continue

            seen_muscles.add(name)

            muscles_data.append(
                {
                    "name": name,
                    "class": cl,
                    "scrape_metadata": {
                        "dom_index": index,
                        "selector": SELECTOR_MUSCLES,
                        "scraped_at": muscles_scraped_at,
                    },
                }
            )
        print("Jumlah seluruh muscle unik:", len(muscles_data))

        print("\n--- SCRAPE JOINTS ---")

        joints_locator = page.locator(SELECTOR_JOINTS)

        print("--- Mengaktifkan mode Joints di web")
        toggle_button = page.locator('div:has-text("Joints") >> [role="switch"]').last
        toggle_button.click()

        page.wait_for_timeout(3_000) 
        
        joints_data: list[dict] = []
        seen_joints: set[str] = set()

        joints_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")
        
        for index in range(joints_locator.count()):
            j = joints_locator.nth(index)

            name = j.get_attribute("id")
            cl = j.get_attribute("class")
            if not name or not cl:
                continue
            name = name.strip() #eg: 'shoulders'
            cl = cl.strip() #'joints'

            if name in seen_joints:
                continue

            seen_joints.add(name)

            joints_data.append(
                {
                    "name": name,
                    "class": cl,
                    "scrape_metadata": {
                        "dom_index": index,
                        "selector": SELECTOR_JOINTS,
                        "scraped_at": joints_scraped_at,
                    },
                }
            )
        print("Jumlah seluruh joint unik:", len(joints_data))

        data = muscles_data + joints_data
        print(f"\nTotal target area tubuh tersimpan: {len(data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, data)
        
        context.close()
        browser.close()