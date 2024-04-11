import json
import tempfile
import subprocess
from selenium import webdriver

from chromedriver import create_chrome_driver
from scrapers import NovelScraperFactory


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


if __name__ == "__main__":
    driver = create_chrome_driver()
    # novel_scrape(driver, "Mushoku Tensei", "https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705/volume-1-prologue_72736022055680334")
    novel_scrape(driver, "Reincarnated With The Mind Control Powers In Another World", "https://www.webnovel.com/book/reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705/chapter-1_67999384498920800")
    driver.quit()
