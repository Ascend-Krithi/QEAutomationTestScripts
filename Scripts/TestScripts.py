# Scripts/TestScripts.py
import unittest
from selenium import webdriver
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = LoginPage(self.driver)
        self.base_url = "http://localhost:8000"  # Adjust as appropriate for your environment

    def test_TC03_empty_username_and_password(self):
        """
        TC03: Submit empty username and password, expect error 'Username and password are required'.
        """
        self.page.navigate_to_login(self.base_url)
        self.page.submit_empty_credentials()
        self.assertTrue(
            self.page.validate_error_for_empty_credentials("Username and password are required"),
            "Expected error message for empty credentials not displayed."
        )

    def test_TC04_empty_username_valid_password(self):
        """
        TC04: Submit empty username and valid password, expect error 'Username is required'.
        """
        self.page.navigate_to_login(self.base_url)
        self.page.submit_empty_username_valid_password("ValidPass123")
        self.assertTrue(
            self.page.validate_error_for_empty_credentials("Username is required"),
            "Expected error message for empty username not displayed."
        )

class TestFinancialTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = FinancialTransferPage(self.driver)

    def test_TC_158_01_valid_financial_transfer(self):
        """
        TC-158-01: Valid financial transfer
        """
        confirmation = self.page.submit_transfer_payload(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z'
        )
        confirmation_message = self.page.get_confirmation_message()
        self.assertIsInstance(confirmation_message, str)
        self.assertTrue(len(confirmation_message) > 0, "Confirmation message should not be empty.")

    def test_TC_158_02_invalid_transfer_missing_destination(self):
        """
        TC-158-02: Invalid transfer missing 'destination' field
        """
        self.page.submit_invalid_payload(
            amount=50.00,
            currency='USD',
            source='ACC123',
            timestamp='2024-06-01T10:00:00Z'
        )
        error_message = self.page.get_error_message()
        self.assertIsInstance(error_message, str)
        self.assertIn('destination', error_message.lower(), "Error message should mention missing 'destination'.")

if __name__ == "__main__":
    unittest.main()
