# pylint: disable=global-statement
# pylint: disable=import-outside-toplevel
# pylint: disable=invalid-name
# pylint: disable=protected-access

"""Configuration for pytest runner."""
import pytest

from tests.utils.env_variables import EnvVariables

pytest_plugins = ["pytester"]
bs_local = None


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", help="Base URL")


@pytest.fixture(scope="function")
def driver(variables, env_variables, selenium_patcher):
    from selenium import webdriver
    _driver = webdriver.Remote(
        command_executor='https://%s:%s@hub-cloud.browserstack.com/wd/hub'
                         % (env_variables.bs_username, env_variables.bs_key),
        desired_capabilities=variables['capabilities'])
    yield _driver
    _driver.close()


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope='session')
def env_variables(pytestconfig):
    env_vars_file_path = "%s/tests/.local.env" % pytestconfig.rootdir
    return EnvVariables(env_vars_file_path)
