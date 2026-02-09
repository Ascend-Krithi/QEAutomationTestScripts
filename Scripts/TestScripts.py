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

# ... [existing test methods here] ...

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
    error_message = login_page.validate_empty_credentials()
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
    # Step 1-4: Login with 'Remember Me'
    login_page.navigate_to_login_page(login_url)
    assert driver.current_url.endswith("/login")
    login_page.login_with_credentials(email, password, remember_me=True)
    # Step 5: Close and reopen browser (simulate by getting cookies, restarting driver, and adding cookies)
    cookies = driver.get_cookies()
    driver.quit()
    driver2 = webdriver.Chrome()
    driver2.get(login_url)
    for cookie in cookies:
        driver2.add_cookie(cookie)
    driver2.get(dashboard_url)
    dashboard_page = DashboardPage(driver2)
    assert dashboard_page.is_dashboard_displayed(), "Dashboard should be displayed, session persisted."
    driver2.quit()
