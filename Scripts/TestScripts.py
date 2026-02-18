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

    async def test_account_numbers_mismatch(self):
        # TC-SCRUM-15483-003: Enter valid payee details, enter mismatched account and verify account, submit, expect error.
        await self.login_page.navigate()
        await self.login_page.submit_login('valid_user', 'valid_password')
        assert await self.account_overview_page.is_displayed()
        await self.bill_pay_page.navigate()
        await self.bill_pay_page.enter_payee_name('Electric Company')
        await self.bill_pay_page.enter_address('123 Main St')
        await self.bill_pay_page.enter_city('NY')
        await self.bill_pay_page.enter_state('NY')
        await self.bill_pay_page.enter_zip_code('10001')
        await self.bill_pay_page.enter_phone_number('555-1234567')
        await self.bill_pay_page.enter_account_number('123456789')
        await self.bill_pay_page.enter_verify_account_number('987654321')
        await self.bill_pay_page.enter_amount('50.00')
        await self.bill_pay_page.select_from_account('Account with sufficient balance')
        await self.bill_pay_page.click_send_payment()
        error_message = await self.bill_pay_page.get_success_message()
        assert 'account numbers don\'t match' in error_message.lower() or 'error' in error_message.lower()
        assert await self.bill_pay_page.is_on_bill_pay_page()

    async def test_mandatory_field_validation(self):
        # TC-SCRUM-15483-004: Leave each mandatory field empty one at a time, submit, expect error and highlight.
        mandatory_fields = [
            ('payee_name', ''),
            ('address', '123 Main St'),
            ('city', 'NY'),
            ('state', 'NY'),
            ('zip_code', '10001'),
            ('phone_number', '555-1234567'),
            ('account_number', '987654321'),
            ('amount', '50.00')
        ]
        for i, (field, value) in enumerate(mandatory_fields):
            await self.login_page.navigate()
            await self.login_page.submit_login('valid_user', 'valid_password')
            assert await self.account_overview_page.is_displayed()
            await self.bill_pay_page.navigate()
            # Fill all fields with valid data
            if field != 'payee_name': await self.bill_pay_page.enter_payee_name('Electric Company')
            else: await self.bill_pay_page.enter_payee_name('')
            if field != 'address': await self.bill_pay_page.enter_address('123 Main St')
            else: await self.bill_pay_page.enter_address('')
            if field != 'city': await self.bill_pay_page.enter_city('NY')
            else: await self.bill_pay_page.enter_city('')
            if field != 'state': await self.bill_pay_page.enter_state('NY')
            else: await self.bill_pay_page.enter_state('')
            if field != 'zip_code': await self.bill_pay_page.enter_zip_code('10001')
            else: await self.bill_pay_page.enter_zip_code('')
            if field != 'phone_number': await self.bill_pay_page.enter_phone_number('555-1234567')
            else: await self.bill_pay_page.enter_phone_number('')
            if field != 'account_number': await self.bill_pay_page.enter_account_number('987654321')
            else: await self.bill_pay_page.enter_account_number('')
            await self.bill_pay_page.enter_verify_account_number('987654321')
            if field != 'amount': await self.bill_pay_page.enter_amount('50.00')
            else: await self.bill_pay_page.enter_amount('')
            await self.bill_pay_page.select_from_account('Account with sufficient balance')
            await self.bill_pay_page.click_send_payment()
            error_message = await self.bill_pay_page.get_success_message()
            assert 'required' in error_message.lower() or 'error' in error_message.lower()
            # Check highlight
            locator_map = {
                'payee_name': BillPayPage.PAYEE_NAME,
                'address': BillPayPage.ADDRESS,
                'city': BillPayPage.CITY,
                'state': BillPayPage.STATE,
                'zip_code': BillPayPage.ZIP_CODE,
                'phone_number': BillPayPage.PHONE_NUMBER,
                'account_number': BillPayPage.ACCOUNT_NUMBER,
                'amount': BillPayPage.AMOUNT
            }
            assert self.bill_pay_page.is_field_highlighted(locator_map[field])
            assert await self.bill_pay_page.is_on_bill_pay_page()
