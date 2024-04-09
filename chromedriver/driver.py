from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from .update import CHROMEDRIVER_PATH


def create_chrome_driver() -> webdriver.Chrome:
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=service, options=options)
