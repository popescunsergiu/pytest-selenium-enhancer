# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
# pylint: disable=too-many-arguments
import time

import pytest
from pytest_selenium_enhancer import CustomWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class TestCustomWaitConditions:

    def test_wait_for_element_present(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        wait.wait_for_element_present(value='//h1[.="Examples"]', timeout=1)
        try:
            wait.wait_for_element_present(value='//h1[.="Examples dummy"]', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_element_visible(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        wait.wait_for_element_visible(value='//h1[.="Examples"]', timeout=1)
        try:
            wait.wait_for_element_visible(value='//h1[.="Examples dummy"]', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_element_clickable(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        wait.wait_for_element_clickable(value='//a[contains(@href,"https://github.com/twbs/bootstrap/archive/v4")]'
                                        , timeout=1)
        try:
            wait.wait_for_element_clickable(value='//a[contains(@href,"https://github.com/twbs/bootstrap/archive/v4")]'
                                            , timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_element_not_visible(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        wait.wait_for_element_not_visible(value='//h1[.="Examples dummy"]', timeout=1)
        try:
            wait.wait_for_element_visible(value='//h1[.="Examples"]', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_the_attribute_value(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        title = driver.find_element(By.XPATH, '//h1[.="Examples"]')

        wait.wait_for_the_attribute_value(title, 'class', 'bd-title mt-0', timeout=1)
        try:
            wait.wait_for_the_attribute_value(title, 'class', 'bd-title', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_the_attribute_contain_value(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        title = driver.find_element(By.XPATH, '//h1[.="Examples"]')

        wait.wait_for_the_attribute_contain_value(title, 'class', 'bd-title', timeout=1)
        try:
            wait.wait_for_the_attribute_contain_value(title, 'class', 'bs-title', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_child_element_visible(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        elem = driver.find_element(By.XPATH, '//main')

        wait.wait_for_child_element_visible(elem, value='./h2[@id="custom-components"]', timeout=1)
        try:
            wait.wait_for_child_element_visible(elem, value='./h3[id="custom-components"]', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e

    def test_wait_for_child_element_not_visible(self, driver, base_url):
        driver.get('%s%s' % (base_url, '/docs/4.4/examples/'))
        wait = CustomWait(driver)

        elem = driver.find_element(By.XPATH, '//main')

        wait.wait_for_child_element_not_visible(elem, value='./h3[@id="custom-components"]', timeout=1)
        try:
            wait.wait_for_child_element_not_visible(elem, value='./h2[id="custom-components"]', timeout=1)
        except TimeoutException as e:
            print(e)
        except Exception as e:
            raise e
