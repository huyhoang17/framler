from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor


class DanTriParser(BaseParser):

    BASE_URL = "https://dantri.com.vn"
    PARSER = "DanTri"

    def __init__(self, mode="selenium"):
        self.mode = mode
        super().__init__()

    def call_extractor(self, mode):
        self.extractor = SeleniumExtractor(
            executable_path=self.BASE_DRIVER
        )

    def parse(self, url, mode="selenium"):
        self.article = Article(url)
        self.soup = self.get_soup(url)
        self.cfg = self.get_config()
        super().parse(url)

        self.article.authors = []
        self.article.text.replace(self.article.tags, "")

        # image_urls
        self.article.image_urls = [
            img.img['src']
            for img in self.soup.find_all(class_="image")
        ]

        # top image
        self.article.top_image_url = self.article.image_urls[0]

        return self.article


class AutoCrawlParser(BaseParser):

    def __init__(self):
        pass

    def __str__(self):
        pass
