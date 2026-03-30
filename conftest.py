import pytest
import os
import allure
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
                # '--unsafely-treat-insecure-origin-as-secure=https://staging.onlygood.world.,https://staging.onlygood.world',
            ]
        )
        context = browser.new_context()
        yield context
        browser.close()

# @pytest.fixture
# def page(request, browser_context):
#     """
#     Create a fresh page per test. 
#     Includes network interception to block leaked localhost resources.
#     """
#     page = browser_context.new_page()
#     yield page
    
#     # Take a screenshot after the test finishes
#     import os
#     os.makedirs("screenshots", exist_ok=True)
#     screenshot_path = f"screenshots/{request.node.name}.png"
#     try:
#         page.screenshot(path=screenshot_path, full_page=True)
#         print(f"\nScreenshot saved to {screenshot_path}")
#     except Exception as e:
#         print(f"\nFailed to take screenshot: {e}")
        
#     page.close()

@pytest.fixture
def page(request, browser_context):
    """
    Create a fresh page per test.
    On teardown:
      1. Saves a PNG screenshot to screenshots/<test_name>.png  (existing behaviour)
      2. Attaches the same PNG to the Allure report              (new behaviour)
    """
    page = browser_context.new_page()
    yield page

    # ── 1. Save screenshot to disk (your original logic) ─────────────────────
    os.makedirs("screenshots", exist_ok=True)                  # create folder if missing
    screenshot_path = f"screenshots/{request.node.name}.png"   # path uses test name
    try:
        page.screenshot(path=screenshot_path, full_page=True)  # capture full page
        print(f"\nScreenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"\nFailed to take screenshot: {e}")

    # ── 2. [NEW] Attach the same screenshot to Allure ─────────────────────────
    try:
        with open(screenshot_path, "rb") as f:                 # open the saved PNG
            allure.attach(                                      # attach it to Allure
                f.read(),                                       # raw bytes of the image
                name=f"Screenshot – {request.node.name}",      # label shown in report
                attachment_type=allure.attachment_type.PNG,    # tell Allure it's a PNG
            )
    except Exception as e:
        print(f"\nFailed to attach screenshot to Allure: {e}")

    page.close()


# ── [NEW] Hook: attach an extra screenshot specifically on test FAILURE ────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Runs around every test phase (setup / call / teardown).
    When the 'call' phase fails we capture an immediate failure screenshot
    and attach it to Allure before the page is closed in the fixture teardown.
    """
    outcome = yield                    # let the test phase run to completion
    rep = outcome.get_result()         # grab the result object

    # Only act on the actual test body ('call'), not setup/teardown
    if rep.when == "call" and rep.failed:
        pg = item.funcargs.get("page") # safely fetch the page fixture if it exists
        if pg:
            try:
                # Capture full-page screenshot as raw bytes (no disk write needed)
                screenshot_bytes = pg.screenshot(full_page=True)

                allure.attach(
                    screenshot_bytes,
                    name="FAILURE – " + item.name,             # clearly labelled
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"\nFailed to attach failure screenshot to Allure: {e}")

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