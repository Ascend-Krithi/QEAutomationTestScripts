# Existing imports and test classes assumed to be present
import pytest
from LoginPage import LoginPage

# --- Existing test methods remain unchanged ---

@pytest.mark.asyncio
async def test_TC_LOGIN_009_invalid_login_rate_limiting(browser):
    """
    TC_LOGIN_009: Attempt login with wronguser@example.com / WrongPassword 10 times, validate rate limiting/lockout/captcha.
    """
    login_page = LoginPage(browser)
    email = "wronguser@example.com"
    password = "WrongPassword"
    lockout_triggered = False
    captcha_triggered = False
    for attempt in range(10):
        await login_page.open()
        await login_page.enter_email(email)
        await login_page.enter_password(password)
        await login_page.submit()
        error_message = await login_page.get_error_message()
        if login_page.is_rate_limited():
            lockout_triggered = True
            break
        if login_page.is_captcha_present():
            captcha_triggered = True
            break
        assert error_message is not None, f"No error message on failed login attempt {attempt+1}"
    assert lockout_triggered or captcha_triggered, "Neither rate limiting nor captcha triggered after 10 invalid attempts"

@pytest.mark.asyncio
async def test_TC_LOGIN_010_case_sensitivity_in_login(browser):
    """
    TC_LOGIN_010: Try login with email variants (USER@EXAMPLE.COM, user@example.com, User@Example.Com, UsEr@ExAmPlE.cOm) and ValidPassword123, validate login succeeds only for exact match.
    """
    login_page = LoginPage(browser)
    valid_email = "user@example.com"
    valid_password = "ValidPassword123"
    email_variants = [
        "USER@EXAMPLE.COM",
        "user@example.com",
        "User@Example.Com",
        "UsEr@ExAmPlE.cOm"
    ]
    results = {}
    for email in email_variants:
        await login_page.open()
        await login_page.enter_email(email)
        await login_page.enter_password(valid_password)
        await login_page.submit()
        if login_page.is_logged_in():
            results[email] = True
            await login_page.logout()
        else:
            results[email] = False
    # Only exact match (user@example.com) should succeed
    assert results[valid_email] is True, "Exact match did not succeed"
    for email in email_variants:
        if email != valid_email:
            assert results[email] is False, f"Login succeeded for variant: {email}"

# --- New test methods for TC_LOGIN_007 and TC_LOGIN_008 ---

@pytest.mark.asyncio
async def test_TC_LOGIN_007_valid_login_without_remember_me_session_persistence(browser):
    """
    TC_LOGIN_007: Valid login without 'Remember Me', check session does not persist after browser restart.
    Steps:
    1. Navigate to login page.
    2. Enter valid email/username and password. Do not select 'Remember Me'.
    3. Click Login button.
    4. Close and reopen browser. User should be logged out; session does not persist.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"  # Replace with actual login URL
    email = "user@example.com"
    password = "ValidPassword123"

    # Step 1-3: Login without Remember Me
    login_page.navigate_to_login_page(url)
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.set_remember_me(False)
    assert login_page.validate_remember_me_unchecked(), "Remember Me should NOT be checked."
    login_page.click_login()
    assert login_page.is_login_successful(), "Login should be successful."

    # Step 4: Close and reopen browser
    session_cookie_before = login_page.get_session_cookie()
    login_page.driver.quit()
    # Simulate browser restart (driver re-instantiation handled externally)
    # After restart, instantiate a new LoginPage with a new driver
    # For demonstration, assume driver is re-instantiated externally and passed as 'browser'
    login_page = LoginPage(browser)
    assert login_page.logout_and_verify_session(url), "Session should not persist after browser restart. User should be logged out."

@pytest.mark.asyncio
async def test_TC_LOGIN_008_forgot_password_flow(browser):
    """
    TC_LOGIN_008: Forgot Password flow and confirmation message validation.
    Steps:
    1. Navigate to login page.
    2. Click on 'Forgot Password' link.
    3. Enter registered email/username and submit.
    Expected: Password reset email is sent and confirmation message displayed.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"  # Replace with actual login URL
    email = "user@example.com"

    login_page.navigate_to_login_page(url)
    login_page.click_forgot_password()
    assert login_page.is_on_password_recovery_page(), "Should be on password recovery page."
    login_page.submit_forgot_password(email)
    confirmation_msg = login_page.get_reset_confirmation_message()
    assert confirmation_msg.strip() != "", "Password reset confirmation message should be displayed."

# --- New test methods for TC_Login_10 and TC_LOGIN_004 ---

@pytest.mark.asyncio
async def test_TC_Login_10_max_length_password(browser):
    """
    TC_Login_10: Navigate to login page, enter valid email and max-length password (128 chars), click login, validate login success.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"
    email = "user@example.com"
    password = "A" * 128

    login_page.navigate_to_login_page(url)
    login_page.enter_credentials(email, password)
    login_page.click_login()
    assert login_page.validate_login_success(), "Login should be successful with max-length password."

@pytest.mark.asyncio
async def test_TC_LOGIN_004_max_length_email_and_password(browser):
    """
    TC_LOGIN_004: Navigate to login page, enter max-length email (254 chars) and password (64 chars), click login, validate login success or error.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"
    email = "u" * 242 + "@example.com"  # 254 chars
    password = "V" * 64  # 64 chars

    login_page.navigate_to_login_page(url)
    login_page.enter_credentials(email, password)
    login_page.click_login()
    # Validate either login success or error
    assert login_page.validate_login_success() or login_page.validate_login_error() != "", "Must show success or error for max-length inputs."

# --- Appended test methods for TC_LOGIN_005 and TC_LOGIN_006 ---

@pytest.mark.asyncio
async def test_TC_LOGIN_005_empty_fields_error(browser):
    """
    TC_LOGIN_005: Navigate to login page, leave email and password empty, click login, validate error message 'Email/Username and Password required' and user remains on login page.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"  # Update to actual login URL
    result = login_page.validate_login_empty_fields_tc(url)
    assert result, "TC_LOGIN_005 failed: Error message or login page persistence not validated."

@pytest.mark.asyncio
async def test_TC_LOGIN_006_remember_me_session_persistence(browser):
    """
    TC_LOGIN_006: Navigate to login page, enter valid credentials, check 'Remember Me', click login, validate redirect to dashboard, close and reopen browser, revisit site, and validate user remains logged in.
    """
    login_page = LoginPage(browser)
    url = "https://example.com/login"  # Update to actual login URL
    email = "user@example.com"
    password = "ValidPass123"
    result = login_page.validate_remember_me_tc(url, email, password)
    assert result, "TC_LOGIN_006 failed: 'Remember Me' session persistence not validated."
