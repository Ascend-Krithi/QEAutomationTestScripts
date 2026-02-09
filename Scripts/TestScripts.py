import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.FinancialTransferPage import FinancialTransferPage

class TestScripts(unittest.TestCase):
    # ... (existing methods, do not modify)

    def test_TC_158_01_valid_transfer(self):
        """
        TC-158-01: Valid transfer (all fields present)
        - Prepare a valid JSON payload for financial transfer with all required fields.
        - Validate the payload using FinancialTransferPage.validate_payload().
        - Simulate submission using FinancialTransferPage.submit_transfer().
        - Assert that the payload is valid and the submission response is either a success or stub.
        """
        driver = webdriver.Chrome()
        try:
            transfer_page = FinancialTransferPage(driver)
            payload = transfer_page.prepare_transfer_payload(
                amount=100.00,
                currency='USD',
                source='ACC123',
                destination='ACC456',
                timestamp='2024-06-01T10:00:00Z'
            )
            is_valid, validation_msg = transfer_page.validate_payload(payload)
            self.assertTrue(is_valid, f"Payload should be valid, but got: {validation_msg}")

            submission_response = transfer_page.submit_transfer(payload)
            self.assertIn(
                submission_response.get('status'),
                ['success', 'stub'],
                f"Submission response should be 'success' or 'stub', got: {submission_response.get('status')}"
            )
        finally:
            driver.quit()

    def test_TC_158_02_missing_destination(self):
        """
        TC-158-02: Missing 'destination' field
        - Prepare a JSON payload missing the 'destination' field.
        - Validate the payload using FinancialTransferPage.validate_payload().
        - Simulate submission using FinancialTransferPage.submit_transfer().
        - Assert that the payload is invalid and the error message indicates the missing 'destination' field.
        """
        driver = webdriver.Chrome()
        try:
            transfer_page = FinancialTransferPage(driver)
            payload = transfer_page.prepare_transfer_payload(
                amount=50.00,
                currency='USD',
                source='ACC123',
                destination=None,
                timestamp='2024-06-01T10:00:00Z'
            )
            is_valid, validation_msg = transfer_page.validate_payload(payload)
            self.assertFalse(is_valid, "Payload should be invalid due to missing 'destination' field.")
            self.assertIn(
                'destination',
                validation_msg.lower(),
                f"Validation message should indicate missing 'destination' field, got: {validation_msg}"
            )

            submission_response = transfer_page.submit_transfer(payload)
            self.assertEqual(
                submission_response.get('status'),
                'error',
                f"Submission response should be 'error' for missing destination, got: {submission_response.get('status')}"
            )
            self.assertIn(
                'destination',
                submission_response.get('message', '').lower(),
                f"Submission error message should mention 'destination', got: {submission_response.get('message')}"
            )
        finally:
            driver.quit()
