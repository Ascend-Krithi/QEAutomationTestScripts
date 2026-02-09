# TransactionPage.py
"""
Page Object for Transaction Page.

This class encapsulates UI elements and actions for transaction operations, including triggers and actions relevant to rules (fixed_amount, percentage_of_deposit, after_deposit).

Features:
- Locators mapped from Locators.json and test case requirements.
- Methods for performing and validating transactions, including triggering rules by deposit.
- Comprehensive docstrings for downstream automation.
- Strict code integrity and structure for enterprise usage.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TransactionPage:
    """
    Page Object Model for Transaction Page.
    """
    URL = "https://example-ecommerce.com/transactions"

    NEW_TRANSACTION_BUTTON = (By.ID, "new-transaction-btn")
    AMOUNT_FIELD = (By.ID, "transaction-amount-input")
    TYPE_DROPDOWN = (By.ID, "transaction-type-dropdown")
    PERCENTAGE_FIELD = (By.ID, "transaction-percentage-input")
    SUBMIT_BUTTON = (By.ID, "submit-transaction-btn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    TRANSACTION_LIST = (By.CSS_SELECTOR, "ul.transaction-list")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def perform_transaction(self, transaction_data: dict):
        """
        Perform a new transaction with provided data.
        Args:
            transaction_data (dict): {'amount', 'type', 'percentage'}
        """
        self.wait.until(EC.element_to_be_clickable(self.NEW_TRANSACTION_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.AMOUNT_FIELD)).send_keys(str(transaction_data['amount']))
        self.wait.until(EC.element_to_be_clickable(self.TYPE_DROPDOWN)).click()
        self.select_dropdown_option(self.TYPE_DROPDOWN, transaction_data['type'])
        if 'percentage' in transaction_data:
            self.wait.until(EC.visibility_of_element_located(self.PERCENTAGE_FIELD)).send_keys(str(transaction_data['percentage']))
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()

    def select_dropdown_option(self, dropdown_locator, option_text):
        dropdown = self.wait.until(EC.visibility_of_element_located(dropdown_locator))
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()
                break

    def is_transaction_successful(self) -> bool:
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return True
        except:
            return False

    def get_transaction_list(self) -> list:
        transaction_list = self.wait.until(EC.visibility_of_element_located(self.TRANSACTION_LIST))
        return [item.text for item in transaction_list.find_elements_by_tag_name('li')]

    def trigger_rule(self, deposit_amount):
        """
        Trigger rule execution by performing a deposit transaction.
        """
        self.perform_transaction({'amount': deposit_amount, 'type': 'deposit'})
        return self.is_transaction_successful()

    # Additional methods for transaction validation can be added as required by future test cases.