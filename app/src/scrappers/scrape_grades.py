import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

        # Return the updated page source for scraping
        return driver.page_source

    except Exception as e:
        print(f"Error clicking on 'Grade Book': {e}")


def __scrape_grades(html_content):
    """
    Parses the given HTML content and extracts class grades, teachers, and marking period.

    Args:
        html_content (str): The HTML content of the gradebook.

    Returns:
        str: JSON string containing the extracted grade data.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the grading period
    grading_period_elem = soup.find("div", class_="current breadcrumb-term")
    grading_period = grading_period_elem.text.strip() if grading_period_elem else "Unknown"

    # Find all classes
    classes_data = []
    for class_row in soup.find_all("div", class_="row gb-class-header gb-class-row flexbox horizontal"):
        class_name_elem = class_row.find("button", class_="btn btn-link course-title")
        teacher_elem = class_row.find("div", class_="teacher.hide-for-screen")

        if class_name_elem and teacher_elem:
            class_name = class_name_elem.text.split(": ", 1)[-1].strip()
            teacher_name = teacher_elem.text.strip()

            # Find the associated grade row using data-guid
            data_guid = class_row.get("data-guid")
            grade_row = soup.find("div", class_="row gb-class-row", attrs={"data-guid": data_guid})

            if grade_row:
                grade_elem = grade_row.find("span", class_="mark")
                score_elem = grade_row.find("span", class_="score")
                grade = grade_elem.text.strip() if grade_elem else "N/A"
                score = score_elem.text.strip() if score_elem else "N/A"

                # Store the extracted data
                classes_data.append({
                    "class": class_name,
                    "teacher": teacher_name,
                    "grading_period": grading_period,
                    "grade": grade,
                    "score": score
                })

    # Convert to JSON and return
    return classes_data

def collect_grades(driver):
    grade_html_source =  __click_grade_book(driver)
    grade_json = __scrape_grades(grade_html_source)
    print( json.dumps(grade_json, indent=4))
    return grade_json
