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
