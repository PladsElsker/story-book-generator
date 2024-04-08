import pathlib
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from chromedriver.update import CHROMEDRIVER_DIRECTORY


CHROMEDRIVER_PATH = pathlib.Path(CHROMEDRIVER_DIRECTORY) / "chromedriver"


class NovelScraper:
    def __init__(self, url: str) -> None:
        self.url = url
        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

    def scrape_chapters(self) -> list[str]:
        raise NotImplementedError()


class WebnovelScraper(NovelScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def scrape_chapters(self) -> list[str]:
        pass


SCRAPER_MAP = {
    "www.webnovel.com": WebnovelScraper,
}


class ScraperFactory:
    def create(self, novel_page_url: str, *, website: str = None) -> str:
        if not website:
            parsed_url = urlparse(novel_page_url).netloc
            website = parsed_url

        return SCRAPER_MAP[website](novel_page_url)


scraper = ScraperFactory().create("https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705")
scraper.scrape_chapters()
