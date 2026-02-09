import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods preserved below
    # ... (existing methods here)

    def test_TC01_valid_login(self):
        """Test valid login scenario."""
        self.login_page.navigate_to_login()
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('ValidPass123')
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_dashboard_displayed(), "Dashboard should be displayed after valid login.")

    def test_TC02_invalid_login(self):
        """Test invalid login scenario."""
        self.login_page.navigate_to_login()
        self.login_page.enter_username('invalid_user')
        self.login_page.enter_password('WrongPass')
        self.login_page.click_login()
        error_message = self.login_page.get_error_message()
        self.assertEqual(error_message, 'Invalid username or password', "Error message should match expected.")
        self.assertFalse(self.login_page.is_dashboard_displayed(), "Dashboard should NOT be displayed after invalid login.")

if __name__ == '__main__':
    unittest.main()
