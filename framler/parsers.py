from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor, RequestsExtractor

import os
import yaml


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
        # TODO: change API
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

    def load_config(self, fpath="html.yaml"):
        super().load_config()
        self.BASE_CONFIG = os.path.join(
            os.path.dirname(__file__), fpath)

        with open(self.BASE_CONFIG) as f:
            self.auto_cfg = yaml.load(f)

    def parse_tag(self, tree, tag_name, link=False):
        pass

    def auto_parse(self, url):

        cfg = self.auto_cfg
        tree = self.get_xpath_tree(url)
        article = Article(url)

        # URL
        article.url = url

        # title::text
        article.title = self.get_elements_by_tag(
            tree, cfg["title"]["attrs"],
            cfg["title"]["vals"],
            cfg["title"]["name"]
        )

        # authors::text
        article.authors = self.get_elements_by_tag(
            tree, cfg["authors"]["attrs"],
            cfg["authors"]["vals"],
            cfg["authors"]["name"]
        )

        # text::text
        article.text = " ".join(self.get_elements_by_tag(
            tree, cfg["text"]["attrs"],
            cfg["text"]["vals"],
            cfg["text"]["name"]
        ))

        # published_date::text
        article.published_date = " ".join(self.get_elements_by_tag(
            tree, cfg["pubd"]["attrs"],
            cfg["pubd"]["vals"],
            cfg["pubd"]["name"]
        ))

        # tags::text
        article.tags = self.get_elements_by_tag(
            tree, cfg["tags"]["attrs"],
            cfg["tags"]["vals"],
            cfg["tags"]["name"]
        )

        # image_urls::links
        article.image_urls = self.get_links_by_tag(
            tree, cfg["image_urls"]["attrs"],
            cfg["image_urls"]["vals"],
            cfg["image_urls"]["src_attrs"],
            cfg["image_urls"]["name"]
        )

        return article
