# Scripts/TestScripts.py
import unittest
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.LoginPage import LoginPage

class TestFinancialTransfer(unittest.TestCase):
    def setUp(self):
        # Setup code for WebDriver, e.g. Chrome
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        # Optionally login if needed
        # ...
        self.page = FinancialTransferPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods remain unchanged

    def test_valid_financial_transfer_TC15801(self):
        """
        TC-158-01: Valid transfer, all fields present, expect success.
        """
        payload = {
            "amount": 1000.0,
            "currency": "USD",
            "source": "AccountA",
            "destination": "AccountB",
            "timestamp": "2024-06-18T12:34:56Z"
        }
        self.page.open_transfer_dialog()
        self.page.enter_transfer_payload(json.dumps(payload))
        self.page.submit_transfer()
        # Wait for success message
        success_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "transfer-success-message"))
        )
        self.assertIn("Transfer successful", success_msg.text)

    def test_missing_destination_financial_transfer_TC15802(self):
        """
        TC-158-02: Missing 'destination', expect error mentioning 'destination'.
        """
        payload = {
            "amount": 1000.0,
            "currency": "USD",
            "source": "AccountA",
            # 'destination' omitted
            "timestamp": "2024-06-18T12:34:56Z"
        }
        self.page.open_transfer_dialog()
        self.page.enter_transfer_payload(json.dumps(payload))
        self.page.submit_transfer()
        # Wait for error message
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "transfer-error-message"))
        )
        self.assertIn("destination", error_msg.text.lower())


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        from selenium import webdriver
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_special_character_input_validation_TC09(self):
        """
        TC09: Enter special characters in username and password, click login, assert dashboard is shown or correct error message is displayed.
        """
        username = "user!@#"
        password = "pass$%^&*"
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        try:
            dashboard = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "dashboard"))
            )
            self.assertTrue(dashboard.is_displayed())
        except Exception:
            error_msg = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "login-error-message"))
            )
            self.assertTrue(
                "invalid" in error_msg.text.lower() or "not allowed" in error_msg.text.lower() or "error" in error_msg.text.lower()
            )

    def test_network_server_error_simulation_TC10(self):
        """
        TC10: Enter valid credentials, simulate network failure during login, assert error message is displayed and login fails.
        """
        username = "valid_user"
        password = "ValidPass123"
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        # Simulate network failure (e.g., disable network using Chrome DevTools or mock)
        # For demonstration, we'll execute JS to offline mode if possible
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
                "offline": True,
                "latency": 0,
                "downloadThroughput": 0,
                "uploadThroughput": 0
            })
        except Exception:
            pass  # If not supported, skip
        self.login_page.click_login()
        error_msg = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-error-message"))
        )
        self.assertIn("unable to connect", error_msg.text.lower())
        # Optionally, check login did not succeed
        self.assertFalse(
            len(self.driver.find_elements(By.ID, "dashboard")) > 0
        )
