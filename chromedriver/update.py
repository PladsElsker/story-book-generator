import os
import shutil
import io
import json
import zipfile
import requests
import subprocess
from pathlib import Path
from loguru import logger


CHROMEDRIVER_DIRECTORY = Path(__file__).parent / "chromedriver-linux64"
CHROMEDRIVER_PATH = CHROMEDRIVER_DIRECTORY / "chromedriver"
GOOGLE_CHROME_KNOWN_GOOD_VERSIONS_URL = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"


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

    download_url = get_chromedriver_download_url(chrome_version)
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


def get_chromedriver_download_url(chrome_version: str) -> str:
    response = requests.get(GOOGLE_CHROME_KNOWN_GOOD_VERSIONS_URL)
    response.raise_for_status()
    good_versions = json.loads(response.text)["versions"]

    version = next(iter(v for v in good_versions if v["version"] == chrome_version))
    downloads = version["downloads"]
    if "chromedriver" not in downloads:
        msg = f"Unable to find a matching chromedriver version for google chrome {chrome_version}"
        raise RuntimeError(msg)

    chromedriver_downloads = downloads["chromedriver"]
    linux_download = next(iter(d for d in chromedriver_downloads if d["platform"] == "linux64"))
    return linux_download["url"]


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
