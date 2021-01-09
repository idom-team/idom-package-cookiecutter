import pytest
from idom.testing import (
    create_simple_selenium_web_driver,
    ServerMountPoint,
)
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--headless",
        dest="headless",
        action="store_true",
        help="Whether to run browser tests in headless mode.",
    )


@pytest.fixture
def display(driver, server_mount_point):
    with server_mount_point.open_mount_function() as mount:
        def display(element_constructor):
            mount(element_constructor)
            driver.get(server_mount_point.url())
        yield display


@pytest.fixture(scope="session")
def server_mount_point():
    mount_point = ServerMountPoint()
    yield mount_point
    mount_point.server.quit()


@pytest.fixture
def driver_wait_until(driver) -> WebDriverWait:
    """A :class:`WebDriverWait` object for the current web driver"""

    def wait_until(function):
        WebDriverWait(driver, 3).until(lambda driver: function())

    return wait_until


@pytest.fixture(scope="session")
def driver(driver_is_headless):
    options = ChromeOptions()
    options.headless = driver_is_headless
    driver = create_simple_selenium_web_driver(driver_options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def driver_is_headless(pytestconfig):
    return bool(pytestconfig.option.headless)
