# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from Pages.LoginPage import LoginPage
from Pages.Navigation import Navigation
from Pages.AccountOverviewPage import AccountOverviewPage
from Pages.BillPayPage import BillPayPage
from Pages.AccountActivityPage import AccountActivityPage
from Pages.ProfilePage import ProfilePage

class TestLoginAndBillPay:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.navigation = Navigation(driver)
        self.account_overview_page = AccountOverviewPage(driver)
        self.bill_pay_page = BillPayPage(driver)
        self.account_activity_page = AccountActivityPage(driver)
        self.profile_page = ProfilePage(driver)

    def test_TC_SCRUM_15483_001(self):
        # Step 2: Navigate to Parabank login page
        url = "https://parabank.parasoft.com"
        self.login_page.navigate_to_login_page(url)
        assert self.login_page.is_login_page_displayed(), "Login page is not displayed"

        # Step 3: Enter valid username and password
        self.login_page.enter_username("testuser")
        self.login_page.enter_password("testpass")

        # Step 4: Click Login button
        self.login_page.click_login_button()
        # Step 5: Verify Account Overview page is displayed
        assert self.account_overview_page.is_at_account_overview(), "Account Overview page not displayed"

        # Step 6: Click Bill Pay in navigation menu
        self.navigation.navigate_to_bill_pay()
        # Step 7: Enter valid payee details
        payee_details = {
            "name": "Electric Company",
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "phone": "555-1234",
            "account": "987654321",
            "verify_account": "987654321"
        }
        self.bill_pay_page.enter_payee_details(payee_details)
        # Step 8: Enter payment amount
        self.bill_pay_page.enter_amount(150.00)
        # Step 9: Select source account
        self.bill_pay_page.select_from_account("123456789")  # Placeholder account ID
        # Step 10: Click Send Payment
        self.bill_pay_page.submit_payment()
        # Step 11: Verify payment confirmation message
        assert self.bill_pay_page.is_payment_confirmed(), "Payment confirmation not displayed"
        confirmation = self.bill_pay_page.get_confirmation_details()
        assert confirmation["payee_name"] == "Electric Company"
        assert confirmation["amount"] == "150.00"
        assert confirmation["from_account"] == "123456789"

        # Step 12: Navigate to Account Activity
        self.navigation.navigate_to_account_activity()
        assert self.account_activity_page.is_account_activity_displayed(), "Account Activity page not displayed"
        # Step 13: Verify transaction appears in transaction history
        transaction_text = self.account_activity_page.get_latest_transaction()
        assert "Electric Company" in transaction_text and "150.00" in transaction_text, "Transaction not recorded correctly"

    def test_TC_SCRUM_15483_002(self):
        # Step 2: Login and navigate to Bill Pay page
        url = "https://parabank.parasoft.com"
        self.login_page.navigate_to_login_page(url)
        self.login_page.enter_username("testuser")
        self.login_page.enter_password("testpass")
        self.login_page.click_login_button()
        self.navigation.navigate_to_bill_pay()
        # Step 3: Enter valid payee information
        payee_details = {
            "name": "Electric Company",
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "phone": "555-1234",
            "account": "987654321",
            "verify_account": "987654321"
        }
        self.bill_pay_page.enter_payee_details(payee_details)
        # Step 4: Enter payment amount greater than account balance
        self.bill_pay_page.enter_amount(10000.00)
        # Step 5: Select account with insufficient funds
        self.bill_pay_page.select_from_account("987654321")  # Placeholder for insufficient funds
        # Step 6: Click Send Payment
        self.bill_pay_page.submit_payment()
        # Step 6/7: System should display error message
        # Placeholder: Error message validation
        error_displayed = not self.bill_pay_page.is_payment_confirmed()
        assert error_displayed, "Insufficient funds error not displayed"
        # Step 7: Verify payment is not processed and balance unchanged
        self.navigation.navigate_to_account_activity()
        assert self.account_activity_page.is_account_activity_displayed(), "Account Activity page not displayed"
        transaction_text = self.account_activity_page.get_latest_transaction()
        assert "10000.00" not in transaction_text, "Transaction should not be recorded"
