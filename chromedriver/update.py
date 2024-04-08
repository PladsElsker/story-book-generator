import os
import io
import pathlib
import zipfile
import requests
import subprocess
from loguru import logger


CHROMEDRIVER_DIRECTORY = pathlib.Path(__file__).parent / "chromedriver-linux64"
LATEST_RELEASE_ROUTE = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
CHROME_DRIVER_DOWNLOAD_URL = "https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"


def check_for_updates():
    try:
        chrome_version_process = subprocess.Popen("google-chrome --version", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = chrome_version_process.communicate()
        chrome_version = output.decode("utf-8").split(" ")[2]
    except Exception as e:
        logger.error("Google chrome is not installed")
        raise e

    try:
        chromedriver_version_process = subprocess.Popen(f"{CHROMEDRIVER_DIRECTORY}/chromedriver -v", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = chromedriver_version_process.communicate()
        chromedriver_version = output.decode("utf-8").split(" ")[1]
        if chromedriver_version == chrome_version:
            logger.debug("Chrome driver is up to date")
            return
    except:
        pass

    logger.debug(f"Installing chrome driver {chrome_version}")

    remove_webdriver()

    download_url = CHROME_DRIVER_DOWNLOAD_URL.format(version=chrome_version)
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        unpack_webdriver(response.content)
    else:
        logger.error(f"Failed to download chrome driver from {download_url}")
    
    logger.debug(f"Chrome driver installed succesfully")


def remove_webdriver():
    try:
        os.remove(CHROMEDRIVER_DIRECTORY)
    except FileNotFoundError:
        pass


def unpack_webdriver(webdriver_content):
    try:
        os.mkdir(CHROMEDRIVER_DIRECTORY)
    except FileExistsError:
        pass
    
    with zipfile.ZipFile(io.BytesIO(webdriver_content)) as zip_file:
        zip_file.extractall(CHROMEDRIVER_DIRECTORY)
