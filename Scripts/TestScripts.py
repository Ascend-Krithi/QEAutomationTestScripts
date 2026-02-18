import pytest
from Pages.LoginPage import LoginPage
from Pages.Navigation import Navigation
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('testuser@example.com')
        await self.login_page.fill_password('password123')
        await self.login_page.toggle_remember_me(True)
        await self.login_page.submit_login('testuser@example.com', 'password123')
        # Further assertions would go here

class TestBillPay:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.navigation = Navigation(page)
        self.bill_pay_page = BillPayPage(page)
        self.account_activity_page = AccountActivityPage(page)

    async def test_successful_bill_pay_and_transaction_verification(self):
        """
        TC-SCRUM-15483-001: Valid login, Bill Pay with valid details, verify confirmation and transaction history.
        """
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('john_demo', 'demo_password1!')
        assert await self.navigation.is_logged_in()

        # Step 2: Navigate to Bill Pay
        await self.navigation.go_to_bill_pay()

        # Step 3: Fill Bill Pay form with valid details
        await self.bill_pay_page.enter_payee_name('Acme Utilities')
        await self.bill_pay_page.enter_address('123 Elm St')
        await self.bill_pay_page.enter_city('Metropolis')
        await self.bill_pay_page.enter_state('NY')
        await self.bill_pay_page.enter_zip_code('10001')
        await self.bill_pay_page.enter_phone('1234567890')
        await self.bill_pay_page.enter_account_number('987654321')
        await self.bill_pay_page.enter_verify_account('987654321')
        await self.bill_pay_page.enter_amount('50.00')
        await self.bill_pay_page.select_from_account('12345')
        await self.bill_pay_page.submit_payment()

        # Step 4: Verify confirmation message
        confirmation = await self.bill_pay_page.get_confirmation_message()
        assert 'Bill Payment Complete' in confirmation

        # Step 5: Go to Account Activity and verify transaction
        await self.navigation.go_to_account_activity()
        transactions = await self.account_activity_page.get_recent_transactions()
        found = False
        for txn in transactions:
            if txn['description'] == 'Bill Payment to Acme Utilities' and txn['amount'] == '-50.00':
                found = True
                break
        assert found, 'Transaction for Bill Payment not found in activity.'

    async def test_bill_pay_insufficient_funds(self):
        """
        TC-SCRUM-15483-002: Valid login, Bill Pay with insufficient funds, expect error and no transaction.
        """
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('john_demo', 'demo_password1!')
        assert await self.navigation.is_logged_in()

        # Step 2: Navigate to Bill Pay
        await self.navigation.go_to_bill_pay()

        # Step 3: Fill Bill Pay form with amount greater than balance
        await self.bill_pay_page.enter_payee_name('Acme Utilities')
        await self.bill_pay_page.enter_address('123 Elm St')
        await self.bill_pay_page.enter_city('Metropolis')
        await self.bill_pay_page.enter_state('NY')
        await self.bill_pay_page.enter_zip_code('10001')
        await self.bill_pay_page.enter_phone('1234567890')
        await self.bill_pay_page.enter_account_number('987654321')
        await self.bill_pay_page.enter_verify_account('987654321')
        await self.bill_pay_page.enter_amount('100000.00')  # Exceeds available balance
        await self.bill_pay_page.select_from_account('12345')
        await self.bill_pay_page.submit_payment()

        # Step 4: Verify error message
        error_msg = await self.bill_pay_page.get_error_message()
        assert 'Insufficient funds' in error_msg

        # Step 5: Go to Account Activity and verify no such transaction
        await self.navigation.go_to_account_activity()
        transactions = await self.account_activity_page.get_recent_transactions()
        for txn in transactions:
            assert not (txn['description'] == 'Bill Payment to Acme Utilities' and txn['amount'] == '-100000.00'), 'Erroneous transaction found despite insufficient funds.'
