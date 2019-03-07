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

    def parse_tag(self, tree, filter_, **kwargs):
        # arc_attrs::to get links, not text
        src_attrs = kwargs.get("src_attrs", None)

        attrs = kwargs.get("attrs", None)
        vals = kwargs.get("vals", None)
        name = kwargs.get("name", None)

        if src_attrs is not None:
            result = self.get_links_by_tag(
                tree, attrs, vals, src_attrs, name
            )
        else:
            result = self.get_elements_by_tag(
                tree, attrs, vals, name
            )

        if filter_:
            result = self.filter_content(result)

        return result

    # START::main method
    def get_auto_text(self, text):
        pass

    def get_auto_title(self, title):
        pass
    # END::main method

    def auto_parse(self, url):

        cfg = self.auto_cfg
        tree = self.get_xpath_tree(url)
        article = Article(url)

        # URL
        article.url = url

        # title::text
        article.title = self.parse_tag(tree, True, **cfg["title"])

        # authors::text
        article.authors = self.parse_tag(tree, False, **cfg["authors"])

        # text::text
        article.text = self.parse_tag(tree, True, **cfg["text"])

        # published_date::text
        article.published_date = self.parse_tag(tree, True, **cfg["pubd"])

        # tags::text
        article.tags = self.parse_tag(tree, False, **cfg["tags"])

        # image_urls::links
        article.image_urls = self.parse_tag(tree, False, **cfg["image_urls"])
        return article
