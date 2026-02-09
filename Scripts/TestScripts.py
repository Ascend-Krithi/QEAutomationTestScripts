import unittest
from Pages.FinancialTransferPage import FinancialTransferPage

class TestScripts(unittest.TestCase):

    def test_TC_158_01_valid_transfer(self):
        page = FinancialTransferPage()
        response = page.run_tc15801(endpoint_url='/transfer')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json()['status'])

    def test_TC_158_02_invalid_account(self):
        page = FinancialTransferPage()
        response = page.run_tc15802(endpoint_url='/transfer')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid account', response.json()['error'])

    def test_TC_158_03_minimum_amount_success(self):
        page = FinancialTransferPage()
        response = page.run_tc15803(endpoint_url='/transfer')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json()['status'])

    def test_TC_158_04_exceed_maximum_error(self):
        page = FinancialTransferPage()
        response = page.run_tc15804(endpoint_url='/transfer')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Amount exceeds maximum limit', response.json()['error'])

    def test_TC_158_05_extra_field_ignored_and_logged(self):
        page = FinancialTransferPage()
        payload = page.prepare_payload_with_extra_field(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z',
            note='Payment for invoice #123'
        )
        success, response = page.submit_payload_via_api(payload, '/transfer')
        self.assertTrue(success, f"API submission failed: {response}")
        self.assertTrue(page.validate_extra_field_handling(response), f"Extra field 'note' was not ignored/logged properly: {response}")

    def test_TC_158_06_malformed_json_rejected(self):
        page = FinancialTransferPage()
        malformed_payload = '{"amount": 100.00, "currency": "USD", "source": "ACC123", "destination": "ACC456", "timestamp": "2024-06-01T10:00:00Z"'  # missing closing brace
        success, response = page.submit_malformed_payload_via_api(malformed_payload, '/transfer')
        self.assertTrue(success, f"Malformed payload did not trigger error: {response}")
        self.assertTrue(page.validate_malformed_json_error(response), f"Malformed JSON error message not found: {response}")

    def test_TC_158_05_valid_payload_with_extra_field(self):
        """
        TC-158-05: Prepare a valid payload with an extra 'note' field,
        submit it to the /transfer endpoint, and assert that the transfer
        completes and the extra field is ignored or logged.
        """
        page = FinancialTransferPage()
        payload = page.prepare_payload_with_extra_field(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z',
            note='Payment for invoice #123'
        )
        success, response, extra_field_logged = page.handle_valid_payload_with_extra_field(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z',
            note='Payment for invoice #123',
            endpoint_url='/transfer'
        )
        self.assertTrue(success, f"Transfer did not complete successfully: {response}")
        self.assertTrue(extra_field_logged, "Extra field 'note' was not logged.")
        self.assertTrue(page.validate_extra_field_handling(response), f"Extra field was not ignored/logged as expected: {response}")

    def test_TC_158_06_malformed_json_payload(self):
        """
        TC-158-06: Prepare a malformed JSON payload (missing closing brace),
        submit it to the /transfer endpoint, and assert that the API returns
        an error indicating 'Invalid JSON format'.
        """
        page = FinancialTransferPage()
        malformed_payload = '{"amount": 100.00, "currency": "USD", "source": "ACC123", "destination": "ACC456", "timestamp": "2024-06-01T10:00:00Z"'  # missing closing brace
        valid, response = page.handle_malformed_json_payload(
            malformed_payload_str=malformed_payload,
            endpoint_url='/transfer'
        )
        self.assertTrue(valid, f"API did not return expected 'Invalid JSON format' error: {response}")

if __name__ == '__main__':
    unittest.main()
