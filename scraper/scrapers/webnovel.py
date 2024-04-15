from selenium import webdriver

from .strategy import NovelScraperStrategy
from scraper.text_cleaning import clean_chapter
from scraper.novel import Chapter, Novel


class WebnovelScraper(NovelScraperStrategy):
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
        
        self.driver.execute_script("document.querySelectorAll('.para-comment').forEach(comment => comment.parentElement.removeChild(comment));");
        self.driver.execute_script("document.querySelectorAll('.para-comment_num').forEach(comment => comment.parentElement.removeChild(comment));");
        chapters_rep = self.driver.execute_script("""
            const all_chapters = [...document.querySelectorAll('.chapter_content')];
            return all_chapters.map(chapter => {
                const title = chapter.querySelector(".cha-tit").textContent;
                const content = chapter.querySelector(".cha-words").textContent;
                return {title, content, scenes: []};
            });
        """)
        chapters = [Chapter(chapter_rep) for chapter_rep in chapters_rep]
        return Novel(
            self.title,
            self.url,
            self.driver.execute_script("return window.location.href;"),
            [clean_chapter(chapter) for chapter in chapters],
        )
