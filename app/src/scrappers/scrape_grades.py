import json
import re
from datetime import datetime
from utils import file_utils, csv_utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

__date_scraped = datetime.now().strftime("%Y-%m-%d_%H%M%S")  # Format: YYYY-MM-DD HH:MM:SS

def click_grade_book(driver):
    __click_grade_book(driver)

def __click_grade_book(driver):
    """
    Clicks on the 'Grade Book' link after logging in.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    try:
        # Click on the "Grade Book" link
        gradebook_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Grade Book"))
        )
        gradebook_link.click()

        # Wait for the gradebook content to load (adjust timeout if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gb-classes"))
        )

    except Exception as e:
        print(f"Error clicking on 'Grade Book': {e}")


def __scrape_grades(driver):
    # Extract table rows
    class_rows = driver.find_elements(By.CSS_SELECTOR, ".gb-class-header.gb-class-row.flexbox.horizontal")

    data = []

    for row in class_rows:

        try:
            # Extract class name
            raw_class_name = row.find_element(By.XPATH, ".//button[contains(@class, 'course-title')]").text.strip()
            # Remove the leading number and colon (e.g., "1: Geometry" → "Geometry")
            class_name = re.sub(r"^\d+:\s*", "", raw_class_name)

            # Extract teacher name
            teacher_name = row.find_element(By.XPATH, ".//span[contains(@class, 'teacher')]//a").text.strip()

            # Extract period
            period = row.find_element(By.XPATH,
                                      "./following-sibling::div[contains(@class, 'gb-class-row')]//button[contains(@class, 'course-markperiod')]").text.strip()

            # Extract grade (if available)
            try:
                grade = row.find_element(By.XPATH,
                                         "./following-sibling::div[contains(@class, 'gb-class-row')]//span[contains(@class, 'mark')]").text.strip()
            except:
                grade = "N/A"

            # Extract score (if available)
            try:
                score = row.find_element(By.XPATH,
                                         "./following-sibling::div[contains(@class, 'gb-class-row')]//span[contains(@class, 'score')]").text.strip()
            except:
                score = "N/A"

            # Append data
            data.append({
                "Class": class_name,
                "Teacher": teacher_name,
                "Period": period,
                "Grade": grade,
                "Score": score,
                "date_scraped": __date_scraped,
            })

        except Exception as e:
            print(f"Error processing a row: {e}")

    print("[INFO] Scraped Grades Successfully.")
    return data


def __save_grades(grade_json, data_output_format):
    file_utils.save_data(grade_json, __date_scraped, data_output_format)


def __convert_to_csv(grade_json):
    return csv_utils.json_to_csv_pandas(grade_json)


def process_grades(driver, data_output_format):

    try:

        __click_grade_book(driver)

        grade_json = __scrape_grades(driver)

        __save_grades(grade_json, data_output_format)

    except Exception as e:
        print(f"[ERROR] Failed to save JSON: {e}")
