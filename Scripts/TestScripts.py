import pytest
from Pages.LoginPage import LoginPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountOverviewPage import AccountOverviewPage

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
        await self.login_page.fill_email('...')  # Existing code continues here

class TestBillPayEndToEnd:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.account_overview_page = AccountOverviewPage(page)
        self.bill_pay_page = BillPayPage(page)

    async def test_pay_bill_success(self):
        # TC-SCRUM-15483-001: Login, verify account overview, pay bill with valid data, confirm payment.
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('valid_user', 'valid_password')
        assert await self.account_overview_page.is_displayed()

        # Step 2: Pay bill with valid data
        await self.bill_pay_page.navigate()
        await self.bill_pay_page.fill_bill_pay_form(
            payee_name='John Doe',
            address='123 Main St',
            city='Springfield',
            state='IL',
            zip_code='62704',
            phone='555-1234',
            account='987654321',
            verify_account='987654321',
            amount='100.00',
            from_account='123456789'
        )
        await self.bill_pay_page.submit_payment()
        confirmation = await self.bill_pay_page.get_confirmation()
        assert 'Payment Complete' in confirmation

    async def test_pay_bill_insufficient_funds(self):
        # TC-SCRUM-15483-002: Attempt bill pay with amount greater than balance, expect error.
        # Step 1: Login
        await self.login_page.navigate()
        await self.login_page.submit_login('valid_user', 'valid_password')
        assert await self.account_overview_page.is_displayed()

        # Step 2: Attempt to pay bill with excessive amount
        await self.bill_pay_page.navigate()
        await self.bill_pay_page.fill_bill_pay_form(
            payee_name='Acme Corp',
            address='456 Commerce Blvd',
            city='Metropolis',
            state='NY',
            zip_code='10001',
            phone='555-6789',
            account='123123123',
            verify_account='123123123',
            amount='1000000.00',  # Exceeds balance
            from_account='123456789'
        )
        await self.bill_pay_page.submit_payment()
        error_message = await self.bill_pay_page.get_error_message()
        assert error_message == 'Insufficient funds'
