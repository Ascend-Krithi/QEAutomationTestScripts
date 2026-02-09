# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow), TC_LOGIN_008 (SQL injection handling), TC_LOGIN_009 (max input length and invalid credentials error), TC_LOGIN_010 (user not found error), TC_Login_10 (max input length valid credentials), and TC_LOGIN_004 (max input length and error feedback).
"""
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# TC_LOGIN_005: Empty Credentials Error Handling
def test_login_empty_credentials_error(driver):
    """
    1. Navigate to the login page
    2. Leave both email/username and password fields empty
    3. Click the 'Login' button
    4. Verify error message is shown and user remains on login page
    """
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login")
    error_message = login_page.login_with_empty_fields_and_check_error()
    assert error_message is not None, "Error message should be displayed for empty credentials."
    assert "required" in error_message.lower(), f"Expected 'required' in error message, got: {error_message}"
    assert driver.current_url.endswith("/login"), "User should remain on login page."

# TC_LOGIN_006: 'Remember Me' and Session Persistence
def test_login_remember_me_session_persistence(driver):
    """
    1. Navigate to the login page
    2. Enter valid email/username and valid password
    3. Check the 'Remember Me' checkbox
    4. Click the 'Login' button
    5. Close and reopen the browser, revisit the website
    6. Verify user remains logged in and dashboard is displayed
    """
    login_page = LoginPage(driver)
    dashboard_url = "https://axos.example.com/dashboard"
    login_url = "https://axos.example.com/login"
    email = "user@example.com"
    password = "ValidPass123"
    login_page.navigate_to_login_page(login_url)
    assert driver.current_url.endswith("/login")
    login_page.login_with_credentials(email, password, remember_me=True)
    session_persisted = login_page.verify_remember_me_persistence(login_url, email, password)
    assert session_persisted, "Session should persist and user should remain logged in."

# TC_LOGIN_007: Forgot Password Flow
def test_login_forgot_password_flow(driver):
    """
    1. Navigate to the login page
    2. Click the 'Forgot Password' link
    3. Verify presence of password recovery form
    """
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login"), "Login page should be displayed."
    clicked = login_page.click_forgot_password_link()
    assert clicked, "Should be able to click 'Forgot Password' link."
    form_displayed = login_page.is_password_recovery_form_displayed()
    assert form_displayed, "Password recovery form should be displayed."

# TC_LOGIN_008: SQL Injection Attempt
def test_login_sql_injection_attempt(driver):
    """
    1. Navigate to the login page
    2. Enter SQL injection string in email/username and/or password fields
    3. Click the 'Login' button
    4. Verify error message 'Invalid credentials' is shown. No security breach occurs.
    """
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page("https://axos.example.com/login")
    assert driver.current_url.endswith("/login"), "Login page should be displayed."
    email_injection = "' OR 1=1;--"
    password_injection = "' OR 1=1;--"
    login_page.attempt_sql_injection_login(email_injection, password_injection)
    error_valid = login_page.verify_invalid_credentials_error()
    assert error_valid, "Error message 'Invalid credentials' should be shown and no security breach occurs."
