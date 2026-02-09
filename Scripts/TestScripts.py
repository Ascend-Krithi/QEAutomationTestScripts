# Scripts/TestScripts.py
import unittest
from selenium import webdriver
from Pages.FinancialTransferPage import FinancialTransferPage

class TestLogin(unittest.TestCase):
    # Existing login-related test methods...
    pass

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
