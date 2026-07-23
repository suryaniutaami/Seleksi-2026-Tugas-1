# Untuk mengambil data listing program di web

from playwright.sync_api import sync_playwright
from datetime import datetime
from zoneinfo import ZoneInfo
from src.helpers.constant import *
from src.helpers.json_io import *

def scrape_programs(OUTPUT_PATH: str) -> None:
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

        programs_url = f"{BASE_URL}/workouts"

        print(f"Membuka: {programs_url}")
        page.goto(
            programs_url,
            wait_until="domcontentloaded",
            timeout=60_000,
        )

        print("Title:", page.title())
        print("Final URL:", page.url)

        page.wait_for_timeout(5_000)

        print("\n--- SCRAPE PROGRAMS ---")

        programs_locator = page.locator(SELECTOR_PROGRAMS)
        data: list[dict] = []
        seen_link: set[str] = set()
        seen_name: set[str] = set()
        programs_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

        page_num = 1

        count_current_page = 0
        for index in range(programs_locator.count()):
            p = programs_locator.nth(index)

            link = p.get_attribute("href")
            name = p.get_attribute("aria-label")

            if not link or not name:
                continue
            
            name = name.strip() #eg: "View Full Body Novice Bodybuilding - Day 1 workout details"
            link = link.strip() #eg: "/workout/full-body-bodybuilding-workout-day-one"

            if link in seen_link or name in seen_name:
                continue
            
            difficulty_locator = p.locator(SELECTOR_PROGRAM_DIFFICULTY) 
            goal_locator = p.locator(SELECTOR_PROGRAM_GOAL) 
            difficulty = None
            goal = None
            if difficulty_locator.count() > 0:
                difficulty = difficulty_locator.first.inner_text().strip() or None  #eg: "Novice"
            if goal_locator.count() > 0:
                goal = goal_locator.first.inner_text().strip() or None  #eg: "Gain Muscle"

            program_card = p.locator("xpath=ancestor::li[1]")   #parent program card
            description = None
            description_locator = program_card.locator(SELECTOR_PROGRAM_DESCRIPTION)
            if description_locator.count() > 0:
                description = description_locator.first.locator("dd").inner_text().strip() or None #eg: "Beginner bodybuilding routine for those new to the gym."
    
            seen_link.add(link)
            seen_name.add(name)

            detail_url = f"{BASE_URL}{link}"

            data.append(
                {
                    "name": name,
                    "detail_url": detail_url,
                    "difficulty": difficulty,
                    "goal": goal,
                    "description": description,
                    "scrape_metadata": {
                        "page_number": page_num,
                        "dom_index": index,
                        "selector": SELECTOR_PROGRAMS,
                        "scraped_at": programs_scraped_at,
                    },
                }
            )
            count_current_page += 1

        print(f"Mencatat dari halaman {page_num} sebanyak: {count_current_page} program")

        # Untuk setiap halaman yang ada, scrape program
        next_button = page.get_by_role("button", name="Next", exact=True)
        while (next_button.count() != 0 and not(next_button.is_disabled())):
            print("\n--- Membuka halaman berikutnya")
            page_num += 1

            next_button.click()
            page.wait_for_timeout(2_000)

            programs_locator = page.locator(SELECTOR_PROGRAMS)

            programs_scraped_at = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(timespec="seconds")

            count_current_page = 0
            for index in range(programs_locator.count()):
                p = programs_locator.nth(index)

                link = p.get_attribute("href")
                name = p.get_attribute("aria-label")

                if not link or not name:
                    continue
                
                name = name.strip() #eg: "View Full Body Novice Bodybuilding - Day 1 workout details"
                link = link.strip() #eg: "/workout/full-body-bodybuilding-workout-day-one"

                if link in seen_link or name in seen_name:
                    continue

                difficulty = None
                goal = None
                difficulty_locator = p.locator(SELECTOR_PROGRAM_DIFFICULTY)
                goal_locator = p.locator(SELECTOR_PROGRAM_GOAL)
                if difficulty_locator.count() > 0:
                    difficulty = difficulty_locator.first.inner_text().strip() or None
                if goal_locator.count() > 0:
                    goal = goal_locator.first.inner_text().strip() or None

                program_card = p.locator("xpath=ancestor::li[1]")   #parent program card
                description = None
                description_locator = program_card.locator(SELECTOR_PROGRAM_DESCRIPTION)
                if description_locator.count() > 0:
                    description = description_locator.first.locator("dd").inner_text().strip() or None #eg: "Beginner bodybuilding routine for those new to the gym."
    

                seen_link.add(link)
                seen_name.add(name)

                detail_url = f"{BASE_URL}{link}"

                data.append(
                    {
                        "name": name,
                        "detail_url": detail_url,
                        "difficulty": difficulty,
                        "goal": goal,
                        "description": description,
                        "scrape_metadata": {
                            "page_number": page_num,
                            "dom_index": index,
                            "selector": SELECTOR_PROGRAMS,
                            "scraped_at": programs_scraped_at,
                        },
                    }
                )
                count_current_page +=1 

            print(f"Mencatat dari halaman {page_num} sebanyak: {count_current_page} program")

            next_button = page.get_by_role("button", name="Next", exact=True)
   
        print(f"\nTotal program tersimpan: {len(data)}")
        print(f"--- Menyimpan ke {OUTPUT_PATH} ---")
        write_json(OUTPUT_PATH, data)

        context.close()
        browser.close()
