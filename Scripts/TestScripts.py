# BillPay Test Scripts
from Pages.BillPayPage import BillPayPage
from selenium import webdriver
import pytest

# Existing content from fetched TestScripts.py would be here...

class TestBillPay:
    @pytest.fixture(scope='function')
    def driver(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    @pytest.fixture(scope='function')
    def bill_pay_page(self, driver):
        return BillPayPage(driver)

    def test_tc_bp_001(self, bill_pay_page):
        """Test Case TC-BP-001: Valid Bill Pay workflow for Electric Company"""
        bill_pay_page.navigate_to_bill_pay()
        bill_pay_page.complete_bill_payment(
            payee_name='Electric Company',
            address='123 Main St',
            city='Springfield',
            state='IL',
            zip_code='62701',
            phone_number='555-123-4567',
            account_number='12345',
            verify_account_number='12345',
            amount='150.00',
            from_account_id='13344'
        )
        bill_pay_page.verify_confirmation(
            expected_payee='Electric Company',
            expected_amount='150.00',
            expected_from_account='13344'
        )

    def test_tc_bp_002(self, bill_pay_page):
        """Test Case TC-BP-002: Minimum amount Bill Pay for Water Utility"""
        bill_pay_page.navigate_to_bill_pay()
        bill_pay_page.complete_bill_payment(
            payee_name='Water Utility',
            address='456 Oak Ave',
            city='Chicago',
            state='IL',
            zip_code='60601',
            phone_number='555-987-6543',
            account_number='67890',
            verify_account_number='67890',
            amount='0.01',
            from_account_id='13344'
        )
        bill_pay_page.verify_confirmation(
            expected_payee='Water Utility',
            expected_amount='0.01',
            expected_from_account='13344'
        )
