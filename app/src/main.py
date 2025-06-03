import os

from config import Config, load_config
from scrappers.pvue_login import login_to_website
from scrappers.scrape_grades import process_grades
from scrappers.scrape_assignments import process_assignments


def main(config: Config | None = None) -> None:
    """Entry point for scraping ParentVUE."""

    cfg = config or load_config()

    driver = None
    try:
        driver = login_to_website(cfg.pvue_url, cfg.username, cfg.password)
        # process_grades(driver, cfg.data_output_format, cfg.grades_file_name, cfg.output_dir)
        process_assignments(driver, cfg.data_output_format, output_dir=cfg.output_dir)
    except Exception as exc:
        print(exc)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
