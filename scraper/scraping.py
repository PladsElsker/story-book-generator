import click
from selenium import webdriver
from novel_storage import make_novel_directory, get_last_scraped_url, merge_scraped

from chromedriver import create_chrome_driver
from scrapers import NovelScraperFactory
from text_cleaning import url_to_novel_key


def novel_scrape(driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> None:
    novel_key = url_to_novel_key(novel_page_url)
    make_novel_directory(novel_key)
    last_scraped_url = get_last_scraped_url(novel_key)
    if last_scraped_url:
        novel_page_url = last_scraped_url

    scraper = NovelScraperFactory().create(driver, novel_title, novel_page_url)
    scraped_data = scraper.scrape()
    merge_scraped(novel_key, scraped_data)


@click.command()
@click.option("--novel-title", "-t", required=True, type=str)
@click.option("--novel-page-url", "-u", required=True, type=str)
def cli(novel_title: str, novel_page_url: str):
    driver = create_chrome_driver()
    novel_scrape(driver, novel_title, novel_page_url)
    driver.quit()


if __name__ == "__main__":
    cli()
