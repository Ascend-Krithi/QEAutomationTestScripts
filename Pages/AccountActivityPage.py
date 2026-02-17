from selenium.webdriver.common.by import By

class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transaction_table = (By.ID, 'transaction-table')
        self.transaction_rows = (By.CSS_SELECTOR, '#transaction-table tbody tr')

    def get_transaction_rows(self):
        return self.driver.find_elements(*self.transaction_rows)

    def verify_transaction(self, payee_name, amount):
        rows = self.get_transaction_rows()
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            if len(columns) >= 3:
                if columns[1].text == payee_name and columns[2].text == str(amount):
                    return True
        return False
