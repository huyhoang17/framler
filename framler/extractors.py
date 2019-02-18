from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from ._base import BaseExtractor
from .log import get_logger

logger = get_logger(__name__)


class SeleniumExtractor(BaseExtractor):

    def __init__(self, url, executable_path=None):
        super().__init__()
        # Add path to your Chromedriver
        if executable_path is None:
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox(executable_path=executable_path)

        self.url = url

    def get_content(self, iwait=30):
        try:
            self.driver.implicitly_wait(iwait)
            self.browser.get(self.url)
            return self.browser.page_source
        except Exception as e:
            logger.exception(e)

    def get_soup(self, mode='lxml'):
        try:
            soup = BeautifulSoup(self.get_page(), mode)
        except Exception as e:
            logger.exception(e)
        return soup


class RequestsExtractor(BaseExtractor):

    def __init__(self):
        pass

    def get_content(self, url):
        req = requests.get(url)
        return req.text

    def get_soup(self, url, mode='lxml'):
        try:
            soup = BeautifulSoup(self.get_content(url), mode)
        except Exception as e:
            logger.exception(e)
        return soup
