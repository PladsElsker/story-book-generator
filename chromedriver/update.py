import os
import shutil
import io
import pathlib
import zipfile
import requests
import subprocess
from loguru import logger


CHROMEDRIVER_DIRECTORY = pathlib.Path(__file__).parent / "chromedriver-linux64"
CHROMEDRIVER_PATH = CHROMEDRIVER_DIRECTORY / "chromedriver"
CHROME_DRIVER_DOWNLOAD_URL = "https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"


def check_for_updates():
    output, error = run_command("google-chrome --version")
    if error:
        logger.error("Google chrome is not installed")
        raise RuntimeError(error.decode("utf-8"))
    
    chrome_version = output.decode("utf-8").split(" ")[2]
    logger.debug(f"Found google chrome version {chrome_version}")

    output, error = run_command(f"{CHROMEDRIVER_DIRECTORY}/chromedriver -v")
    chromedriver_version = None
    if error:
        logger.debug(f"Chrome driver is not installed")
    else:
        chromedriver_version = output.decode("utf-8").split(" ")[1]
        if chromedriver_version == chrome_version:
            logger.debug("Chrome driver is up to date")
            return
        else:
            logger.debug(f"Chrome driver version does not match google chrome")
    
    logger.debug(f"Installing chrome driver {chrome_version}")
    remove_webdriver()
    download_url = CHROME_DRIVER_DOWNLOAD_URL.format(version=chrome_version)
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        unpack_webdriver(response.content)
    else:
        logger.error(f"Failed to download chrome driver from {download_url}")
    
    logger.debug(f"Chrome driver installed succesfully")


def run_command(command: str) -> tuple[str]:
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()


def remove_webdriver():
    try:
        shutil.rmtree(CHROMEDRIVER_DIRECTORY)
    except:
        pass


def unpack_webdriver(webdriver_content):
    try:
        os.mkdir(CHROMEDRIVER_DIRECTORY)
    except FileExistsError:
        pass
    
    with zipfile.ZipFile(io.BytesIO(webdriver_content)) as zip_file:
        zip_file.extractall(CHROMEDRIVER_DIRECTORY.parent)


check_for_updates()
