from urllib.parse import urlparse
from selenium import webdriver

from . import (
    webnovel,
)


class NovelScraperFactory:
    def create(self, driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> str:
        parsed_url = urlparse(novel_page_url)
        website = parsed_url.hostname
        return SCRAPER_MAP[website](driver, novel_title, novel_page_url)


SCRAPER_MAP = {
    "www.webnovel.com": webnovel.WebnovelScraper,
}
