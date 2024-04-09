import os
import shutil
import io
import zipfile
import requests
import subprocess
from pathlib import Path
from loguru import logger


CHROMEDRIVER_DIRECTORY = Path(__file__).parent / "chromedriver-linux64"
CHROMEDRIVER_PATH = CHROMEDRIVER_DIRECTORY / "chromedriver"
CHROME_DRIVER_DOWNLOAD_URL = "https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"


def check_for_updates() -> None:
    chrome_version = get_google_chrome_version_or_raise()
    chromedriver_version = get_chromedriver_version()

    logger.info(f"Found google chrome version {chrome_version}")

    if chromedriver_version == chrome_version:
        logger.info("Chrome driver is up to date")
        return

    if chromedriver_version is None:
        logger.warning(f"Chrome driver is not installed")
    else:
        logger.warning(f"Chrome driver version does not match google chrome")
    
    logger.warning(f"Installing chrome driver {chrome_version}")

    remove_chromedriver()
    download_url = CHROME_DRIVER_DOWNLOAD_URL.format(version=chrome_version)
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    unpack_chromedriver(response.content)
    
    logger.info(f"Chrome driver installed succesfully")


def get_google_chrome_version_or_raise() -> str:
    output, error = run_command("google-chrome --version")
    if error:
        logger.error("Google chrome is not installed")
        raise RuntimeError(error.decode("utf-8"))
    
    return output.decode("utf-8").split(" ")[2]


def get_chromedriver_version() -> str:
    output, error = run_command(f"{CHROMEDRIVER_PATH} -v")
    if error:
        return None
    
    return output.decode("utf-8").split(" ")[1]


def run_command(command: str) -> tuple[str]:
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()


def remove_chromedriver() -> None:
    try:
        shutil.rmtree(CHROMEDRIVER_DIRECTORY)
    except:
        pass


def unpack_chromedriver(chromedriver_content: bytes) -> None:
    try:
        os.mkdir(CHROMEDRIVER_DIRECTORY)
    except FileExistsError:
        pass
    
    with zipfile.ZipFile(io.BytesIO(chromedriver_content)) as zip_file:
        zip_file.extractall(CHROMEDRIVER_DIRECTORY.parent)


check_for_updates()
