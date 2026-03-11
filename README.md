# Automation Python Playwright - Onlygood Staging

This project handles automated UI testing for the Onlygood platform using Python and Playwright.

## Prerequisites

- **Python**: 3.8+
- **Playwright**: 1.43+ (Required for `X25519` encryption support)
- **Chromium**: Version 123+ (Automatically installed with Playwright 1.43+)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright Browsers**:
   ```bash
   playwright install chromium
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```env
   BASE_URL=https://staging.onlygood.world/auth/login
   LOGIN_USERNAME=your_email@example.com
   LOGIN_PASSWORD=your_password
   ```

## Running Tests

To run the login tests:
```bash
pytest tests/test_login.py
```

To see real-time output:
```bash
pytest -s tests/test_login.py
```

## Troubleshooting

### "Failed to secure login request" or "SubtleCrypto" Errors
This error occurs if the browser context is insecure or if the browser version is too old to support the `X25519` elliptic curve algorithm used by the application's encryption service.

**Fix**:
1. Ensure `playwright` is updated to at least version **1.43**.
   ```bash
   pip install -U playwright
   playwright install chromium
   ```
2. Verify that `conftest.py` does not contain flags that disable essential web security features needed for the Web Crypto API.

### URL Blocking
The login URL should be `https://staging.onlygood.world/auth/login`. Avoid adding a trailing dot (e.g., `onlygood.world./`), as this causes SSL certificate mismatches and triggers security blocks.
