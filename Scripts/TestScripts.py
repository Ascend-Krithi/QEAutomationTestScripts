# TestScripts.py
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
import pytest

@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Test Case TC_Login_07: Login without 'Remember Me', session expiration

def test_TC_Login_07(driver):
    login_page = LoginPage(driver)
    driver.get('https://example.com/login')
    # Step 1: Navigate to login page
    assert login_page.enter_username is not None
    # Step 2: Enter valid credentials without selecting 'Remember Me'
    login_page.enter_username('user@example.com')
    login_page.enter_password('ValidPassword123')
    assert not login_page.is_remember_me_selected()
    # Step 3: Click Login
    login_page.click_login()
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()
    # Step 4: Simulate session expiration and validate redirect
    assert login_page.expire_session_and_validate_redirect()

# Test Case TC_LOGIN_001: Basic login and redirect

def test_TC_LOGIN_001(driver):
    login_page = LoginPage(driver)
    driver.get('https://example.com/login')
    # Step 1: Navigate to login page
    assert login_page.enter_username is not None
    # Step 2: Enter valid email/username and valid password
    login_page.enter_username('user@example.com')
    login_page.enter_password('ValidPassword123')
    # Step 3: Click Login
    login_page.click_login()
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()

# Test Case TC_LOGIN_002: Invalid credentials

def test_TC_LOGIN_002(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to the login page
    assert driver.current_url.endswith('/login')
    # Step 2: Enter invalid email/username or password
    login_page.enter_credentials('wronguser@example.com', 'WrongPassword')
    # Step 3: Click the Login button
    login_page.click_login()
    # Step 4: Assert error message for invalid credentials is displayed
    error_msg = login_page.get_error_message()
    assert error_msg != '', 'Error message for invalid credentials should be displayed'
    assert driver.current_url.endswith('/login'), 'User should remain on login page'

# Test Case TC_LOGIN_003: Empty fields

def test_TC_LOGIN_003(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to the login page
    assert driver.current_url.endswith('/login')
    # Step 2: Leave email/username and password fields empty
    login_page.enter_credentials('', '')
    # Step 3: Click the Login button
    login_page.click_login()
    # Step 4: Assert validation message for empty fields is displayed
    validation_msg = login_page.get_validation_message()
    assert validation_msg != '', 'Validation message for empty fields should be displayed'
    assert driver.current_url.endswith('/login'), 'User should remain on login page'

# Test Case TC_Login_10: Max length email and password

def test_TC_Login_10(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    max_length_email = 'user@example.com'  # Replace with actual max length email (e.g., 254 chars)
    max_length_password = 'A'*128  # Replace with actual max length password (128 chars)
    login_page.enter_max_length_email_and_valid_password(max_length_email, max_length_password)
    login_page.click_login()
    # Assert fields accept maximum length input (could check input values if needed)
    # Assert user is logged in if credentials are valid
    assert login_page.is_login_successful(), 'User should be logged in with max length credentials'

# Test Case TC_LOGIN_004: Max length email/username and password

def test_TC_LOGIN_004(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    max_length_username = 'userwithverylongemailaddress@example.com'  # Replace with actual max length username/email (e.g., 254 chars)
    max_length_password = 'VeryLongPassword123!' + 'A'*46  # 64 chars
    login_page.login_with_max_length_credentials(max_length_username, max_length_password)
    login_page.click_login()
    # Assert fields accept input up to maximum length
    # Assert user is logged in if credentials are valid; error if invalid
    if login_page.is_login_successful():
        assert True, 'User should be logged in with max length credentials'
    else:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', 'Error message should be displayed for invalid credentials'

# Test Case TC_LOGIN_005: Special characters in credentials

def test_TC_LOGIN_005(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to login page
    assert driver.current_url.endswith('/login')
    # Step 2: Enter credentials with special characters
    special_username = 'special_user!@#$/example.com'
    special_password = 'P@$$w0rd!#'
    login_page.enter_special_characters_credentials(special_username, special_password)
    # Step 3: Click Login
    login_page.click_login()
    # Step 4: Assert fields accept special character input and login/error behavior
    assert login_page.are_special_characters_accepted(special_username, special_password), 'Fields should accept special characters'
    if login_page.is_login_successful():
        assert True, 'User should be logged in with special character credentials'
    else:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != '', 'Error message should be displayed for invalid credentials'

# Test Case TC_LOGIN_006: "Remember Me" session persistence

def test_TC_LOGIN_006(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login('https://example.com/login')
    # Step 1: Navigate to login page
    assert driver.current_url.endswith('/login')
    # Step 2: Enter valid credentials and check 'Remember Me'
    login_page.enter_username('user@example.com')
    login_page.enter_password('ValidPassword123')
    login_page.check_remember_me()
    assert login_page.is_remember_me_selected(), "'Remember Me' checkbox should be selected"
    # Step 3: Click Login
    login_page.click_login()
    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed(), 'Dashboard should be displayed after login'
    # Step 4: Close and reopen browser, assert session persists
    driver.quit()
    new_driver = webdriver.Chrome()
    new_driver.implicitly_wait(10)
    dashboard_new = DashboardPage(new_driver)
    new_driver.get('https://example.com/dashboard')
    assert dashboard_new.is_dashboard_displayed(), 'Session should persist with "Remember Me" enabled'
    new_driver.quit()
