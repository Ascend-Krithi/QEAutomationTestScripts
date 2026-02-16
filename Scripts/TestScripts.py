import necessary modules

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
        await self.login_page.fill_email(''

class TestBillPayFunctionality:
    def __init__(self, page):
        self.page = page
        self.bill_pay_page = BillPayPage(page)

    async def test_bill_pay_electric_company(self):
        # TC-BP-001: Navigate to Bill Pay, enter valid details for Electric Company, submit, confirm
        await self.bill_pay_page.navigate_to_bill_pay()
        await self.bill_pay_page.enter_payee_details(
            payee_name='Electric Company',
            address='123 Main St',
            city='Springfield',
            state='IL',
            zip_code='62701',
            phone='555-123-4567',
            account='12345',
            verify_account='12345',
            amount='150.00',
            from_account='13344'
        )
        await self.bill_pay_page.submit_payment()
        confirmation = await self.bill_pay_page.confirm_payment()
        assert confirmation is True

    async def test_bill_pay_water_utility(self):
        # TC-BP-002: Navigate to Bill Pay, enter valid details for Water Utility, minimum amount 0.01, submit, confirm
        await self.bill_pay_page.navigate_to_bill_pay()
        await self.bill_pay_page.enter_payee_details(
            payee_name='Water Utility',
            address='456 Oak Ave',
            city='Chicago',
            state='IL',
            zip_code='60601',
            phone='555-987-6543',
            account='67890',
            verify_account='67890',
            amount='0.01',
            from_account='13344'
        )
        await self.bill_pay_page.submit_payment()
        confirmation = await self.bill_pay_page.confirm_payment()
        assert confirmation is True
