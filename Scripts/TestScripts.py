import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Existing test methods ...

    def test_TC_Login_08_forgot_password_redirect(self):
        """TC_Login_08: Navigate to login page, click forgot password, expect redirect to password recovery page."""
        self.login_page.navigate_to_login_page()
        self.login_page.click_forgot_password()
        self.assertTrue(
            self.login_page.is_password_recovery_redirected(),
            "User was not redirected to password recovery page after clicking 'Forgot Password'."
        )

    def test_TC_Login_09_max_length_input_login(self):
        """TC_Login_09: Navigate to login page, enter max-length email and valid password, click login, expect fields accept max input and login succeeds."""
        self.login_page.navigate_to_login_page()
        login_success = self.login_page.login_with_max_length_email()
        self.assertTrue(
            login_success,
            "Login did not succeed with max-length email and valid password."
        )

if __name__ == "__main__":
    unittest.main()
