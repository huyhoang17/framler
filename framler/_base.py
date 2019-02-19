from abc import ABC, abstractmethod
import os
import yaml

from .cleaners import remove_multiple_space
from .utils import download_driver


class BaseExtractor(ABC):

    @abstractmethod
    def get_content(self):
        pass


class BaseParser(object):

    def __init__(self):
        self.load_config()
        self.call_extractor(self.mode, self.BASE_DRIVER)
        self.check_driver()

    def load_config(self):
        self.BASE_CONFIG = os.path.join(
            os.path.dirname(__file__), "config.yaml")

        with open(self.BASE_CONFIG) as f:
            self.cfg = yaml.load(f)

        self.BASE_DRIVER = os.path.join(
            os.path.expanduser('~'),
            self.cfg["driver"]["untar_folder"],
            self.cfg["driver"]["untar_fname"]
        )

    def check_driver(self):
        if not os.path.exists(self.BASE_DRIVER):
            download_driver()

    def get_config(self):
        return self.cfg["site"][self.PARSER]

    def get_content(self, url):
        return self.extractor.get_content(url)

    def get_soup(self, url):
        return self.extractor.get_soup(url)

    def get_strs(self, **kwargs):
        return remove_multiple_space(' '.join(
            [s.get_text() for s in self.soup.find_all(**kwargs)])
        ).strip()

    def call_extractor(self, mode, executable_path):
        pass

    def parse(self, url, mode="selenium"):

        # URL
        self.article.url = url

        # title
        self.article.title = self.get_strs(**self.cfg["title"])

        # author
        self.article.author = self.get_strs(**self.cfg["author"])

        # text (content)
        self.article.text = self.get_strs(**self.cfg["text"])

        # published_date
        self.article.published_date = self.get_strs(**self.cfg["pubd"])

        # tags
        self.article.tags = self.get_strs(**self.cfg["tags"])

        # image_urls
        self.article.image_urls = self.get_strs(**self.cfg["image_urls"])

        # top image
        self.article.top_image_url = \
            self.get_strs(**self.cfg["top_image_url"])
