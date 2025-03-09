import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scrappers.scrape_grades import click_grade_book


def process_assignments(driver, data_output_format):
    click_grade_book(driver)
    __iterate_over_each_class(driver, data_output_format)


def __scrape_assignment(class_name, driver, data_output_format):
    print("Loaded Page {}. Start Scrapping!!!".format(class_name))


def __iterate_over_each_class(driver, data_output_format):
    """
    Scrape all assignments from each class page.
    """
    time.sleep(3)  # Allow initial page load

    while True:
        # Find all class rows (Re-fetch on every iteration to avoid stale elements)
        class_rows = driver.find_elements(By.CSS_SELECTOR, "div.gb-class-header.gb-class-row")
        total_classes = len(class_rows)
        print(f"Loaded {total_classes} classes")

        for index in range(total_classes):
            try:
                # Refresh elements to avoid stale reference
                class_rows = driver.find_elements(By.CSS_SELECTOR, "div.gb-class-header.gb-class-row")
                row = class_rows[index]

                # Extract class name
                class_name_element = row.find_element(By.CSS_SELECTOR, "button.course-title")
                class_name = class_name_element.text.split(": ", 1)[-1]
                print(f"Class: {class_name}")

                # Extract teacher name
                teacher_element = row.find_element(By.CSS_SELECTOR, "span.teacher.hide-for-print a")
                teacher_name = teacher_element.text.strip()
                print(f"Class: {class_name}, Teacher: {teacher_name}")

                # Extract Marking Period (MP)
                try:
                    marking_period_row = row.find_element(By.XPATH, "following-sibling::div[contains(@class, 'gb-class-row')]")
                    marking_period_element = marking_period_row.find_element(By.CSS_SELECTOR, "button.btn.btn-link.course-markperiod")
                    marking_period = marking_period_element.text.strip()
                except Exception:
                    marking_period = "N/A"

                print(f"Class: {class_name}, Teacher: {teacher_name}, Marking Period: {marking_period}")

                # Ensure the button is visible in the viewport
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", class_name_element)
                time.sleep(1)  # Short pause after scrolling

                # Ensure the button is clickable and click it
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.course-title")))
                    print(f"Clicking on {class_name} using ActionChains")
                    ActionChains(driver).move_to_element(class_name_element).click().perform()
                except Exception:
                    print(f"ActionChains failed, using JavaScript click for {class_name}")
                    driver.execute_script("arguments[0].click();", class_name_element)

                time.sleep(3)  # Allow class details page to load

                # Call function to scrape assignments
                __scrape_assignment(class_name, driver, data_output_format)

                # Return to gradebook page
                click_grade_book(driver)

                # Ensure gradebook page reloads before next iteration
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gb-class-header.gb-class-row")))
                time.sleep(3)

            except Exception as e:
                print(f"Error processing class {class_name}: {e}")
        break  # Exit the loop after processing all classes

