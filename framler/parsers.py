from ._base import BaseParser
from .articles import Article
from .cleaners import remove_multiple_space


# TESTING
class DanTriParser(BaseParser):

    BASE_URL = 'https://dantri.com.vn'

    def __init__(self):
        self.call_extractor()

    def call_extractor(self, mode="requests"):
        super().call_extractor()

    def parse(self, url, mode='requests'):
        self.article = Article(url)
        self.soup = self.get_soup(url)

        # title
        self.article.title = ' '.join(
            [i.get_text() for i in self.soup.find_all('h1')]).strip()

        # text
        text = self.soup.find_all(class_="detail-content")
        self.article.text = remove_multiple_space(
            " ".join([i.get_text() for i in text])).strip()

        # tags
        tags = self.soup.find_all(class_='news-tag-list')
        self.article.tags = remove_multiple_space(
            " ".join([i.get_text() for i in tags])).strip()
        self.article.text.replace(self.article.tags, "")

        # image_urls
        self.article.image_urls = [
            img.img['src']
            for img in self.soup.find_all(class_="image")
        ]

        return self.article


class AutoCrawlParser(BaseParser):

    def __init__(self):
        pass

    def __str__(self):
        pass
