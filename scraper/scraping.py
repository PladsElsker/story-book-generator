from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver

from chromedriver import create_chrome_driver
from text_cleaning import clean_chapter


SCRAPED_NOVELS_DIRECTORY = Path.cwd.parent / "novels"


def novel_scrape(driver: webdriver.Chrome, novel_page_url: str) -> None:
    # resume_scraping_page = novel_page_url
    # if novel_page_url in storage:
        # resume_scraping_page = storage[novel_page_url]["last_scraped_url"]

    scraper = NovelScraperFactory().create(driver, novel_page_url)
    scraped_data = scraper.scrape()
    
    # if novel_page_url in storage:
    #     previous_scraped_data = storage[novel_page_url]
    #     first_scraped_title = scraped_data["chapters"][0]["title"]
    #     seem_index = next(iter(i for i, chapter in enumerate([previous_scraped_data["chapters"]]) if chapter["title"] == first_scraped_title))
    #     scraped_data["chapters"][0:0] = previous_scraped_data["chapters"][:seem_index+1]
    
    # storage[novel_page_url] = scraped_data


class NovelScraperFactory:
    def create(self, driver: webdriver.Chrome, novel_page_url: str) -> str:
        parsed_url = urlparse(novel_page_url)
        website = parsed_url.netloc.split(":")[0]
        return SCRAPER_MAP[website](driver, novel_page_url)


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
                }, 50);
                timeout_handle = setTimeout(() => callback('done'), 4000);
            """)
        
        chapters = self.driver.execute_script("""
            const all_chapters = [...document.querySelectorAll('.chapter_content')];
            console.log("test-1-2");  
            return all_chapters.map(chapter => {
                const title = chapter.querySelector(".cha-tit").textContent;
                const content = chapter.querySelector(".cha-words").textContent;
                return {title, content};
            });
        """)
        scraped = {}
        scraped["chapters"] = [clean_chapter(chapter) for chapter in chapters]
        scraped["main_page_url"] = self.url
        scraped["last_scraped_url"] = self.driver.execute_script("return window.location.href;")
        return scraped


SCRAPER_MAP = {
    "www.webnovel.com": WebnovelScraper,
}


if __name__ == "__main__":
    driver = create_chrome_driver()
    novel_scrape(driver, "https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705/volume-1-prologue_72736022055680334")
    # novel_scrape(driver, "https://www.webnovel.com/book/reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705/chapter-1_67999384498920800")

    driver.quit()
