import os
import yaml
from multiprocessing import Pool, cpu_count
from time import time

from bs4 import BeautifulSoup
from lxml import html
import requests

from .cleaners import remove_multiple_space
from .utils import download_driver
from .log import get_logger

logger = get_logger(__name__)


class BaseExtractor(object):
    """
    :param pmode: parsing mode (lxml or html.parser or ....)
    """
    PMODE = "lxml"

    def __init__(self):
        pass

    def set_browser(self, browser):
        """
        :param browser: firefox, chrome; defaut to firefox
        """
        self.BROWSER = browser

    def set_rmode(self, rmode):
        self.RMODE = rmode

    def set_pmode(self, pmode):
        self.PMODE = pmode

    def get_content(self, url):
        logger.info(url)
        try:
            if self.RMODE == "selenium":
                self.driver.get(url)
                return self.driver.page_source
            elif self.RMODE == "requests":
                req = requests.get(url)
                return req.text
        except Exception as e:
            logger.exception(e)

    def get_soup(self, url):
        try:
            soup = BeautifulSoup(self.get_content(url), self.PMODE)
            return soup
        except Exception as e:
            logger.exception(e)

    def get_xpath_tree(self, url):
        try:
            tree = html.fromstring(self.get_content(url))
            return tree
        except Exception as e:
            logger.exception(e)

    def retry_connection(self, url, retry=3, timeout=30):
        pass

    def run_process(self, url):
        if self.retry_connection(url):
            html = self.get_content(url)
            output_list = self.parse(url, html)
            self.write_to_file(output_list)
        else:
            logger.warning("Can not fetch data from: %s", url)

    def run_processes(self, samples):
        logger.info("Number of cpu: %s", cpu_count())

        start_time = time()
        p = Pool(cpu_count() - 1)
        p.map(self.get_content, samples)
        p.close()
        p.join()
        end_time = time()

        elapsed_time = str(end_time - start_time)
        logger.info("Elapsed run time: %s seconds", elapsed_time)


class BaseParser(object):

    def __init__(self):
        self.load_config()
        if self.RMODE == "selenium":
            self.check_driver()
        self.call_extractor()

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
            logger.info("Downloading firefox selenium driver ....")
            download_driver()

    def call_extractor(self):
        pass

    def get_content(self, url):
        return self.extractor.get_content(url)

    def get_links_by_tag(self,
                         tree,
                         attr,
                         val,
                         src_attrs,
                         name="*",
                         fmt="//{}[@{}='{}']/@{}"):
        matches = []
        for src_attr in src_attrs:
            xpath_seq = fmt.format(name, attr, val, src_attr)
            res = tree.xpath(xpath_seq)
            matches.extend(res)
        return matches

    def get_element_by_tag(self,
                           tree,
                           name,
                           attr,
                           val,
                           get_text=True,
                           fmt="//{}[@{}='{}']{}"):
        if get_text:
            text = "/text()"
        xpath_seq = fmt.format(name, attr, val, text)
        res = tree.xpath(xpath_seq)
        return res

    def get_elements_by_tag(self,
                            tree,
                            attrs,
                            vals,
                            names=["*"],
                            get_text=True,
                            all_=True):
        matches = []
        if all_:
            names = "*"
        for name in names:
            for attr in attrs:
                for val in vals:
                    found = self.get_element_by_tag(
                        tree, name, attr=attr,
                        val=val, get_text=True
                    )
                    matches.extend(found)

        return matches

    def exclude_content(self, elements):
        pass

    def extract_nest_elements(self, elements):
        pass

    def extract_content_sub_elements(self, elements):
        pass

    def get_soup(self, url):
        return self.extractor.get_soup(url)

    def get_xpath_tree(self, url):
        return self.extractor.get_xpath_tree(url)

    def get_strs(self, **kwargs):
        return remove_multiple_space(' '.join(
            [s.get_text() for s in self.soup.find_all(**kwargs)])
        ).strip()

    def get_links(self, **kwargs):
        return [img.img["src"] for img in self.soup.find_all(**kwargs)]

    def parse(self, url):

        cfg = self.cfg["site"][self.PARSER]

        # URL
        self.article.url = url

        # title::text
        self.article.title = self.get_strs(**cfg["title"])

        # author::text
        self.article.authors = self.get_strs(**cfg["authors"])

        # text::text
        self.article.text = self.get_strs(**cfg["text"])

        # published_date::text
        self.article.published_date = self.get_strs(**cfg["pubd"])

        # tags::text
        self.article.tags = self.get_strs(**cfg["tags"])

        # image_urls::links
        self.article.image_urls = self.get_links(**cfg["image_urls"])


class BaseExporter(object):

    def __init__(self):
        pass

    def export(self):
        pass
