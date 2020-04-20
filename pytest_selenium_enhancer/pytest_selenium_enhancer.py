# pylint: disable=function-redefined
# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
# pylint: disable=too-many-statements
# pylint: disable=unused-variable

import base64
from io import BytesIO
import cv2
import numpy
from PIL import Image
from selenium.common.exceptions import WebDriverException


def add_custom_commands():
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

    @add_method(WebDriver)
    def get_full_page_screenshot_as_base64(self, elements_to_hide=None, ios_offset=0):
        """Gets full page screenshot of current page by automatically scroll the full width and height of the page
                NOTE:
                    - Does not work for infinite scrolling pages

            Returns:
            PIL.Image.Image: returns the image as Image object

        """
        stitched_image = __take_full_page_screenshot(self, elements_to_hide, ios_offset)
        return cv2.cvtColor(numpy.array(stitched_image), cv2.COLOR_RGB2BGR)

    @add_method(WebDriver)
    def get_full_page_screenshot_as_png(self, image_path, elements_to_hide=None, ios_offset=0):
        """Gets full page screenshot of current page by automatically scroll the full width and height of the page
                NOTE:
                    - Does not work for infinite scrolling pages

            Returns:
            PIL.Image.Image: returns the image as Image object

        """
        stitched_image = __take_full_page_screenshot(self, elements_to_hide, ios_offset)
        from os import makedirs
        makedirs(image_path[:image_path.rfind('/')], exist_ok=True)
        stitched_image.save(image_path)
        return cv2.imread(image_path)

    @add_method(WebDriver)
    def shadow_find_element(self, css_selector):
        """Returns an element by given CSS selector

            Returns:
            WebElement: returns the element as WebElement
        """
        return self.execute_script('return document.shadowRoot.querySelector(arguments[0])', css_selector)

    @add_method(WebDriver)
    def shadow_cascade_find_element(self, *args):
        """Returns an element by given list of CSS selectors

            Returns:
            WebElement: returns the element as WebElement
        """
        script = 'return document'
        for arg in args:
            script += '.querySelector("%s").shadowRoot' % arg
        script = script[:-11] + ';'
        return self.execute_script(script)

    @add_method(WebDriver)
    def shadow_find_elements(self, css_selector):
        """Returns a list of elements by given of CSS selector

            Returns:
            list<WebElement>: returns the element as WebElement
        """
        return self.execute_script('return document.shadowRoot.querySelectorAll(arguments[0])', css_selector)

    @add_method(WebElement)
    def shadow_find_element(self, css_selector):
        """Returns an element by given CSS selector

            Returns:
            WebElement: returns the element as WebElement
        """
        return self.parent.execute_script('return arguments[0].shadowRoot.querySelector(arguments[1])', self,
                                          css_selector)

    @add_method(WebElement)
    def shadow_cascade_find_element(self, *args):
        """Returns an element by given list of CSS selectors

            Returns:
            WebElement: returns the element as WebElement
        """
        script = 'return %s' % self
        for arg in args:
            script += '.shadowRoot.querySelector("%s")' % arg
        return self.parent.execute_script(script)

    @add_method(WebElement)
    def shadow_find_elements(self, css_selector):
        """Returns a list of elements by given of CSS selector

            Returns:
            list<WebElement>: returns the element as WebElement
        """
        return self.parent.execute_script('return arguments[0].shadowRoot.querySelectorAll(arguments[1])', self,
                                          css_selector)

    def __take_full_page_screenshot(selenium, elements_to_hide, ios_offset=0):
        if elements_to_hide is None:
            elements_to_hide = {"start": [], "all": [], "end": []}
        device_pixel_ratio = selenium.execute_script('return ratio = window.devicePixelRatio || 1;')
        total_width = round(
            selenium.execute_script("return document.body.scrollWidth * arguments[0];", device_pixel_ratio))
        total_height = round(
            selenium.execute_script("return document.body.scrollHeight * arguments[0];", device_pixel_ratio))
        viewport_width = round(
            selenium.execute_script("return document.body.parentNode.clientWidth * arguments[0];", device_pixel_ratio))
        viewport_height = round(
            selenium.execute_script("return document.body.parentNode.clientHeight * arguments[0];", device_pixel_ratio))

        rectangles = []
        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height
            if top_height > total_height:
                top_height = total_height
            while ii < total_width:
                top_width = ii + viewport_width
                if top_width > total_width:
                    top_width = total_width
                rectangles.append((ii, i, top_width, top_height))
                ii = ii + viewport_width
            i = i + viewport_height - ios_offset
        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        i = 1

        __hide_elements(selenium, elements_to_hide['all'])
        for rectangle in rectangles:
            if i == 1 != rectangles.__len__():
                __hide_elements(selenium, elements_to_hide['end'])
            if rectangle[1] != 0:
                __hide_elements(selenium, elements_to_hide['start'])
            if i == rectangles.__len__():
                __show_elements(selenium, elements_to_hide['end'])
            if previous is not None:
                selenium.execute_script("window.scrollTo({0}, {1})".format(round(rectangle[0] / device_pixel_ratio),
                                                                           round(rectangle[1] / device_pixel_ratio)))
                import time
                time.sleep(3)
            offset = (rectangle[0], rectangle[1])

            image_base_64 = selenium.get_screenshot_as_base64()
            screenshot = Image.open(BytesIO(base64.b64decode(image_base_64)))
            screenshot = screenshot.crop((0, ios_offset, screenshot.size[0], screenshot.size[1]))
            if viewport_width < total_width < rectangle[0] + viewport_width \
                    and viewport_height < total_height < rectangle[1] + viewport_height:
                offset = (total_width - viewport_width, total_height - viewport_height)
            elif viewport_width < total_width < rectangle[0] + viewport_width:
                offset = (total_width - viewport_width, rectangle[1])
            elif viewport_height < total_height < rectangle[1] + viewport_height:
                offset = (rectangle[0], total_height - viewport_height)
            # screenshot.save('/Users/spopescu/PersonalDev/pytest-selenium-enhancer/tests/screenshots/actual/a.png')
            # stitched_image.save('/Users/spopescu/PersonalDev/pytest-selenium-enhancer/tests/screenshots/actual/b.png')
            stitched_image.paste(screenshot, offset)
            del screenshot
            previous = rectangle
            i += 1

        return stitched_image

    def __show_elements(selenium, elements):
        """
        Usage:
            Hide elements from web page
        Args:
            selenium(str) : WebDriver / Appium instance
            elements (list) : The element on web page to be hide
        Returns:
            N/A
        Raises:
            N/A
        """
        if elements is not None:
            try:
                for element in elements:
                    selenium.execute_script("arguments[0].setAttribute('style', 'opacity:1;');", element)
            except WebDriverException as error:
                print('Error : ', str(error))

    def __hide_elements(selenium, elements):
        """
        Usage:
            Hide elements from web page
        Args:
            selenium(str) : WebDriver / Appium instance
            elements (list) : The element on web page to be hide
        Returns:
            N/A
        Raises:
            N/A
        """
        if elements is not None:
            try:
                for element in elements:
                    selenium.execute_script("arguments[0].setAttribute('style', 'opacity:0;');", element)
            except WebDriverException as error:
                print('Error : ', str(error))


def add_method(cls):
    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator
