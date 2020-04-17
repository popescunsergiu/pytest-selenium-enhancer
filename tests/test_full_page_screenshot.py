# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
# pylint: disable=too-many-arguments

import functools
import operator
import os
from time import sleep

import pytest

from tests.utils.utils import compare_images


class TestFullPageScreenshot:
    base_score = 0.99

    common_args = ("path, name, elems_to_hide", [
        ("", "main_page",
         {"top": ["//header"],
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/getting-started/introduction/", "getting_started_introduction",
         {"top": ["//header"],
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/", "examples",
         {"top": ["//header"],
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/album/", "examples_album",
         {"top": None,
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/pricing/", "examples_pricing",
         {"top": None,
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/dashboard/", "examples_dashboard",
         {"top": ["//nav"],
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/sticky-footer/", "examples_sticky_footer",
         {"top": None,
          "all": None,
          "bottom": None
          }),
        ("/docs/4.4/examples/offcanvas/", "examples_offcanvas",
         {"top": ["//nav"],
          "all": None,
          "bottom": None
          }),
    ])

    @staticmethod
    def test_driver_is_enhanced(driver):
        from selenium.webdriver.remote.webdriver import WebDriver
        from selenium.webdriver.remote.webelement import WebElement

        assert hasattr(WebDriver, 'shadow_find_element'), 'Should have shadow_find_element'
        assert hasattr(WebElement, 'shadow_find_element'), 'Should have shadow_find_element'
        assert hasattr(WebDriver, 'shadow_cascade_find_element'), 'Should have shadow_cascade_find_element'
        assert hasattr(WebElement, 'shadow_cascade_find_element'), 'Should have shadow_cascade_find_element'
        assert hasattr(WebDriver, 'shadow_find_elements'), 'Should have shadow_find_elements'
        assert hasattr(WebElement, 'shadow_find_elements'), 'Should have shadow_find_elements'
        assert hasattr(WebDriver,
                       'get_full_page_screenshot_as_base64'), 'Should have get_full_page_screenshot_as_base64'

    @pytest.mark.parametrize(*common_args)
    def test_full_page_screenshot_as_png(self, pytestconfig, driver, base_url, path, name, elems_to_hide):
        env = self.__get_env(driver)

        driver.get('%s%s' % (base_url, path))
        sleep(2)

        actual_screenshot_url = '%s/tests/screenshots/actual/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)
        base_screenshot_url = '%s/tests/screenshots/base/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)
        diff_screenshot_url = '%s/tests/screenshots/diff/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)

        elems_to_hide = self.__elems_to_hide(driver, elems_to_hide)
        device_offset = driver.capabilities['deviceOffset'] if 'deviceOffset' in driver.capabilities else 0

        image_b = driver.get_full_page_screenshot_as_png(actual_screenshot_url, elems_to_hide, device_offset)

        assert compare_images(image_b, base_screenshot_url, actual_screenshot_url,
                              diff_screenshot_url, self.base_score) >= self.base_score, 'Should have image matching'

        os.remove(actual_screenshot_url)

    @pytest.mark.parametrize(*common_args)
    def test_full_page_screenshot_as_base64(self, pytestconfig, driver, base_url, path, name, elems_to_hide):
        env = self.__get_env(driver)

        actual_screenshot_url = '%s/tests/screenshots/actual/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)
        base_screenshot_url = '%s/tests/screenshots/base/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)
        diff_screenshot_url = '%s/tests/screenshots/diff/full_page_%s_%s.png' % (pytestconfig.rootdir, name, env)

        driver.get('%s%s' % (base_url, path))
        sleep(2)

        elems_to_hide = self.__elems_to_hide(driver, elems_to_hide)
        device_offset = driver.capabilities['deviceOffset'] if 'deviceOffset' in driver.capabilities else 0

        image_b = driver.get_full_page_screenshot_as_base64(elems_to_hide, device_offset)

        assert compare_images(image_b, base_screenshot_url, actual_screenshot_url,
                              diff_screenshot_url, self.base_score) >= self.base_score, 'Should have image matching'

    @staticmethod
    def __get_env(driver):
        if 'deviceModel' in driver.capabilities:
            env = driver.capabilities['deviceModel']
        elif 'deviceName' in driver.capabilities:
            env = driver.capabilities['deviceName']
        else:
            driver.set_window_size('1366', '768')
            env = driver.capabilities['browserName']
        return env

    @staticmethod
    def __elems_to_hide(driver, elements):
        start_elems = functools.reduce(operator.iconcat,
                                       [driver.find_elements_by_xpath(element) for element in elements['top']],
                                       []) if elements['top'] else None
        all_elems = functools.reduce(operator.iconcat,
                                     [driver.find_elements_by_xpath(element) for element in elements['all']],
                                     []) if elements['all'] else None
        end_elems = functools.reduce(operator.iconcat,
                                     [driver.find_elements_by_xpath(element) for element in elements['bottom']],
                                     []) if elements['bottom'] else None
        return {
            "top": start_elems,
            "all": all_elems,
            "bottom": end_elems
        }
