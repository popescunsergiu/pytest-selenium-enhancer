import time
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import pytest_selenium_enhancer.custom_expected_conditions as CEC


class CustomWait:
    def __init__(self, driver):
        self.driver = driver
        self.implicit_wait = driver.capabilities['timeouts']['implicit'] if 'timeouts' in driver.capabilities and \
            'implicit' in driver.capabilities['timeouts'] and driver.capabilities['timeouts']['implicit'] != 0 \
            else 30

    def wait_for_element_present(self, by=By.XPATH, value=None, text=None, timeout=10):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_element_visible(self, by=By.XPATH, value=None, text=None, timeout=10):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))

    def wait_for_element_not_visible(self, by=By.XPATH, value=None, text=None, timeout=5):
        sleep(2)
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, timeout)
        self.driver.implicitly_wait(timeout)
        result = wait.until(EC.invisibility_of_element_located((by, value)))
        # pylint: disable=no-member
        self.driver.implicitly_wait(self.implicit_wait)
        return result

    def wait_for_element_clickable(self, by=By.XPATH, value=None, text=None, timeout=10):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def wait_for_child_element_visible(self, parent_element, by=By.XPATH, value=None, text=None, timeout=10):
        if text is not None:
            value = value % text
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(CEC.visibility_of_child_element_located(parent_element, (by, value)))

    def wait_for_child_element_not_visible(self, parent_element, by=By.XPATH, value=None, text=None, timeout=5):
        if text is not None:
            value = value % text

        wait = WebDriverWait(self.driver, timeout)
        self.driver.implicitly_wait(timeout)
        result = wait.until(CEC.invisibility_of_child_element_located(parent_element, (by, value)))
        # pylint: disable=no-member
        self.driver.implicitly_wait(self.implicit_wait)
        return result

    def wait_for_the_attribute_value(self, element, attribute, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(CEC.wait_for_the_attribute_value(element, attribute, value))

    def wait_for_the_attribute_contain_value(self, element, attribute, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(CEC.wait_for_the_attribute_contain_value(element, attribute, value))

    @staticmethod
    def wait_until(some_predicate, timeout=20, period=0.25, description=""):
        must_end = time.time() + timeout
        while time.time() < must_end:
            if some_predicate():
                return True
            time.sleep(period)
        assert some_predicate() is True, description

    # pylint: disable=no-member
    @staticmethod
    def static_wait(period=1):
        sleep(period)
