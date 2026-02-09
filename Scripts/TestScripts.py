# Scripts/TestScripts.py
"""
Test scripts for LoginPage scenarios: TC_LOGIN_007 (Forgot Password flow) and TC_LOGIN_008 (SQL injection handling).
"""
import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# TC_LOGIN_007: Forgot Password flow
def test_forgot_password_flow(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Click 'Forgot Password' link
    login_page.click_forgot_password()
    # Step 3: Verify presence of password recovery form
    assert login_page.is_password_recovery_form_displayed(), "Password recovery form should be displayed."

# TC_LOGIN_008: SQL Injection attempt handling
def test_sql_injection_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login("https://axos.example.com/login")
    # Step 1: Login page is displayed
    assert driver.current_url.endswith("/login")
    # Step 2: Enter SQL injection strings
    sql_email = "' OR 1=1;--"
    sql_password = "' OR 1=1;--"
    login_page.login_with_sql_injection(sql_email, sql_password)
    # Step 3: Click 'Login' button (done in login_with_sql_injection)
    # Step 4: Verify error message and no security breach
    assert login_page.validate_invalid_credentials_error(), "Invalid credentials error should be shown."