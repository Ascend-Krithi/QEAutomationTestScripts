# NavigationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NavigationPage:
    """
    Page Object for navigation actions, such as accessing Bill Pay and Account Overview.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.locators = {
            'billPayLink': (By.LINK_TEXT, 'Bill Pay'),
            'accountOverviewLink': (By.LINK_TEXT, 'Accounts Overview')
        }

    def go_to_bill_pay(self):
        """Navigate to Bill Pay section."""
        self.wait.until(EC.element_to_be_clickable(self.locators['billPayLink'])).click()

    def go_to_account_overview(self):
        """Navigate to Account Overview section."""
        self.wait.until(EC.element_to_be_clickable(self.locators['accountOverviewLink'])).click()
