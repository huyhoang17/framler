import os
import yaml
from urllib.parse import urlsplit

from ._base import BaseParser
from .articles import Article
from .extractors import SeleniumExtractor, RequestsExtractor
from .log import get_logger

logger = get_logger(__name__)


def call_extractor(mode):
    if mode == "selenium":
        extractor = SeleniumExtractor()
    elif mode == "requests":
        extractor = RequestsExtractor()
    return extractor


class NewspapersParser(BaseParser):

    def __init__(self, parser, mode="requests"):
        self.PARSER = parser
        self.RMODE = mode
        super().__init__()

    def call_extractor(self):
        self.extractor = call_extractor(self.RMODE)

    def check_valid_url(self, url):
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        return self.PARSER in base_url

    def parse(self, url):

        assert self.check_valid_url(url), \
            "Invalid url for '{}' parser".format(self.PARSER)

        article = Article(url)
        soup = self.get_soup(url)
        try:
            cfg = self.cfg["site"][self.PARSER]
        except KeyError:
            raise NotImplementedError("Invalid parser")

        # URL
        article.url = url

        # title::text
        article.title = self.get_strs(soup, **cfg["title"])

        # authors::text
        article.authors = self.get_strs(soup, **cfg["authors"])

        # text::text
        article.text = self.get_strs(soup, **cfg["text"])

        # published_date::text
        article.published_date = self.get_strs(soup, **cfg["pubd"])

        # tags::text
        article.tags = self.get_strs(soup, **cfg["tags"])

        # image_urls::links
        article.image_urls = self.get_links(soup, **cfg["image_urls"])

        return article


class AutoCrawlParser(BaseParser):

    def __init__(self, mode="requests"):
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
