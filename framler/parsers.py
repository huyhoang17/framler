from collections import Counter
from copy import deepcopy
import os
import yaml
from urllib.parse import urlsplit

import datefinder

from ._base import BaseParser
from .articles import Article
from .cleaners import (
    remove_multiple_space,
    remove_punctuation
)
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
        if soup is None:
            return

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

    # START::main method
    def get_title(self, title):
        return title

    def get_text(self, text):
        return text

    def get_authors(self, authors):
        if authors:
            return [authors[0].strip()]
        return []

    def get_pubd(self, seqs):
        result = []
        for seq in seqs:
            matches = datefinder.find_dates(seq)
            result.extend(list(matches))

        if result:
            result = str(Counter(result).most_common(1)[0][0]).split()[0]
        else:
            result = ""
        return result

    def get_tags(self, tags):
        results = []
        for tag in tags:
            tag = tag.lower()
            tag = remove_multiple_space(tag)
            tag = remove_punctuation(tag)
            tag = tag.strip()
            if tag and tag not in results:
                results.append(tag)

        return results

    def get_image_urls(self, image_urls):
        return image_urls
    # END::main method

    def parse_tag(self, tree, filter_, **kwargs):
        """
        :param filter_: True if return string, False if return list elements
        """
        # arc_attrs::to get links, not text
        src_attrs = kwargs.get("src_attrs", None)

        attrs = kwargs.get("attrs", None)
        vals = kwargs.get("vals", None)
        name = kwargs.get("name", None)
        exc_vals = kwargs.get("exc_vals", None)

        if exc_vals is not None:
            temp_tree = deepcopy(tree)
            self.temp_tree = self.exclude_content(temp_tree, attrs, exc_vals)
            result = self.get_elements_by_tag(
                temp_tree, attrs, vals, name
            )
            del temp_tree
        else:
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

    def parse(self, url):

        cfg = self.auto_cfg
        self.call_extractor()
        tree = self.get_xpath_tree(url)
        article = Article(url)

        # URL
        article.url = url

        # title::text
        article.title = self.get_title(
            self.parse_tag(tree, True, **cfg["title"])
        )

        # authors::text
        article.authors = self.get_authors(
            self.parse_tag(tree, False, **cfg["authors"])
        )

        # text::text
        article.text = self.get_text(
            self.parse_tag(tree, True, **cfg["text"])
        )

        # published_date::text
        article.published_date = self.get_pubd(
            self.parse_tag(tree, False, **cfg["pubd"])
        )

        # tags::text
        article.tags = self.get_tags(
            self.parse_tag(tree, False, **cfg["tags"])
        )

        # image_urls::links
        article.image_urls = self.get_image_urls(
            self.parse_tag(self.temp_tree, False, **cfg["image_urls"])
        )
        return article
