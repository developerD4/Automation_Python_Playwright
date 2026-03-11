class LoginPage:

    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#email")
        self.password_input = page.locator("#pswrd")
        self.login_button = page.locator("button[type='submit']")
        # Dashboard selectors
        self.dashboard_nav = page.locator("h3").first
        # Error message selectors
        self.error_message = page.locator(".toast-message, .alert-danger, [role='alert'], .error-msg")

    def navigate(self, url):
        print(f"Navigating to: {url}")
        self.page.goto(url)

    def enter_username(self, username):
        self.username_input.wait_for(state='visible', timeout=10000)
        self.username_input.fill(username)

    def enter_password(self, password):
        self.password_input.wait_for(state='visible', timeout=10000)
        self.password_input.fill(password)

    def click_login(self):
        """Click the Sign In button and wait for result."""
        self.login_button.wait_for(state='visible', timeout=10000)
        
        print("Clicking Sign In button...")
        self.login_button.click()

    def get_environment_heading(self):
        # Wait for dashboard content
        print("Waiting for dashboard element...")
        self.dashboard_nav.wait_for(state='visible', timeout=10000)
        return self.dashboard_nav.inner_text()

    def login(self, username, password):
        try:
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()
            self.page.wait_for_load_state("load")
            heading = self.get_environment_heading()
            return heading
        except Exception as e:
            print(f"Login failed with exception: {e}")
            return None