import sys
if "." not in sys.path:
    sys.path[0:0] = ["."]

from selenium import webdriver

from chromedriver import create_chrome_driver
from scrapers import NovelScraperFactory
from text_cleaning import url_to_novel_key
from storage_handler import ensure_novel_directory_created, get_novel, merge_scraped


def novel_scrape(driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> None:
    novel_key = url_to_novel_key(novel_page_url)
    ensure_novel_directory_created(novel_key, novel_title, novel_page_url)
    novel_page_url = get_novel(novel_key)["last_scraped_url"]

    scraper = NovelScraperFactory().create(driver, novel_title, novel_page_url)
    scraped_data = scraper.scrape()
    merge_scraped(novel_key, scraped_data)


def cli():
    driver = create_chrome_driver()
    # novel_scrape(driver, "Mushoku Tensei", "https://www.webnovel.com/book/mushoku-tensei-full-version_27096259406624705/volume-1-prologue_72736022055680334")
    novel_scrape(driver, "Reincarnated With The Mind Control Powers In Another World", "https://www.webnovel.com/book/reincarnated-with-the-mind-control-powers-in-another-world._25331737205609705/chapter-1_67999384498920800")
    driver.quit()


if __name__ == "__main__":
    cli()
