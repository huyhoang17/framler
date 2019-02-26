from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor, RequestsExtractor


def call_extractor(mode):
    if mode == "selenium":
        extractor = SeleniumExtractor()
    elif mode == "requests":
        extractor = RequestsExtractor()
    return extractor


class NewspapersParser(BaseParser):

    def __init__(self, parser, mode="selenium"):
        self.PARSER = parser
        self.RMODE = mode
        super().__init__()

    def call_extractor(self):
        self.extractor = call_extractor(self.RMODE)

    def parse(self, url):
        self.article = Article(url)
        self.soup = self.get_soup(url)
        super().parse(url)

        return self.article


class AutoCrawlParser(BaseParser):

    def __init__(self, mode="selenium"):
        self.RMODE = mode
        super().__init__()

    def call_extractor(self):
        self.extractor = call_extractor(self.RMODE)
