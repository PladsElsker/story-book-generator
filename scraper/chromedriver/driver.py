from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from .update import GOOGLE_CHROME_BINARY, CHROMEDRIVER_BINARY


def create_chrome_driver(*, headless: bool = False, dark_mode: bool = True) -> webdriver.Chrome:
    service = Service(executable_path=CHROMEDRIVER_BINARY)
    options = Options()
    options.binary_location = str(GOOGLE_CHROME_BINARY)
    if headless:
        options.add_argument("--headless")
    
    if dark_mode:
        options.add_argument('--force-dark-mode')

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=service, options=options)
