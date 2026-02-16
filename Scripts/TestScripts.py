# Import necessary modules
from BillPayPage import BillPayPage

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
        await self.login_page.fill_email('')

class TestBillPayFunctionality:
    def __init__(self, driver):
        self.bill_pay_page = BillPayPage(driver)

    def test_tc_bp_001(self):
        # Step 2: Navigate to Bill Pay section
        self.bill_pay_page.navigate_to_bill_pay()
        # Step 3: Enter valid payee name
        self.bill_pay_page.fill_payee_information(
            name="Electric Company",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-123-4567"
        )
        # Step 6: Enter account number and verify
        self.bill_pay_page.fill_account_details("12345", "12345")
        # Step 7: Enter payment amount
        self.bill_pay_page.enter_amount(150.00)
        # Step 8: Select source account
        self.bill_pay_page.select_from_account("13344")
        # Step 9: Click Send Payment and verify confirmation
        self.bill_pay_page.submit_payment()
        assert self.bill_pay_page.verify_payment_success()
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation['payee_name'] == "Electric Company"
        assert confirmation['amount'] == "$150.00"
        assert confirmation['from_account'] == "13344"

    def test_tc_bp_002(self):
        # Step 2: Navigate to Bill Pay section
        self.bill_pay_page.navigate_to_bill_pay()
        # Step 3: Fill all mandatory fields
        self.bill_pay_page.fill_payee_information(
            name="Water Utility",
            address="456 Oak Ave",
            city="Chicago",
            state="IL",
            zip_code="60601",
            phone="555-987-6543"
        )
        # Step 6: Enter account number and verify
        self.bill_pay_page.fill_account_details("67890", "67890")
        # Step 4: Enter minimum amount
        self.bill_pay_page.enter_amount(0.01)
        # Step 5: Select account
        self.bill_pay_page.select_from_account("13344")
        # Step 6: Submit payment and verify confirmation
        self.bill_pay_page.submit_payment()
        assert self.bill_pay_page.verify_payment_success()
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation['payee_name'] == "Water Utility"
        assert confirmation['amount'] == "$0.01"
        assert confirmation['from_account'] == "13344"
