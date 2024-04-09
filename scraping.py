import json
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from chromedriver import CHROMEDRIVER_PATH
import text_cleaning


SCRAPED_NOVEL_DIRECTORY = Path("scraped_novels")


class NovelScraper:
    def __init__(self, url: str) -> None:
        self.url = url
        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=service, options=options)

        self.driver.get(url)
        self.driver.execute_script("document.querySelector('#j_read').click();")

    def scrape_chapters(self) -> list[str]:
        raise NotImplementedError()

    def close(self):
        self.driver.quit()


class WebnovelScraper(NovelScraper):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    def scrape_chapters(self) -> list[str]:
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
        
        chapters = json.loads(self.driver.execute_script("""
            const all_chapters = [...document.querySelectorAll('.chapter_content')];
            console.log("test-1-2");  
            return JSON.stringify(all_chapters.map(chapter => {
                const title = chapter.querySelector(".cha-tit").textContent;
                const paragraph = chapter.querySelector(".cha-words").textContent;
                return {title, paragraph};
            }));
        """))
        chapters["main_page_url"] = self.url;
        chapters["last_scraped_url"] = self.driver.execute_script("return window.location.href;");
        chapters = [text_cleaning.clean_chapter(chapter) for chapter in chapters]
        return chapters


SCRAPER_MAP = {
    "www.webnovel.com": WebnovelScraper,
}


class ScraperFactory:
    def create(self, webdriver: webdriver.Chrome, novel_page_url: str, *, website: str = None) -> str:
        if not website:
            parsed_url = urlparse(webdriver, novel_page_url).netloc
            website = parsed_url

        return SCRAPER_MAP[website](novel_page_url)


scraper = ScraperFactory().create("https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705")
scraper.scrape_chapters()
scraper.close()

"""
- Comprends pas pourquoi le scraping serait fait dans l'extension chrome. 
    -> Le user va voir les pages bouger à des vitesses fulgurantes / tab ouverte à côté qui n'est pas utilisée. 

- Pourquoi markdown? On peut tu sauvegarder les chapitres en json à la place? 
- Obliger les modèles d'image et de son à avoir le même paragraphe avec lequel travailler semble être arbitraire / inutile. 
    -> On pourrait très bien synchroniser l'image avec ses propres paragraphes, et générer la voix "phrase par phrase", par exemple. 

- Une idée que j'ai eu pour l'audio avec Louis pour guider un tts avec RVC: 
    x = tts(text, rvc(voice_sample))
    x = weighted_sum(x, rvc(x))
"""
