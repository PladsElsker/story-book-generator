import json
import tempfile
import subprocess
from urllib.parse import urlparse
from selenium import webdriver

from chromedriver import create_chrome_driver
from text_cleaning import clean_chapter


def novel_scrape(driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> None:
    novel_key = novel_page_url.replace("/", "_").replace(":", "_")
    output, error = subprocess.Popen(f"./novels.sh {novel_key} get-last-scraped-url", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if not error:
        novel_page_url = output.decode("utf-8")

    scraper = NovelScraperFactory().create(driver, novel_title, novel_page_url)
    scraped_data = scraper.scrape()
    
    with tempfile.NamedTemporaryFile(mode="wb") as temp_file:
        temp_file.write(json.dumps(scraped_data).encode("utf-8"))
        output, error = subprocess.Popen(f"./novels.sh {novel_key} merge-scraped {temp_file.name}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if error:
            raise RuntimeError(error.decode("utf-8"))


class NovelScraperFactory:
    def create(self, driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> str:
        parsed_url = urlparse(novel_page_url)
        website = parsed_url.netloc.split(":")[0]
        return SCRAPER_MAP[website](driver, novel_title, novel_page_url)


class NovelScraper:
    def __init__(self, driver: webdriver.Chrome, title: str, url: str) -> None:
        self.title = title
        self.url = url
        self.driver = driver
        self.driver.get(url)

    def scrape(self) -> list[str]:
        raise NotImplementedError()


class WebnovelScraper(NovelScraper):
    def __init__(self, driver: webdriver.Chrome, title: str, url: str) -> None:
        super().__init__(driver, title, url)

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
        scraped["title"] = self.title
        scraped["first_chapter_url"] = self.url
        scraped["last_scraped_url"] = self.driver.execute_script("return window.location.href;")
        scraped["chapters"] = [clean_chapter(chapter) for chapter in chapters]
        return scraped


SCRAPER_MAP = {
    "www.webnovel.com": WebnovelScraper,
}


if __name__ == "__main__":
    driver = create_chrome_driver()
    # novel_scrape(driver, "Mushoku Tensei", "https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705/volume-1-prologue_72736022055680334")
    novel_scrape(driver, "Reincarnated With The Mind Control Powers In Another World", "https://www.webnovel.com/book/reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705/chapter-1_67999384498920800")
    driver.quit()
