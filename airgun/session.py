import logging
import os

from datetime import datetime

from airgun.browser import browser
from widgetastic.browser import Browser

from airgun.entities.login import Login

from airgun.settings import Settings


LOGGER = logging.getLogger(__name__)


class Session(object):
    """A session context manager that manages login and logout"""

    def __init__(self, test, user=None, password=None):
        self.test = test
        self._user = user or Settings.admin_username
        self._password = password or Settings.admin_password

    def __enter__(self):
        self.browser = Browser(browser())

        self.browser.url = 'https://' + Settings.hostname

        # Library methods
        self.login = Login(self.browser)

        self.login.login({'username': self._user, 'password': self._password})
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                self.login.logout()
            else:
                self.take_screenshot()
        except Exception as err:
            LOGGER.exception(err)
        finally:
            self.browser.selenium.quit()

    def take_screenshot(self):
        """Take screen shot from the current browser window.

        The screenshot named ``screenshot-YYYY-mm-dd_HH_MM_SS.png`` will be
        placed on the path specified by
        ``settings.screenshots_path/YYYY-mm-dd/ClassName/method_name/``.

        All directories will be created if they don't exist. Make sure that the
        user running robottelo have the right permissions to create files and
        directories matching the complete.
        """
        # fixme: not tested
        # Take a screenshot if any exception is raised and the test method is
        # not in the skipped tests.
        now = datetime.now()
        path = os.path.join(
            Settings.screenshots_path,
            now.strftime('%Y-%m-%d'),
        )
        if not os.path.exists(path):
            os.makedirs(path)
        filename = '{0}-screenshot-{1}.png'.format(
            self.test.replace(' ', '_'),
            now.strftime('%Y-%m-%d_%H_%M_%S')
        )
        path = os.path.join(path, filename)
        LOGGER.debug('Saving screenshot %s', path)
        self.browser.selenium.save_screenshot(path)
