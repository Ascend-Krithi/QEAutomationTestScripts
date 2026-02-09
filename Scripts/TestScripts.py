# Scripts/TestScripts.py
import unittest
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.FinancialTransferPage import FinancialTransferPage

class TestFinancialTransfer(unittest.TestCase):
    def setUp(self):
        # Setup code for WebDriver, e.g. Chrome
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        # Optionally login if needed
        # ...
        self.page = FinancialTransferPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods remain unchanged

    def test_valid_financial_transfer_TC15801(self):
        """
        TC-158-01: Valid transfer, all fields present, expect success.
        """
        payload = {
            "amount": 1000.0,
            "currency": "USD",
            "source": "AccountA",
            "destination": "AccountB",
            "timestamp": "2024-06-18T12:34:56Z"
        }
        self.page.open_transfer_dialog()
        self.page.enter_transfer_payload(json.dumps(payload))
        self.page.submit_transfer()
        # Wait for success message
        success_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "transfer-success-message"))
        )
        self.assertIn("Transfer successful", success_msg.text)

    def test_missing_destination_financial_transfer_TC15802(self):
        """
        TC-158-02: Missing 'destination', expect error mentioning 'destination'.
        """
        payload = {
            "amount": 1000.0,
            "currency": "USD",
            "source": "AccountA",
            # 'destination' omitted
            "timestamp": "2024-06-18T12:34:56Z"
        }
        self.page.open_transfer_dialog()
        self.page.enter_transfer_payload(json.dumps(payload))
        self.page.submit_transfer()
        # Wait for error message
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "transfer-error-message"))
        )
        self.assertIn("destination", error_msg.text.lower())
