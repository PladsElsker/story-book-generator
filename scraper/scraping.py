import click
import json
import tempfile
import subprocess
from selenium import webdriver

from chromedriver import create_chrome_driver
from scrapers import NovelScraperFactory


def novel_scrape(driver: webdriver.Chrome, novel_title: str, novel_page_url: str) -> None:
    novel_key = novel_page_url.replace("/", "_").replace(":", "_")
    output, error = subprocess.Popen(f"./novels.sh {novel_key} get-last-scraped-url", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if error:
        raise RuntimeError(error.decode("utf-8"))
    elif output:
        novel_page_url = output.decode("utf-8")

    scraper = NovelScraperFactory().create(driver, novel_title, novel_page_url)
    scraped_data = scraper.scrape()
    
    with tempfile.NamedTemporaryFile(mode="wb") as temp_file:
        temp_file.write(json.dumps(scraped_data).encode("utf-8"))
        output, error = subprocess.Popen(f"./novels.sh {novel_key} merge-scraped {temp_file.name}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if error:
            raise RuntimeError(error.decode("utf-8"))


@click.command()
@click.option("--novel-title", "-t", required=True, type=str)
@click.option("--novel-page-url", "-u", required=True, type=str)
def cli(novel_title: str, novel_page_url: str):
    driver = create_chrome_driver()
    novel_scrape(driver, novel_title, novel_page_url)
    driver.quit()


if __name__ == "__main__":
    cli()
