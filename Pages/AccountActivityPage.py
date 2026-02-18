from selenium.webdriver.common.by import By
class AccountActivityPage:
    def __init__(self, driver):
        self.driver = driver
        self.transactionTable = (By.ID, 'transactionTable')
        self.latestTransaction = (By.CSS_SELECTOR, '#transactionTable tbody tr:first-child')

    def is_transaction_table_displayed(self):
        return self.driver.find_element(*self.transactionTable).is_displayed()

    def get_latest_transaction(self):
        row = self.driver.find_element(*self.latestTransaction)
        return [cell.text for cell in row.find_elements_by_tag_name('td')]

    def get_all_transactions(self):
        table = self.driver.find_element(*self.transactionTable)
        rows = table.find_elements_by_css_selector('tbody tr')
        return [[cell.text for cell in row.find_elements_by_tag_name('td')] for row in rows]
