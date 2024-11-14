from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os


def test_create():
    DEFAULT_URL = "http://localhost:5000"
    url = os.getenv("EMPLOYEES_URL", DEFAULT_URL)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.find_element(By.ID, "name").send_keys("John Doe")
    driver.find_element(By.ID, "submit-input").click()

    message = driver.find_element(By.ID, "message-paragraph").text
    assert message == "Employee has been created"

    driver.quit()
