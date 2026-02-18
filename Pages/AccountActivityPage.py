import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transaction_table = (By.ID, "transactionTable")
        self.latest_transaction = (By.CSS_SELECTOR, "#transactionTable tbody tr:first-child")

    def is_transaction_present(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.transaction_table))
            return len(self.driver.find_elements(*self.latest_transaction)) > 0
        except Exception:
            return False

    def get_latest_transaction_details(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.latest_transaction))
        row = self.driver.find_element(*self.latest_transaction)
        return [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
