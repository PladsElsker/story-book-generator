from selenium import webdriver


class NovelScraper:
    def __init__(self, driver: webdriver.Chrome, title: str, url: str) -> None:
        self.title = title
        self.url = url
        self.driver = driver
        self.driver.get(url)

    def scrape(self) -> list[str]:
        raise NotImplementedError()
