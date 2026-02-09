# DashboardPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object for the Dashboard Page.
    Provides methods to validate successful login and interact with dashboard elements.
    """
    # Locators (Assumed, update with actual values from Locators.json when available)
    DASHBOARD_HEADER = (By.XPATH, '//h1[text()="Dashboard"]')
    USER_PROFILE_ICON = (By.ID, 'userProfileIcon')

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def is_dashboard_displayed(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_user_profile_icon_displayed(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False
