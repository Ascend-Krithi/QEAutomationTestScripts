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
        return self.driver.find_element(*self.latest_transaction)

    def verify_latest_transaction(self, payee_name, amount):
        row = self.get_latest_transaction()
        columns = row.find_elements(By.TAG_NAME, 'td')
        # Assuming columns: [Date, Payee, Amount, ...]
        if len(columns) >= 3:
            actual_payee = columns[1].text.strip()
            actual_amount = columns[2].text.strip().replace('$', '')
            try:
                actual_amount_float = float(actual_amount)
            except ValueError:
                return False
            return actual_payee == payee_name and abs(float(amount) - actual_amount_float) < 0.001
        return False
