# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
# pylint: disable=too-many-arguments
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from custom_wait import CustomWait


@pytest.fixture(scope='session')
def my_custom_commands():
    from selenium.webdriver.remote.webelement import WebElement
    from pytest_selenium_enhancer import add_method

    @add_method(WebElement)
    def wait_and_click(self, timeout):
        """Waits for a given period of time then clicks the element
        """
        time.sleep(timeout)
        self.click()


class TestCustomExpectedConditions:

    def test_add_and_use_custom_command(self, driver, base_url, my_custom_commands):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))

        button = driver.find_element(By.XPATH, '//a[@href="/"]')
        button.wait_and_click(5)
        assert driver.current_url == 'https://getbootstrap.com/'
