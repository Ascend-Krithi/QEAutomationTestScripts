# Pages/Navigation.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Navigation:
    def __init__(self, driver):
        self.driver = driver
        self.bill_pay_link = (By.LINK_TEXT, 'Bill Pay')
        self.account_overview_link = (By.LINK_TEXT, 'Accounts Overview')

    def go_to_bill_pay(self):
        bill_pay = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.bill_pay_link)
        )
        bill_pay.click()

    def go_to_account_overview(self):
        account_overview = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.account_overview_link)
        )
        account_overview.click()
