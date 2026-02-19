# Pages/AccountActivityPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transaction_table = (By.ID, 'transactionTable')
        self.latest_transaction = (By.CSS_SELECTOR, '#transactionTable tbody tr:first-child')

    def get_latest_transaction(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transaction_table)
        )
        latest_row = self.driver.find_element(*self.latest_transaction)
        cells = latest_row.find_elements(By.TAG_NAME, 'td')
        transaction_details = [cell.text for cell in cells]
        return transaction_details
