from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor, RequestsExtractor


class NewspapersParser(BaseParser):

    def __init__(self, parser, mode="selenium"):
        self.PARSER = parser
        self.RMODE = mode
        super().__init__()

    def call_extractor(self):
        if self.RMODE == "selenium":
            self.extractor = SeleniumExtractor(
                executable_path=self.BASE_DRIVER
            )
        elif self.RMODE == "requests":
            self.extractor = RequestsExtractor()

    def parse(self, url):
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
