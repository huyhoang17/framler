from abc import ABC, abstractmethod

from .extractors import SeleniumExtractor, RequestsExtractor


class BaseExtractor(ABC):

    @abstractmethod
    def get_content(self):
        pass


class BaseParser(object):

    def __init__(self):
        self.call_extractor()

    def get_content(self, url):
        return self.extractor.get_content(url)

    def get_soup(self, url):
        return self.extractor.get_soup(url)

    def get_clean_text(self):
        pass

    # def get_strs(self, seq, class_):
    #     return remove_multiple_space(' '.join(
    #         [s.get_text() for s in self.soup.find_all(class_=class_)])
    #     ).strip()

    def call_extractor(self, mode="requests"):
        if mode == "requests":
            self.extractor = RequestsExtractor()
        elif mode == "selenium":
            self.extractor = SeleniumExtractor()

    def parse(self, url, mode='requests'):
        pass
