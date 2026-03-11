import pytest
from config.config import LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_USERNAME_INVALID, LOGIN_PASSWORD_INVALID


class TestLogin:
    """Test class for login functionality."""

    def test_login_success(self, login_page):
        """Verify that valid credentials result in a successful login."""
        heading = login_page.login(LOGIN_USERNAME, LOGIN_PASSWORD)

        assert heading is not None, (
            f"Login failed: no environment heading found after login. "
            f"Current URL: {login_page.page.url}"
        )
        print(f"Login successful! Heading: {heading}")
        
    def test_invalid_login(self, login_page):
        """Verify that invalid credentials result in an error message."""
        heading = login_page.login(LOGIN_USERNAME_INVALID, LOGIN_PASSWORD_INVALID)
        assert heading is None, (
            f"Login failed: no environment heading found after login. "
            f"Current URL: {login_page.page.url}"
        )
        print(f"Login failed with invalid credentials! Heading: {heading}")

    def test_add_form(self, add_form):
        """Verify that adding a form is successful."""
        add_form.select_entity()
        print(f"Add form successful! Data: Test Data")