{Import necessary modules}

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

class TestParabankBillPay:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.bill_pay_page = BillPayPage(page)
        self.transactions_page = TransactionsPage(page)

    async def test_successful_bill_payment_and_transaction_history(self):
        # TC-SCRUM-15483-001
        # Step 1: Navigate to Parabank login page
        await self.login_page.navigate()
        # Step 2: Log in with valid credentials
        await self.login_page.submit_login('valid_user', 'valid_password')
        assert await self.dashboard_page.is_loaded()
        # Step 3: Navigate to Bill Pay page
        await self.dashboard_page.go_to_bill_pay()
        assert await self.bill_pay_page.is_loaded()
        # Step 4: Fill out bill pay form with valid data and submit
        await self.bill_pay_page.fill_payee_information(
            payee_name="John Doe",
            address="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-1234",
            account="987654321",
            verify_account="987654321",
            amount="100.00",
            from_account="123456789"
        )
        await self.bill_pay_page.submit_payment()
        # Step 5: Verify payment confirmation is displayed
        assert await self.bill_pay_page.is_payment_confirmed()
        # Step 6: Navigate to transaction history
        await self.dashboard_page.go_to_transactions()
        assert await self.transactions_page.is_loaded()
        # Step 7: Verify the new transaction appears in the list
        transaction_found = await self.transactions_page.find_transaction(
            description="Bill Payment to John Doe",
            amount="100.00"
        )
        assert transaction_found

    async def test_insufficient_funds_bill_payment(self):
        # TC-SCRUM-15483-002
        # Step 1: Navigate to Parabank login page
        await self.login_page.navigate()
        # Step 2: Log in with valid credentials
        await self.login_page.submit_login('valid_user', 'valid_password')
        assert await self.dashboard_page.is_loaded()
        # Step 3: Navigate to Bill Pay page
        await self.dashboard_page.go_to_bill_pay()
        assert await self.bill_pay_page.is_loaded()
        # Step 4: Fill out bill pay form with amount greater than balance and submit
        await self.bill_pay_page.fill_payee_information(
            payee_name="Jane Smith",
            address="456 Elm St",
            city="Springfield",
            state="IL",
            zip_code="62701",
            phone="555-5678",
            account="123123123",
            verify_account="123123123",
            amount="1000000.00",  # Exceeds available balance
            from_account="123456789"
        )
        await self.bill_pay_page.submit_payment()
        # Step 5: Verify insufficient funds error is displayed
        error_message = await self.bill_pay_page.get_error_message()
        assert "Insufficient funds" in error_message
        # Step 6: Navigate to transaction history
        await self.dashboard_page.go_to_transactions()
        assert await self.transactions_page.is_loaded()
        # Step 7: Verify no transaction for the failed payment is recorded
        transaction_found = await self.transactions_page.find_transaction(
            description="Bill Payment to Jane Smith",
            amount="1000000.00"
        )
        assert not transaction_found
