import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def test_create():
    default_url = "http://localhost:5000"
    url = os.getenv("EMPLOYEES_URL", default_url)

    driver_type = os.getenv("SELENIUM_DRIVER", "ChromeDriver")
    if driver_type == "ChromeDriver":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif driver_type == "RemoteWebDriver":
        command_executor = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=command_executor, options=options)
    else:
        raise ValueError(f"Invalid driver: {driver_type}")
    driver.get(url)
    driver.find_element(By.ID, "name").send_keys("John Doe")
    driver.find_element(By.ID, "submit-input").click()

    message = driver.find_element(By.ID, "message-paragraph").text
    assert message == "Employee has been created"

    driver.quit()
