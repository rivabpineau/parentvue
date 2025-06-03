import os
import sys
from unittest.mock import MagicMock, patch

# Add app/src to path so modules can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app', 'src'))

import scrappers.scrape_grades as scrape_grades
import scrappers.scrape_assignments as scrape_assignments


def make_grade_row(class_text, teacher_text, period_text, grade_text, score_text):
    row = MagicMock()

    def find_element_side_effect(by, value):
        if 'course-title' in value:
            return MagicMock(text=class_text)
        if 'teacher' in value:
            return MagicMock(text=teacher_text)
        if 'course-markperiod' in value:
            return MagicMock(text=period_text)
        if 'mark' in value:
            return MagicMock(text=grade_text)
        if 'score' in value:
            return MagicMock(text=score_text)
        raise Exception('unexpected locator')

    row.find_element.side_effect = find_element_side_effect
    return row


def make_assignment_row(category, weight, score, possible):
    row = MagicMock()
    tds = [
        MagicMock(text=category),
        MagicMock(text=weight),
        MagicMock(text=score),
        MagicMock(text=possible),
    ]
    row.find_elements.side_effect = lambda by, value: tds if value == 'td' else []
    return row


def test_process_grades_calls_dependencies():
    driver = MagicMock()
    grade_data = [{'Class': 'Algebra'}]
    with patch('scrappers.scrape_grades.__click_grade_book') as mock_click, \
         patch('scrappers.scrape_grades.__scrape_grades', return_value=grade_data) as mock_scrape, \
         patch('scrappers.scrape_grades.__save_grades') as mock_save:
        scrape_grades.process_grades(driver, 'json')
        mock_click.assert_called_once_with(driver)
        mock_scrape.assert_called_once_with(driver)
        mock_save.assert_called_once_with(grade_data, 'json')


def test_scrape_grades_parses_rows():
    driver = MagicMock()
    row = make_grade_row('1: Algebra', 'Mr. Doe', 'MP1', 'A', '100%')
    driver.find_elements.return_value = [row]
    with patch('scrappers.scrape_grades.__date_scraped', '2024-01-01_000000'):
        result = scrape_grades.__scrape_grades(driver)
    assert result == [{
        'Class': 'Algebra',
        'Teacher': 'Mr. Doe',
        'Period': 'MP1',
        'Grade': 'A',
        'Score': '100%',
        'date_scraped': '2024-01-01_000000',
    }]


def test_process_assignments_calls_dependencies():
    driver = MagicMock()
    with patch('scrappers.scrape_assignments.click_grade_book') as mock_click, \
         patch('scrappers.scrape_assignments.__iterate_over_each_class') as mock_iter:
        scrape_assignments.process_assignments(driver, 'csv')
        mock_click.assert_called_once_with(driver)
        mock_iter.assert_called_once_with(driver, 'csv')


def test_scrape_assignment_parses_rows():
    driver = MagicMock()
    row = make_assignment_row('Homework', '10%', '9', '10')
    driver.find_elements.return_value = [row]
    driver.find_element.return_value = MagicMock()
    with patch('scrappers.scrape_assignments.WebDriverWait') as MockWait:
        MockWait.return_value.until.return_value = None
        class_meta = {'Class': 'Algebra', 'Teacher': 'Mr. Doe', 'MarkingPeriod': 'MP1'}
        result = scrape_assignments.__scrape_assignment(driver, 'json', class_meta)
    assert result == [{
        'Class': 'Algebra',
        'Teacher': 'Mr. Doe',
        'Marking Period': 'MP1',
        'Category': 'Homework',
        'Weight': '10%',
        'Score': '9',
        'Possible Score': '10',
    }]
