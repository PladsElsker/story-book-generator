from selenium import webdriver
from abc import ABC, abstractmethod

from scraper.novel import Novel


class NovelScraperStrategy(ABC):
    def __init__(self, driver: webdriver.Chrome, title: str, url: str) -> None:
        self.title = title
        self.url = url
        self.driver = driver
        self.driver.get(url)

    @abstractmethod
    def scrape(self) -> Novel:
        raise NotImplementedError()
