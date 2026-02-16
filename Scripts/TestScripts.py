# Existing imports and code ...

import unittest
from BillPayPage import BillPayPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestBillPay(unittest.TestCase):
    # Existing test methods ...

    def test_tc_bp_001_successful_bill_payment(self):
        """
        TC-BP-001: Successful Bill Payment
        Steps:
        1. Navigate to Bill Pay page
        2. Enter valid payee details (Name, Address, Account, Amount)
        3. Submit payment
        Expected: Confirmation message displayed, payment recorded
        """
        bill_pay_page = BillPayPage(self.driver)
        bill_pay_page.navigate_to()
        bill_pay_page.enter_payee_name("John Doe")
        bill_pay_page.enter_payee_address("123 Main St, Springfield")
        bill_pay_page.enter_payee_account("987654321")
        bill_pay_page.enter_payment_amount("150.00")
        bill_pay_page.submit_payment()

        confirmation = bill_pay_page.get_confirmation_message()
        self.assertIn("Payment successful", confirmation)
        self.assertTrue(bill_pay_page.is_payment_recorded("John Doe", "987654321", "150.00"))

    def test_tc_bp_002_invalid_account_number(self):
        """
        TC-BP-002: Invalid Account Number
        Steps:
        1. Navigate to Bill Pay page
        2. Enter payee details with invalid account number
        3. Submit payment
        Expected: Error message for invalid account number, payment not processed
        """
        bill_pay_page = BillPayPage(self.driver)
        bill_pay_page.navigate_to()
        bill_pay_page.enter_payee_name("Jane Smith")
        bill_pay_page.enter_payee_address("456 Elm St, Metropolis")
        bill_pay_page.enter_payee_account("abc123")  # Invalid account
        bill_pay_page.enter_payment_amount("200.00")
        bill_pay_page.submit_payment()

        error = bill_pay_page.get_error_message()
        self.assertIn("Invalid account number", error)
        self.assertFalse(bill_pay_page.is_payment_recorded("Jane Smith", "abc123", "200.00"))

# ... Existing code continues ...
