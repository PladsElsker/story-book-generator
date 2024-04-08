from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from chromedriver import CHROMEDRIVER_PATH


class NovelScraper:
    def __init__(self, url: str) -> None:
        self.url = url
        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

    def scrape_chapters(self) -> list[str]:
        raise NotImplementedError()

    def close(self):
        self.driver.quit()


class WebnovelScraper(NovelScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def scrape_chapters(self) -> list[str]:
        self.driver.execute_script("document.querySelector('#j_read').click();")
        for _ in range(350):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_async_script("setTimeout(() => arguments[arguments.length - 1](''), 500);")


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
scraper.close()
