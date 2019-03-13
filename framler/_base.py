import os
import yaml
from multiprocessing import Pool, cpu_count
from time import time, sleep
import string
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from lxml import html
from selenium.common.exceptions import TimeoutException
import requests

from .cleaners import (
    remove_multiple_space,
    remove_html_tags,
    remove_all_html_tags,
    remove_links_content
)
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

    def get_netloc(self, url):
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        return base_url

    def get_roadmap(self, url):
        logger.info("Checking roadmaps...")
        roadmaps = [
            "sitemap",
            "sitemap.xml",
            "sitemap_index.xml",
            "rss.htm",
            "rss.html",
        ]
        for roadmap in roadmaps:
            url_roadmap = os.path.join(self.get_netloc(url), roadmap)
            req = requests.get(url)
            if req.ok:
                return url_roadmap

        return None

    def get_content(self, url):
        try:
            if self.RMODE == "selenium":
                self.driver.get(url)
                sleep(3)
                text = self.driver.page_source  # html
                # terminate driver
                self.quit()
                return text
            elif self.RMODE == "requests":
                req = requests.get(url)
                if not req.encoding.lower().startswith("utf"):
                    return req.content.decode("utf")  # html
                return req.text  # html
        except TimeoutException:
            return
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
            # remove script, stype text from js code
            soup = self.get_soup(url)
            soup = remove_html_tags(soup, get_text=False)
            tree = html.fromstring(str(soup))  # str(soup)::html
            return tree
        except Exception as e:
            logger.exception(e)


class BaseParser(object):

    def __init__(self):
        self.load_config()
        if self.RMODE == "selenium":
            self.check_driver()
        # self.call_extractor()

    def load_config(self, fpath="config.yaml"):
        self.BASE_CONFIG = os.path.join(
            os.path.dirname(__file__), fpath)

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
        try:
            return self.extractor.get_content(url)
        except AttributeError:
            self.call_extractor()
            return self.extractor.get_content(url)

    def count_objs(self, tree, xpath_seq):
        xpath_seq = "count({})".format(xpath_seq)
        count = tree.xpath(xpath_seq)
        return int(count)

    def get_trans(self,
                  ele,
                  from_=string.ascii_uppercase,
                  to_=string.ascii_lowercase,
                  fmt_trans="translate(@{}, '{}', '{}')"):
        return fmt_trans.format(ele, from_, to_)

    def get_contains(self,
                     attr,
                     val,
                     name="*",
                     get_text=False):
        fmt_xpath = "//{}[contains(translate(@{}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]"  # noqa
        if get_text:
            fmt_xpath += "//text()"

        return fmt_xpath.format(name, attr, val)

    def get_links_by_tag(self,
                         tree,
                         attrs,
                         vals,
                         src_attrs,
                         names=["*"],
                         fmt="//{}[contains(@{}, '{}')]//@{}"):
        """
        TODO:
            - filter links
        """
        matches = []
        for name in names:
            if name is None:
                name = "*"
            for attr in attrs:
                for val in vals:
                    for src_attr in src_attrs:
                        if src_attr is None:
                            continue
                        if attr is None and val is None:
                            xpath_seq = "//{}//@{}".format(name, src_attr)
                        elif None in (attr, val, src_attr):
                            continue
                        else:
                            xpath_seq = fmt.format(name, attr, val, src_attr)
                        res = tree.xpath(xpath_seq)
                        matches.extend(res)

        return list(set(matches))

    def filter_links(self, links):
        pass

    def get_element_by_tag(self,
                           tree,
                           attr,
                           val,
                           name,
                           get_text=True,
                           fmt="//{}[contains({}, '{}')]{}"):
        """
        "//*[@class='abc']"
        "//*[@class='abc']/text()"
        "//ABC[@class='abc']"
        "//ABC[@class='abc']/text()"

        old_fmt::"//{}[contains(@{}, '{}')]{}"

        TODO:
            - filter duplicate elements
            - title: select first element
            - text: filter duplicate content
        """
        if get_text:
            text = "//text()"
        else:
            text = ""

        if name != "*" and attr is None and val is None:
            xpath_seq = "//{}{}".format(name, text)
        elif name == "*" and None in (attr, val):
            return None
        elif None in (attr, val):
            return None
        else:
            attr = self.get_trans(attr)
            xpath_seq = fmt.format(name, attr, val, text)
        res = tree.xpath(xpath_seq)
        res = self.remove_empty_val(res)
        return res

    def clean_all(self, text):
        text = remove_all_html_tags(text)
        text = remove_links_content(text)
        return text

    def simplify(self, text):
        return remove_multiple_space(text).strip()

    def filter_content(self, sents, join=True):
        sents = [sent for sent in sents if self.simplify(sent)]

        result = []
        for sent in sents:
            if sent not in result:
                result.append(sent)

        if join:
            result = self.clean_all(self.simplify(" ".join(result)))

        return result

    def get_elements_by_tag(self,
                            tree,
                            attrs,
                            vals,
                            names=["*"],
                            get_text=True,
                            join=False):
        """
        name - attr - val
        A B C //text()
        * B C //text()
        A * * //text()
        """
        matches = []
        for name in names:
            if name is None:
                name = "*"
            for attr in attrs:
                for val in vals:
                    found = self.get_element_by_tag(
                        tree, attr=attr, val=val,
                        name=name, get_text=True
                    )
                    if found:
                        matches.extend(found)

        if join:
            return " ".join(matches)
        return matches

    def exclude_content(self,
                        tree,
                        attrs,
                        exc_vals):
        fmt_xpath = "//*[contains(translate(@{}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{}')]"  # noqa
        for attr in attrs:
            for exc_val in exc_vals:
                xpath_seq = self.get_contains(attr, exc_val)
                for bad in tree.xpath(xpath_seq):
                    bad.getparent().remove(bad)

        return tree

    def remove_empty_val(self, vals):
        return [val for val in vals if len(val.strip()) > 0]

    def check_datetime_fmt(self, dt):
        """
        TODO: check if string is in datetime format
        https://stackoverflow.com/a/16870699
        """
        pass

    def extract_nest_elements(self, elements):
        pass

    def extract_content_sub_elements(self, elements):
        pass

    def get_soup(self, url):
        return self.extractor.get_soup(url)

    def get_xpath_tree(self, url):
        return self.extractor.get_xpath_tree(url)

    def get_strs(self, soup, **kwargs):
        return remove_multiple_space(" ".join(
            [s.get_text() for s in soup.find_all(**kwargs)])
        ).strip()

    def get_links(self, soup, **kwargs):
        return [img.img["src"] for img in soup.find_all(**kwargs)]

    def run_processes(self, urls, no_cpus=None):
        result = []
        logger.info("Number of cpu: %s", cpu_count())

        start_time = time()
        no_cpus = no_cpus if no_cpus is not None else cpu_count() - 1

        p = Pool(no_cpus)
        try:
            result = p.map(self.parse, urls)
        except Exception as e:
            logger.exception(e)
        # for url in urls:
        #     result.append(p.apply_async(self.auto_parse, (url,)).get())

        p.close()
        p.join()
        end_time = time()

        elapsed_time = str(end_time - start_time)
        logger.info("Elapsed run time: %s seconds", elapsed_time)
        logger.info("Task ended. Pool join!")

        return result


class BaseExporter(object):

    def __init__(self):
        pass

    def export(self):
        pass
