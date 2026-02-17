import pytest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        # Add assertion for error message

    def test_remember_me_functionality(self):
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        # Add assertion for remember me

class TestBillPay:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)

    def test_TC_SCRUM_15483_001(self):
        # Step 2: Navigate to login page
        self.driver.get('https://parabank.parasoft.com')
        # Step 3: Enter valid username and password
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        # Step 4: Click Login button
        self.login_page.click_login()
        # Step 5: Verify Account Overview page is displayed
        # Add assertion for Account Overview
        # Step 6: Click Bill Pay in navigation
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 7: Enter valid payee details
        self.bill_pay_page.enter_payee_name('Electric Company')
        self.bill_pay_page.enter_account('987654321')
        # Step 8: Enter payment amount
        self.bill_pay_page.enter_amount('150.00')
        # Step 9: Select source account (handled above)
        # Step 10: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 11: Verify payment confirmation message
        assert self.bill_pay_page.is_payment_successful()
        # Step 12: Navigate to Account Activity
        self.driver.get('https://parabank.parasoft.com/accountactivity.htm')
        # Step 13: Verify transaction appears in history
        assert self.account_activity_page.verify_transaction('Electric Company', '150.00')

    def test_TC_SCRUM_15483_002(self):
        # Step 2: Login and navigate to Bill Pay page
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 3: Enter valid payee information
        self.bill_pay_page.enter_payee_name('Electric Company')
        self.bill_pay_page.enter_account('987654321')
        # Step 4: Enter payment amount greater than balance
        self.bill_pay_page.enter_amount('10000')
        # Step 5: Select account with insufficient funds
        # Step 6: Click Send Payment button
        self.bill_pay_page.click_send_payment()
        # Step 6: System displays error message: Insufficient funds
        # Add assertion for error
        # Step 7: Verify payment is not processed and balance unchanged
        # Add assertion for no transaction

    def test_empty_bill_pay_fields_validation(self):
        """
        Test negative flow: Attempt bill pay with empty fields, expect validation errors.
        """
        # Step 1: Login
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        # Step 2: Navigate to Bill Pay
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 3: Leave all fields empty and attempt payment
        self.bill_pay_page.fill_payee_info('', '', '', '', '', '')
        self.bill_pay_page.fill_account_info('', '')
        self.bill_pay_page.fill_payment_amount('')
        # Not selecting from_account
        self.bill_pay_page.click_send_payment()
        # Step 4: Assert validation error is shown (example: error message element exists)
        try:
            error_elem = self.driver.find_element_by_css_selector('.error')
            assert error_elem.is_displayed(), 'Validation error not displayed for empty fields.'
        except Exception:
            assert False, 'Validation error not displayed for empty fields.'

    def test_insufficient_funds_bill_pay(self):
        """
        Test negative flow: Attempt bill pay with amount greater than balance, expect insufficient funds error.
        """
        # Step 1: Login
        self.driver.get('https://parabank.parasoft.com')
        self.login_page.enter_username('testuser')
        self.login_page.enter_password('testpass')
        self.login_page.click_login()
        # Step 2: Navigate to Bill Pay
        self.driver.get('https://parabank.parasoft.com/billpay.htm')
        # Step 3: Fill payee info
        self.bill_pay_page.fill_payee_info('Electric Company', '123 Main St', 'Metropolis', 'CA', '90210', '5551234567')
        self.bill_pay_page.fill_account_info('987654321', '987654321')
        self.bill_pay_page.fill_payment_amount('10000')
        # Step 4: Select from account (simulate insufficient funds)
        self.bill_pay_page.select_from_account('12345')  # Assuming '12345' is insufficient
        # Step 5: Click Send Payment
        self.bill_pay_page.click_send_payment()
        # Step 6: Assert insufficient funds error is shown
        try:
            error_elem = self.driver.find_element_by_xpath("//*[contains(text(), 'Insufficient funds')]")
            assert error_elem.is_displayed(), 'Insufficient funds error not displayed.'
        except Exception:
            assert False, 'Insufficient funds error not displayed.'
        # Step 7: Navigate to Account Activity and verify no new transaction
        self.driver.get('https://parabank.parasoft.com/accountactivity.htm')
        assert not self.account_activity_page.verify_transaction('Electric Company', '10000'), 'Transaction should not appear for insufficient funds.'
