from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TransactionPage:
    """
    Page Object for simulating deposits and checking rule execution.
    Designed for test case TC-FT-003.
    """
    def __init__(self, driver):
        self.driver = driver
        self.balance_field = (By.ID, 'account-balance')
        self.deposit_field = (By.ID, 'deposit-amount')
        self.source_field = (By.ID, 'deposit-source')
        self.deposit_button = (By.ID, 'deposit-submit')
        self.transfer_status = (By.CSS_SELECTOR, 'div.transfer-status')
        self.transfer_amount_field = (By.ID, 'transfer-amount')  # Added for transfer amount check

    def simulate_deposit(self, balance, deposit, source):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.balance_field)).clear()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.balance_field)).send_keys(str(balance))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.deposit_field)).send_keys(str(deposit))
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.source_field)).send_keys(source)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.deposit_button)).click()

    def get_transfer_status(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.transfer_status)).text
        except:
            return None

    def verify_percentage_transfer(self, deposit, expected_percentage):
        # Verifies that the transfer amount is correct
        try:
            transfer_amount = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.transfer_amount_field)).text
            expected_amount = deposit * expected_percentage / 100
            return float(transfer_amount) == expected_amount
        except:
            return False
