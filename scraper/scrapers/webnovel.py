from selenium import webdriver

from .novel_scraper_strategy import NovelScraper
from text_cleaning import clean_chapter


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
