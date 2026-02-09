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

if __name__ == '__main__':
    unittest.main()
