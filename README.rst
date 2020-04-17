************************
pytest-selenium-enhancer
************************


pytest-selenium-enhancer is a plugin for pytest_ that provides enhanced webdriver functionality by dynamically
adding methods to:
- remote.webdriver.Webdriver
- remote.webdriver.WebElement

It provides a set of commands to enable testing of WebComponents_ and Visual Regression Testing

.. contents:: **Table of Contents**
    :depth: 4

Requirements
============

Following prerequisites are needed in order to use pytest-selenium-enhancer:

- numpy
- opencv-python >= 4.2.0.32
- pillow >= 7.0.0
- Python >= 3.7.5
- pytest >= 5.3.0
- pytest-variables >= 1.9.0
- requests
- selenium >= 3.141.0

Installation
============

To install pytest-selenium-enhancer:

.. code-block::

  pip install pytest-selenium-enhancer

Features and Usage
==================

Custom Commands
---------------

Adding custom commands
^^^^^^^^^^^^^^^^^^^^^^

Custom commands have to be added to the WebDriver and WebElement before they are used within the test project.
List of built-in fixtures:
.. code-block::

    selenium_patcher
        # Adds the predefined CustomCommands to WebDriver and WebElement

To extend the browser instance with own set of commands, the decorator *add_method* is here to help.
.. code-block::

    @pytest.fixture(scope='session')
    def my_custom_commands():
        @add_method(WebElement)
        def wait_and_click(self, timeout):
            """Waits for a given period of time then clicks the element
            """
            sleep(timeout)
            self.click()

To add the command to WebElement simply add the fixture as param to the browser function
Example of usage for the built-in fixture *selenium_patcher* and your defined fixture *my_custom_commands*:
.. code-block::

    @pytest.fixture(scope="function")
    def driver(variables, env_variables, selenium_patcher, my_custom_commands):
        from selenium import webdriver
        _driver = webdriver.Remote(
            command_executor='https://%s:%s@hub-cloud.browserstack.com/wd/hub'
                            % (env_variables.bs_username, env_variables.bs_key),
            desired_capabilities=variables['capabilities'])
        yield _driver
        _driver.close()

The plugin provides a set of custom commands to use for browser testing with pytest_

Build in remote.Webdriver Custom Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

shadow_find_element WebDriver
+++++++++++++++++++++++++++++

    Returns an element of a DOM subtree by given selector

    *Usage*
    .. code-block::

        browser.shadow_find_element(selector)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selector", "(obj:CSS Selector)", "CSS Selector as described here_"

    *Example*
    .. code-block::

        browser.shadow_find_element('custom-login-component')

shadow_cascade_find_element WebDriver
+++++++++++++++++++++++++++++++++++++

    Returns an element of a DOM subtree by given list of selectors

    *Usage*
    .. code-block::

        browser.shadow_cascade_find_element(selectors)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selectors", "(obj:CSS Selector), n (obj:CSS Selector)", "CSS Selectors as described here_"

    *Example*
    .. code-block::

        browser.shadow_cascade_find_element('custom-login-component', 'custom-login-form', 'custom-field')

shadow_find_elements WebDriver
++++++++++++++++++++++++++++++

    Returns a list of elements of a DOM subtree by given of selector

    *Usage*
    .. code-block::

        browser.shadow_find_elements(selector)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selectors", "(obj:CSS Selector)", "CSS Selectors as described here_"

    *Example*
    .. code-block::

        browser.shadow_cascade_find_element('custom-login-component')

get_full_page_screenshot_as_base64 WebDriver
++++++++++++++++++++++++++++++++++++++++++++

    Gets full page screenshot of current page by automatically scroll the full width and height of the page
        *NOTE:* Does not work for infinite scrolling pages

    *Usage*
    .. code-block::

        browser.get_full_page_screenshot_as_base64(elements_to_hide, device_offset)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "elements_to_hide", "(obj)", "{'top': [sticky top elements that you want to hide after first horizontal scroll], 'all':[elements that you want to completely hide], 'bottom': [sticky bottom elements that you want to show only after first horizontal scroll]}"
        "device_offset", "(int)", "iOS only. Used to define the height of the browser upper controls. Safari iOS browser controls are part of the screenshot taken by selenium so we want not to have them into a full page screenshot"

    *Example*
    .. code-block::

        elements_to_hide = {
            "start": [self.get_header()._banner] if self.page_name is 'home_page'] else [],
            "all": [],
            "end": [self.get_persistent_isi()._component_container]
        }
        browser.get_full_page_screenshot_as_base64(elements_to_hide, 284)

get_full_page_screenshot_as_png WebDriver
+++++++++++++++++++++++++++++++++++++++++

    Gets full page screenshot of current page by automatically scroll the full width and height of the page
        *NOTE:* Does not work for infinite scrolling pages

    *Usage*
    .. code-block::

        browser.get_full_page_screenshot_as_png(image_path, elements_to_hide, device_offset)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "image_path", "(str)", "Full path of the location to where to save the screenshot"
        "elements_to_hide", "(obj)", "{'top': [sticky top elements that you want to hide after first horizontal scroll], 'all':[elements that you want to completely hide], 'bottom': [sticky bottom elements that you want to show only after first horizontal scroll]}"
        "device_offset", "(int)", "iOS only. Used to define the height of the browser upper controls. Safari iOS browser controls are part of the screenshot taken by selenium so we want not to have them into a full page screenshot"

    *Example*
    .. code-block::

        elements_to_hide = {
            "start": [self.get_header()._banner] if self.page_name is 'home_page'] else [],
            "all": [],
            "end": [self.get_persistent_isi()._component_container]
        }
        browser.get_full_page_screenshot_as_png(image_path, elements_to_hide, 284)

Build in remote.WebElement Custom Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

shadow_find_element WebElement
++++++++++++++++++++++++++++++

    Returns a child element of a DOM subtree by given selector

    *Usage*
    .. code-block::

        element.shadow_find_element(selector)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selector", "(obj:CSS Selector)", "CSS Selector as described here_"

    *Example*
    .. code-block::

        custom_login_component = browser.find_element_by_tag_name('custom-login-component')
        custom_login_component.shadow_find_element('custom-login-component')

shadow_cascade_find_element WebElement
++++++++++++++++++++++++++++++++++++++

    Returns a child element of a DOM subtree by given list of selectors

    *Usage*
    .. code-block::

        element.shadow_cascade_find_element(selectors)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selectors", "(obj:CSS Selector), n (obj:CSS Selector)", "CSS Selectors as described here_"

    *Example*
    .. code-block::

        custom_login_component = browser.find_element_by_tag_name('custom-login-component')
        custom_login_component.shadow_cascade_find_element('custom-login-component', 'custom-login-form', 'custom-field')

shadow_find_elements WebElement
+++++++++++++++++++++++++++++++

    Returns a list of children elements of a DOM subtree by given of selector

    *Usage*
    .. code-block::

        element.shadow_find_elements(selector)

    *Parameters*
    .. csv-table::

        :header: "Name", "Type", "Details"
        :widths: 20, 30, 50

        "selectors", "(obj:CSS Selector)", "CSS Selectors as described here_"

    *Example*
    .. code-block::

        custom_login_component = browser.find_element_by_tag_name('custom-login-component')
        custom_login_component.shadow_cascade_find_element('custom-login-component')

If you want to know more about WebComponents_ and ShadowRoot_


**NOTE:** For the above examples, the following piece of HTML, as seen in `Developer Tools`_, was considered:
.. code-block::

    <custom-login-component>
        #shadowRoot (open)
        <custom-login-form>
            #shadowRoot (open)
            <custom-field type="text">
                #shadowRoot (open)
                <input></input>
            </custom-field>
            <custom-field type="password">
                #shadowRoot (open)
                <input></input>
            </custom-field>
            <custom-button>Login
                #shadowRoot (open)
                <button></button>
            </custom-button>
        </custom-login-form>
    </custom-login-component>

Custom Waits
------------

wait_for_element_present
^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_element_visible
^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_element_not_visible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_element_clickable
^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_child_element_visible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_child_element_not_visible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_the_attribute_value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_for_the_attribute_contain_value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TODO

wait_until
^^^^^^^^^^
TODO

Contributing
============

We welcome contributions.

To learn more, see Contributing_

E2E testing is brought to you by BrowserStack_.

.. image:: https://github.com/popescunsergiu/pytest-selenium-enhancer/raw/master/.github/BrowserStack-logo.png
    :alt: BrowserStack
    :target: https://browserstack.com

Resources
=========

- `Release Notes`_
- `Issue Tracker`_
- Code_

.. _pytest: http://pytest.org

.. _WebComponents: https://developer.mozilla.org/en-US/docs/Web/Web_Components

.. _here: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors

.. _ShadowRoot: https://developer.mozilla.org/en-US/docs/Web/API/ShadowRoot
.. _Developer Tools: https://developers.google.com/web/tools/chrome-devtools

.. _Contributing: https://github.com/pytest-dev/pytest-selenium-enhancer/blob/master/.github/CONTRIBUTING.rst
.. _BrowserStack: https://browserstack.com

.. _Release Notes:  https://github.com/popescunsergiu/pytest-selenium-enhancer/blob/master/CHANGES.rst
.. _Issue Tracker: https://github.com/popescunsergiu/pytest-selenium-enhancer/issues
.. _Code: https://github.com/popescunsergiu/pytest-selenium-enhancer
