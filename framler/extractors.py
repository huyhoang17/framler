from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests

from ._base import BaseExtractor
from .log import get_logger

logger = get_logger(__name__)


class SeleniumExtractor(BaseExtractor):

    def __init__(self, timeout=180,
                 display_browser=False,
                 fast_load=False,
                 executable_path=None):

        self.profile = webdriver.FirefoxProfile()
        self.options = Options()
        self.options.add_argument("--headless")

        # Reference:
        # - https://github.com/hailoc12/docbao/blob/master/backend/lib/crawl.py
        # - https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions  # noqa
        if fast_load:
            self.profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            self.profile.set_preference('permissions.default.image', 2)
            # Disable notification
            self.profile.set_preference(
                'permissions.default.desktop-notification', 2)
            # Disable Flash
            self.profile.set_preference(
                'dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            # Adblock Extension
            self.profile.exp = "input/adblock.xpi"
            self.profile.add_extension(extension=self.profile.exp)

        # Add path to your Chromedriver
        if executable_path is None:
            self.driver = webdriver.Firefox(
                firefox_options=self.options, firefox_profile=self.profile
            )
        else:
            self.driver = webdriver.Firefox(
                firefox_options=self.options, firefox_profile=self.profile,
                executable_path=executable_path
            )

        self.driver.set_page_load_timeout(timeout)
        self.driver.implicitly_wait(timeout)
        self.is_quit = False

    def get_content(self, url):
        try:
            self.driver.get(url)
            return self.driver.page_source
        except Exception as e:
            logger.exception(e)

    def get_soup(self, url, mode="lxml"):
        try:
            soup = BeautifulSoup(self.get_content(url), mode)
            return soup
        except Exception as e:
            logger.exception(e)


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
