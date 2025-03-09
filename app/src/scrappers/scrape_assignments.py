import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from scrappers.scrape_grades import click_grade_book


def process_assignments(driver, data_output_format):
    click_grade_book(driver)
    __iterate_over_each_class(driver, data_output_format)

#TODO scraping assignments now. but still needs some refinement. its pulling all of the hidden rows and total row, and not considering the header row as a header row.
def __scrape_assignment(driver, data_output_format, class_meta_data):
    class_name = class_meta_data['Class']
    teacher_name = class_meta_data['Teacher']
    marking_period = class_meta_data['MarkingPeriod']

    print(f"📌 Loaded Page {class_name}. Start Scraping!")

    assignments_data = []

    try:
        # ✅ Ensure table is fully loaded before proceeding
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'dx-datagrid-rowsview')]"))
        )

        # ✅ Scroll table into view to handle lazy loading
        assignments_grid = driver.find_element(By.XPATH, "//div[contains(@class,'dx-datagrid-rowsview')]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", assignments_grid)
        time.sleep(2)  # Ensure lazy-loaded content is visible

        # ✅ Locate assignment rows that have `role="row"`
        assignment_rows = driver.find_elements(By.XPATH, "//tbody/tr[@role='row']")

        print(f"✅ Found {len(assignment_rows)} assignment(s) for {class_name}.")

        if not assignment_rows:
            print(f"⚠️ No assignments found for {class_name}.")
            return []

        # ✅ Extract assignment details from each row
        for row in assignment_rows:
            try:
                # **Locate all <td> elements**
                td_elements = row.find_elements(By.TAG_NAME, "td")

                # ✅ Ensure there are enough columns before accessing specific indices
                if len(td_elements) < 4:  # Adjust based on the minimum columns needed
                    print(f"⚠️ Skipping row due to insufficient columns: {len(td_elements)}")
                    continue  # Skip to the next row

                assignment_category = td_elements[0].text.strip()  # Formative, Homework, etc.
                weight = td_elements[1].text.strip()  # Weight percentage
                score = td_elements[2].text.strip()  # Actual score
                possible_score = td_elements[3].text.strip()  # Maximum possible score

                # ✅ Store extracted data
                assignment_info = {
                    "Class": class_name,
                    "Teacher": teacher_name,
                    "Marking Period": marking_period,
                    "Category": assignment_category,
                    "Weight": weight,
                    "Score": score,
                    "Possible Score": possible_score,
                }

                assignments_data.append(assignment_info)
                print(f"📌 Extracted: {assignment_info}")

            except Exception as row_error:
                print(f"⚠️ Error processing an assignment in {class_name}: {row_error}")

    except Exception as e:
        print(f"❌ Error scraping assignments for {class_name}: {e}")

    return assignments_data


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

                class_meta_data = {
                    "Class": class_name,
                    "Teacher": teacher_name,
                    "MarkingPeriod": marking_period,
                }

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
                __scrape_assignment(driver, data_output_format, class_meta_data)

                # Return to gradebook page
                click_grade_book(driver)

                # Ensure gradebook page reloads before next iteration
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gb-class-header.gb-class-row")))
                time.sleep(3)

            except Exception as e:
                print(f"Error processing class {class_name}: {e}")
        break  # Exit the loop after processing all classes

