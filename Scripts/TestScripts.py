Import necessary modules

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
        await self.login_page.fill_email('

    # --- Appended methods for TC-BP-001 and TC-BP-002 ---

    async def test_bill_pay_electric_company(self):
        """
        TC-BP-001: Steps for bill pay including navigation, form filling, and payment confirmation for Electric Company.
        """
        bill_pay_page = BillPayPage(self.page)
        await bill_pay_page.navigate()
        await bill_pay_page.select_payee('Electric Company')
        await bill_pay_page.fill_account_number('123456789')
        await bill_pay_page.fill_amount('150.00')
        await bill_pay_page.submit_payment()
        confirmation = await bill_pay_page.get_confirmation_message()
        assert confirmation == 'Payment to Electric Company successful'

    async def test_bill_pay_water_utility_minimum(self):
        """
        TC-BP-002: Steps for bill pay with minimum amount and confirmation for Water Utility.
        """
        bill_pay_page = BillPayPage(self.page)
        await bill_pay_page.navigate()
        await bill_pay_page.select_payee('Water Utility')
        await bill_pay_page.fill_account_number('987654321')
        await bill_pay_page.fill_amount('25.00')
        await bill_pay_page.submit_payment()
        confirmation = await bill_pay_page.get_confirmation_message()
        assert confirmation == 'Payment to Water Utility successful'
