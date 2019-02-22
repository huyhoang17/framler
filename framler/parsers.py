from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor, RequestsExtractor


class NewspapersParser(BaseParser):

    def __init__(self, parser, mode="selenium"):
        self.PARSER = parser
        self.mode = mode
        super().__init__()

    def call_extractor(self, mode="selenium"):
        if mode == "selenium":
            self.extractor = SeleniumExtractor(
                executable_path=self.BASE_DRIVER
            )
        elif mode == "requests":
            self.extractor = RequestsExtractor()

    def parse(self, url, mode="selenium"):
        self.article = Article(url)
        self.soup = self.get_soup(url)
        self.cfg = self.get_config()
        super().parse(url)

        return self.article


class AutoCrawlParser(BaseParser):

    def __init__(self):
        pass

    def __str__(self):
        pass
