import json
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from chromedriver import CHROMEDRIVER_PATH
import text_cleaning


SCRAPED_NOVELS_DIRECTORY = Path("scraped_novels")


class NovelScraper:
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:
        self.url = url
        self.driver = driver
        self.driver.get(url)

    def scrape(self) -> list[str]:
        raise NotImplementedError()


class WebnovelScraper(NovelScraper):
    def __init__(self, driver: webdriver.Chrome, url: str) -> None:
        super().__init__(driver, url)
        self.driver.execute_script("document.querySelector('#j_read').click();")

    def scrape(self) -> list[str]:
        end_reached = False

        while not end_reached:
            end_reached = self.driver.execute_async_script("""
                const callback = arguments[arguments.length - 1];
                const previous_height = document.body.scrollHeight;
                                                                
                window.scrollTo(0, document.body.scrollHeight);
                let interval_handle = null;
                let timeout_handle = null;
                handle = setInterval(() => {
                    if(previous_height != document.body.scrollHeight){
                        clearInterval(interval_handle);
                        clearTimeout(timeout_handle);
                        callback('');
                    }
                }, 1000);
                timeout_handle = setTimeout(() => callback('done'), 4000);
            """)
        
        chapters = json.loads(self.driver.execute_script("""
            const all_chapters = [...document.querySelectorAll('.chapter_content')];
            console.log("test-1-2");  
            return JSON.stringify(all_chapters.map(chapter => {
                const title = chapter.querySelector(".cha-tit").textContent;
                const paragraph = chapter.querySelector(".cha-words").textContent;
                return {title, paragraph};
            }));
        """))
        scraped = {}
        scraped["chapters"] = [text_cleaning.clean_chapter(chapter) for chapter in chapters]
        scraped["main_page_url"] = self.url;
        scraped["last_scraped_url"] = self.driver.execute_script("return window.location.href;");
        return scraped


SCRAPER_MAP = {
    "www.webnovel.com": WebnovelScraper,
}


class ScraperFactory:
    def create(self, driver: webdriver.Chrome, novel_page_url: str, *, website: str = None) -> str:
        if not website:
            parsed_url = urlparse(novel_page_url).netloc
            website = parsed_url

        return SCRAPER_MAP[website](driver, novel_page_url)


if __name__ == "__main__":
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    # scraper = ScraperFactory().create(driver, "https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705")
    scraper = ScraperFactory().create(driver, "https://www.webnovel.com/book/strongest-mage-with-the-lust-system_22715595806121505")
    scraped = scraper.scrape()
    driver.quit()
