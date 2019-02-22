from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ._base import BaseExtractor
from .log import get_logger

logger = get_logger(__name__)


class SeleniumExtractor(BaseExtractor):
    """
    :param RMODE: request mode (selenium or requests)
    :param BROWSER: firefox, chrome; defaut to firefox
    """
    BROWSER = "firefox"  # default
    RMODE = "selenium"

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
                options=self.options, firefox_profile=self.profile
            )
        else:
            self.driver = webdriver.Firefox(
                options=self.options, firefox_profile=self.profile,
                executable_path=executable_path
            )

        self.driver.set_page_load_timeout(timeout)
        self.driver.implicitly_wait(timeout)

    def retry_connection(self,
                         url,
                         retry=3,
                         timeout=30):
        connection_attempts = 0
        while connection_attempts < retry:
            try:
                self.driver.get(url)
                self.driver.implicitly_wait(timeout)
                return True
            except Exception as e:
                logger.exception(e)
                logger.error("Error connecting to %s", url)
                logger.error("Attempt #%s.", connection_attempts)
                connection_attempts += 1
        return False


class RequestsExtractor(BaseExtractor):
    """
    :param RMODE: request mode (selenium or requests)
    """
    RMODE = "requests"
