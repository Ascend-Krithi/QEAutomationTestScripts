
import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

class TestScripts(unittest.TestCase):

    # Existing test methods...

    def test_login_valid_credentials(self):
        """TC01: Validate successful login redirects to dashboard."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            login_page.enter_username('valid_user')
            login_page.enter_password('valid_password')
            login_page.click_login()
            dashboard_page = DashboardPage(driver)
            self.assertTrue(dashboard_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login.")
        finally:
            driver.quit()

    def test_login_invalid_credentials(self):
        """TC02: Validate error handling for invalid credentials."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.go_to_login_page()
            login_page.enter_username('invalid_user')
            login_page.enter_password('invalid_password')
            login_page.click_login()
            self.assertTrue(login_page.is_error_message_displayed(), "Error message should be displayed for invalid login.")
        finally:
            driver.quit()