import unittest
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

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

    def test_TC_158_07_performance_bulk_transfers(self):
        """
        TC-158-07: Prepare and submit 10,000 valid transfer payloads in rapid succession.
        Assert all transfers are processed within <1s per transfer. Monitor API response times and throughput.
        """
        page = FinancialTransferPage()
        base_payload = {
            "amount": 100.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456"
        }
        metrics = page.submit_bulk_transfers_api(base_payload, num_transfers=10000, auth_token="valid_token")
        self.assertTrue(metrics['successes'] >= 9990, f"Bulk transfer did not process enough successes: {metrics['successes']}")
        self.assertTrue(metrics['max_time'] < 1.0, f"Some transfers exceeded 1s: max_time={metrics['max_time']}")
        self.assertTrue(metrics['throughput'] > 500, f"Throughput too low: {metrics['throughput']}")

    def test_TC_158_08_invalid_auth_token(self):
        """
        TC-158-08: Submit a valid payload with an invalid authentication token, expect rejection with authentication error.
        """
        page = FinancialTransferPage()
        payload = {
            "amount": 100.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        result = page.submit_transfer_invalid_auth(payload, invalid_token="bad_token")
        self.assertEqual(result['status'], "rejected", f"Transfer was not rejected as expected: {result['response']}")
        self.assertEqual(result['error_message'], "Invalid authentication token", f"Error message mismatch: {result['error_message']}")

    def test_TC_158_09_valid_transfer(self):
        """TC-158-09: Submit valid transfer and verify processing"""
        page = FinancialTransferPage()
        payload = {
            'amount': 200.00,
            'currency': 'USD',
            'source': 'ACC123',
            'destination': 'ACC456',
            'timestamp': '2024-06-01T10:00:00Z'
        }
        response = page.submit_transfer(payload)
        self.assertTrue(page.is_transfer_successful(response), "Transfer was not processed successfully")
        # Stub: Check for backend log entry (to be implemented)
        backend_log = page.check_backend_log_entry(payload)
        self.assertTrue(backend_log, "Backend log entry for transfer not found (stub)")

    def test_TC_158_10_unsupported_currency(self):
        """TC-158-10: Submit transfer with unsupported currency and verify error"""
        page = FinancialTransferPage()
        payload = {
            'amount': 100.00,
            'currency': 'XYZ',  # Unsupported currency
            'source': 'ACC123',
            'destination': 'ACC456',
            'timestamp': '2024-06-01T10:00:00Z'
        }
        response = page.submit_transfer(payload)
        self.assertFalse(page.is_transfer_successful(response), "Transfer should not succeed with unsupported currency")
        self.assertIn('Unsupported currency', page.get_error_message(response), "Error message does not indicate unsupported currency")

    # --- New Tests for Rule Configuration Automation ---
    def test_TC_SCRUM158_01_rule_schema_persistence(self):
        """
        TC_SCRUM158_01: Prepare a JSON rule schema with all supported trigger, condition, and action types, submit it via API, and validate persistence in the database.
        """
        page = RuleConfigurationPage(driver=None)
        schema = page.prepare_rule_schema()
        api_response = page.submit_rule_schema_api(schema)
        self.assertIn('id', api_response, 'API did not return rule id')
        rule_id = api_response['id']
        db_rule = page.retrieve_rule_from_db(rule_id)
        self.assertEqual(schema['trigger'], db_rule['trigger'], 'Trigger mismatch between schema and DB')
        self.assertEqual(schema['conditions'], db_rule['conditions'], 'Conditions mismatch between schema and DB')
        self.assertEqual(schema['actions'], db_rule['actions'], 'Actions mismatch between schema and DB')

    def test_TC_SCRUM158_02_rule_simulation(self):
        """
        TC_SCRUM158_02: Prepare a rule schema with two conditions and two actions, submit via API, and verify simulation logic.
        """
        page = RuleConfigurationPage(driver=None)
        conditions = [
            {"type": "amount_above", "value": 1000},
            {"type": "date_range", "start": "2024-01-01", "end": "2024-12-31"}
        ]
        actions = [
            {"type": "notify", "recipient": "admin"},
            {"type": "transfer", "account": "external"}
        ]
        schema = page.prepare_rule_schema(conditions=conditions, actions=actions)
        api_response = page.submit_rule_schema_api(schema)
        self.assertIn('id', api_response, 'API did not return rule id')
        simulation_result = page.simulate_rule_evaluation(schema)
        self.assertTrue(simulation_result['conditions_evaluated'], 'Conditions not evaluated as expected')
        self.assertTrue(simulation_result['actions_triggered'], 'Actions not triggered as expected')
        self.assertIn('details', simulation_result)

if __name__ == '__main__':
    unittest.main()
