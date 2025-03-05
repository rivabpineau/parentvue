from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_webdriver():
    # Setup Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximize window TODO: either parameratize or or create config obj.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver