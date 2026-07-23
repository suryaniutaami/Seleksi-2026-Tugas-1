from src.scraper.scrape_target_areas import scrape_target_areas
from src.scraper.scrape_filters import scrape_filters
from src.scraper.scrape_listings import scrape_listings
from src.scraper.scrape_workouts import scrape_workouts
from src.scraper.scrape_programs import scrape_programs
from src.scraper.scrape_program_workouts import scrape_program_workouts
from src.helpers.constant import *

def main() -> None:
    print("\n--- SCRAPE DATA ---")
    OUTPUT_DIR_RAW.mkdir(parents=True, exist_ok=True)

    scrape_target_areas(OUTPUT_DIR_RAW / "target_areas.json")
    scrape_filters(OUTPUT_DIR_RAW / "filters.json")
    scrape_listings(OUTPUT_DIR_RAW / "listings.json")
    scrape_workouts(OUTPUT_DIR_RAW / "workouts.json")
    scrape_programs(OUTPUT_DIR_RAW / "programs.json")
    scrape_program_workouts(OUTPUT_DIR_RAW / "program_workouts.json")

if __name__ == "__main__":
    main()