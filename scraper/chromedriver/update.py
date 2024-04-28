import re
import shutil
import io
import json
import zipfile
import requests
import subprocess
from pathlib import Path
from loguru import logger


ENFORCED_CHROME_VERSION = "123.0.6312.122"
GOOGLE_CHROME_LAST_KNOWN_GOOD_VERSION_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
GOOGLE_CHROME_KNOWN_GOOD_VERSIONS_WITH_DOWNLOADS_URL = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
CHROME_PKG_DIRECTORY = Path(__file__).parent
GOOGLE_CHROME_DIRECTORY = CHROME_PKG_DIRECTORY / "chrome-linux64"
GOOGLE_CHROME_BINARY = GOOGLE_CHROME_DIRECTORY / "chrome"
CHROMEDRIVER_DIRECTORY = CHROME_PKG_DIRECTORY / "chromedriver-linux64"
CHROMEDRIVER_BINARY = CHROMEDRIVER_DIRECTORY / "chromedriver"


def check_for_updates(*, version: str = None) -> None:
    if version is None:
        version = get_latest_google_chrome_version()

    google_chrome_version = get_version(GOOGLE_CHROME_BINARY)
    if google_chrome_version is not None:
        logger.info(f"Found google chrome version {google_chrome_version}")

    if google_chrome_version is None:
        logger.warning("Google chrome not installed")
        install_google_chrome(version)
    elif google_chrome_version != version:
        logger.warning(f"Updating google chrome")
        remove_google_chrome()
        install_google_chrome(version)

    google_chrome_version = get_version(GOOGLE_CHROME_BINARY)
    chromedriver_version = get_version(CHROMEDRIVER_BINARY)

    if chromedriver_version == google_chrome_version:
        logger.info("Chrome driver is up to date")
        return

    if chromedriver_version is None:
        logger.warning(f"Chrome driver is not installed")
    else:
        logger.warning(f"Chrome driver version does not match google chrome")
        remove_chromedriver()

    install_chromedriver(google_chrome_version)


def get_version(executable: str) -> str:
    output, error = subprocess.Popen(f"{executable} --version", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if error:
        return None
    
    matches = re.search("\\d*\\.\\d*\\.\\d*\\.\\d*", output.decode("utf-8"))
    return matches.group(0)


def get_latest_google_chrome_version() -> None:
    response = requests.get(GOOGLE_CHROME_LAST_KNOWN_GOOD_VERSION_URL)
    response.raise_for_status()
    latest = json.loads(response.text)
    return latest["channels"]["Stable"]["version"]


def install_google_chrome(version: str) -> None:
        logger.warning(f"Installing google chrome version {version}")
        download_url = get_chrome_dependency_download_url(version, "chrome")
        install_chrome_dependency(download_url)
        logger.info(f"Google chrome installed succesfully")


def install_chromedriver(version: str) -> None:
        logger.warning(f"Installing chrome driver version {version}")
        download_url = get_chrome_dependency_download_url(version, "chromedriver")
        install_chrome_dependency(download_url)
        logger.info(f"Chrome driver installed succesfully")


def get_chrome_dependency_download_url(version: str, dependency: str) -> str:
    response = requests.get(GOOGLE_CHROME_KNOWN_GOOD_VERSIONS_WITH_DOWNLOADS_URL)
    response.raise_for_status()
    good_versions = json.loads(response.text)["versions"]

    version = next(iter(v for v in good_versions if v["version"] == version))
    downloads = version["downloads"]
    if dependency not in downloads:
        dependency_map = { "chrome": "google chrome" }
        dependency_name = dependency_map[dependency] if dependency in dependency_map else dependency
        msg = f"Unable to find {dependency_name} version {version}"
        raise RuntimeError(msg)

    dependency_downloads = downloads[dependency]
    linux_download = next(iter(d for d in dependency_downloads if d["platform"] == "linux64"))
    return linux_download["url"]


def install_chrome_dependency(download_url: str) -> None:
    response = requests.get(download_url, stream=True)
    response.raise_for_status()
    unpack_chrome_dependency(response.content)


def remove_chromedriver() -> None:
    try:
        shutil.rmtree(CHROMEDRIVER_DIRECTORY)
    except:  # Just making sure the directory is deleted, we don't care if it was already not there
        pass


def remove_google_chrome() -> None:
    try:
        shutil.rmtree(GOOGLE_CHROME_DIRECTORY)
    except:  # Same as "remove_chromedriver()"
        pass


def unpack_chrome_dependency(dependency_content: bytes) -> None:
    with zipfile.ZipFile(io.BytesIO(dependency_content)) as zip_file:
        zip_file.extractall(CHROME_PKG_DIRECTORY)


check_for_updates(version=ENFORCED_CHROME_VERSION)
