import unittest
from RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage
from selenium import webdriver

class TestRuleConfiguration(unittest.TestCase):

    def setUp(self):
        self.page = RuleConfigurationPage()

    # Existing test methods...

    def test_TC_SCRUM158_01(self):
        ...
    # (all other methods as above)

    def test_TC03_login_empty_credentials(self):
        ...
    def test_TC04_login_empty_username(self):
        ...

    def test_TC05_login_empty_password(self):
        """TC05: Navigate to login page, enter valid username and leave password empty, click login, expect error 'Password is required'."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page()
            login_page.enter_username("valid_user")
            login_page.leave_password_empty()
            login_page.click_login_button()
            result = login_page.validate_error_message("Password is required")
            self.assertTrue(result, "Expected error message 'Password is required' not displayed.")
        finally:
            driver.quit()

    def test_TC06_login_remember_me(self):
        """TC06: Navigate to login page, enter valid username and password, check 'Remember Me', click login, expect session persists after browser restart."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        try:
            login_page.navigate_to_login_page()
            login_page.enter_username("valid_user")
            login_page.enter_password("ValidPass123")
            login_page.select_remember_me()
            login_page.click_login_button()
            result = login_page.validate_session_persistence()
            self.assertTrue(result, "Session did not persist after browser restart.")
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
