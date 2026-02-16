# BillPayPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    """
    Page Object for Bill Pay functionality. Handles form filling, submission, and confirmation verification.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Locators from Locators.json
        self.locators = {
            'payeeName': (By.NAME, 'payee.name'),
            'address': (By.NAME, 'payee.address.street'),
            'city': (By.NAME, 'payee.address.city'),
            'state': (By.NAME, 'payee.address.state'),
            'zipCode': (By.NAME, 'payee.address.zipCode'),
            'phoneNumber': (By.NAME, 'payee.phoneNumber'),
            'accountNumber': (By.NAME, 'payee.accountNumber'),
            'verifyAccountNumber': (By.NAME, 'verifyAccount'),
            'amount': (By.NAME, 'amount'),
            'fromAccountId': (By.NAME, 'fromAccountId'),
            'sendPaymentButton': (By.CSS_SELECTOR, "input[value='Send Payment']"),
            'successMessage': (By.ID, 'billpayResult'),
            'confPayeeName': (By.ID, 'payeeName'),
            'confAmount': (By.ID, 'amount'),
            'confFromAccount': (By.ID, 'fromAccountId')
        }

    def fill_bill_pay_form(self, payee_name, address, city, state, zip_code, phone, account, verify_account, amount, from_account):
        """Fill the Bill Pay form with the provided details."""
        self.wait.until(EC.visibility_of_element_located(self.locators['payeeName'])).send_keys(payee_name)
        self.driver.find_element(*self.locators['address']).send_keys(address)
        self.driver.find_element(*self.locators['city']).send_keys(city)
        self.driver.find_element(*self.locators['state']).send_keys(state)
        self.driver.find_element(*self.locators['zipCode']).send_keys(zip_code)
        self.driver.find_element(*self.locators['phoneNumber']).send_keys(phone)
        self.driver.find_element(*self.locators['accountNumber']).send_keys(account)
        self.driver.find_element(*self.locators['verifyAccountNumber']).send_keys(verify_account)
        self.driver.find_element(*self.locators['amount']).send_keys(amount)
        from_account_dropdown = self.driver.find_element(*self.locators['fromAccountId'])
        from_account_dropdown.send_keys(from_account)

    def submit_payment(self):
        """Click Send Payment button to submit the form."""
        self.driver.find_element(*self.locators['sendPaymentButton']).click()

    def verify_confirmation(self, expected_payee, expected_amount, expected_account):
        """Verify confirmation page details after payment submission."""
        self.wait.until(EC.visibility_of_element_located(self.locators['successMessage']))
        actual_payee = self.driver.find_element(*self.locators['confPayeeName']).text
        actual_amount = self.driver.find_element(*self.locators['confAmount']).text
        actual_account = self.driver.find_element(*self.locators['confFromAccount']).text
        assert expected_payee in actual_payee, f"Expected payee {expected_payee} not found."
        assert expected_amount in actual_amount, f"Expected amount {expected_amount} not found."
        assert expected_account in actual_account, f"Expected account {expected_account} not found."
