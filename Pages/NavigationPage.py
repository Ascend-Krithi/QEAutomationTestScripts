# NavigationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NavigationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.billPayLink = (By.LINK_TEXT, "Bill Pay")
        self.accountOverviewLink = (By.LINK_TEXT, "Accounts Overview")

    def go_to_bill_pay(self):
        self.wait.until(EC.element_to_be_clickable(self.billPayLink)).click()

    def go_to_account_overview(self):
        self.wait.until(EC.element_to_be_clickable(self.accountOverviewLink)).click()
