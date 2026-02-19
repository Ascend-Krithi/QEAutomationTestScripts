# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage
from selenium import webdriver

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.enter_username('')
        self.login_page.enter_password('')
        self.login_page.click_login()
        # assert error message (requires implementation)

    def test_remember_me_functionality(self):
        self.login_page.enter_username('testuser123')
        self.login_page.enter_password('Pass@1234')
        self.login_page.click_login()
        # assert login success (requires implementation)

class TestBillPay:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)

    def test_TC001_pay_bill(self):
        # Step 2: Login
        self.login_page.enter_username('testuser123')
        self.login_page.enter_password('Pass@1234')
        self.login_page.click_login()
        # Step 3: Navigate to Bill Pay (assume navigation handled)
        # Step 4: Enter payee information
        self.bill_pay_page.enter_payee_name('Electric Power Company')
        self.bill_pay_page.enter_address('123 Main Street')
        self.bill_pay_page.enter_city('Springfield')
        self.bill_pay_page.enter_state('IL')
        self.bill_pay_page.enter_zip_code('62701')
        self.bill_pay_page.enter_phone_number('555-0123')
        self.bill_pay_page.enter_account_number('987654321')
        self.bill_pay_page.enter_verify_account_number('987654321')
        # Step 5: Select From Account
        self.bill_pay_page.select_from_account('Savings Account #12345')
        # Step 6: Enter payment amount
        self.bill_pay_page.enter_amount('150.00')
        # Step 7: Send payment
        self.bill_pay_page.click_send_payment()
        # Step 7: Assert confirmation
        assert self.bill_pay_page.get_confirmation_payee_name() == 'Electric Power Company'
        assert self.bill_pay_page.get_confirmation_amount() == '150.00'
        assert self.bill_pay_page.get_confirmation_from_account() == 'Savings Account #12345'
        # Step 8: Navigate to Account Activity
        # Step 9: Assert transaction
        transaction_details = self.account_activity_page.get_latest_transaction_details()
        assert 'Electric Power Company' in transaction_details
        assert '150.00' in transaction_details

    def test_TC002_minimum_payment(self):
        # Step 2: Login and navigate to Bill Pay
        self.login_page.enter_username('testuser123')
        self.login_page.enter_password('Pass@1234')
        self.login_page.click_login()
        # Step 3: Enter payee information
        self.bill_pay_page.enter_payee_name('Electric Power Company')
        self.bill_pay_page.enter_address('123 Main Street')
        self.bill_pay_page.enter_city('Springfield')
        self.bill_pay_page.enter_state('IL')
        self.bill_pay_page.enter_zip_code('62701')
        self.bill_pay_page.enter_phone_number('555-0123')
        self.bill_pay_page.enter_account_number('987654321')
        self.bill_pay_page.enter_verify_account_number('987654321')
        # Step 4: Select From Account & enter minimum payment
        self.bill_pay_page.select_from_account('Savings Account #12345')
        self.bill_pay_page.enter_amount('0.01')
        # Step 5: Send payment
        self.bill_pay_page.click_send_payment()
        # Step 5: Assert confirmation
        assert self.bill_pay_page.get_confirmation_payee_name() == 'Electric Power Company'
        assert self.bill_pay_page.get_confirmation_amount() == '0.01'
        assert self.bill_pay_page.get_confirmation_from_account() == 'Savings Account #12345'