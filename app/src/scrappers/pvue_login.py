import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scrappers.init_webdriver import create_webdriver


def login_to_website(url: str, username: str, password: str):

    """
    Logs into the Edupoint ParentVUE website and returns the Selenium WebDriver instance.

    Args:
        url:
        username (str): User's email or username.
        password (str): User's password.

    Returns:
        webdriver.Chrome: Selenium WebDriver instance after successful login.
    """

    driver = create_webdriver()

    try:
        # Open the login page
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Find and fill in the login credentials
        username_input = driver.find_element(By.ID, "ctl00_MainContent_username")
        password_input = driver.find_element(By.ID, "ctl00_MainContent_password")

        username_input.send_keys(username)
        password_input.send_keys(password)

        # Submit the login form
        password_input.send_keys(Keys.RETURN)

        # Wait for login to complete
        time.sleep(5)  # Adjust this based on site loading speed

        # Return the driver instance after login
        return driver

    except Exception as e:
        print(f"Error logging in: {e}")
        driver.quit()
        return None



