import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ._base import BaseExtractor
from .log import get_logger
from .utils import load_config

logger = get_logger(__name__)


class SeleniumExtractor(BaseExtractor):
    """
    :param RMODE: request mode (selenium or requests)
    :param BROWSER: firefox, chrome; defaut to firefox
    """
    BROWSER = "firefox"  # default
    RMODE = "selenium"

    def __init__(self, timeout=300,
                 display_browser=False,
                 fast_load=False,
                 executable_path=None):

        self.cfg = load_config()["driver"]
        self.timeout = timeout
        self.display_browser = display_browser
        self.fast_load = fast_load
        self.executable_path = executable_path

        self.profile = webdriver.FirefoxProfile()
        self.options = Options()
        self.options.add_argument("--headless")

        # Reference:
        # - https://github.com/hailoc12/docbao/blob/master/backend/lib/crawl.py
        # - https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions  # noqa
        if self.fast_load:
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

        # Add path to your FirefoxDriver
        if self.executable_path is None:
            self.executable_path = os.path.join(
                os.path.expanduser('~'),
                self.cfg["untar_folder"],
                self.cfg["untar_fname"]
            )
        logger.info("Executable path: %s", self.executable_path)
        self.driver = webdriver.Firefox(
            options=self.options, firefox_profile=self.profile,
            executable_path=self.executable_path
        )

        self.driver.set_page_load_timeout(self.timeout)
        self.driver.implicitly_wait(self.timeout)

    def quit(self):
        """
        Terminate driver selenium
        """
        self.driver.quit()


class RequestsExtractor(BaseExtractor):
    """
    :param RMODE: request mode (selenium or requests)
    """
    RMODE = "requests"
