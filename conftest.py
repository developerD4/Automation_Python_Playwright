import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from config.config import BASE_URL, LOGIN_USERNAME, LOGIN_PASSWORD
from pages.add_form import AddForm

@pytest.fixture(scope="session")
def browser_context():
    """
    Launch browser once per test session with specific flags to support
    crypto operations on the trailing-dot domain.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-default-browser-check',
                '--ignore-certificate-errors',
                '--allow-running-insecure-content',
                # Enable new crypto algorithms like X25519
                '--enable-experimental-web-platform-features',
                '--unsafely-treat-insecure-origin-as-secure=https://staging.onlygood.world.,https://staging.onlygood.world',
            ]
        )
        context = browser.new_context()
        yield context
        browser.close()

@pytest.fixture
def page(browser_context):
    """
    Create a fresh page per test. 
    Includes network interception to block leaked localhost resources.
    """
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture
def login_page(page):
    """Navigate to the login URL and return a LoginPage instance."""
    lp = LoginPage(page)
    lp.navigate(BASE_URL)
    return lp

@pytest.fixture
def add_form(login_page):
    """Navigate to the add form URL and return an AddForm instance."""
    login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)
    af = AddForm(login_page.page)
    return af