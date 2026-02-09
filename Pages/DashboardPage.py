# DashboardPage.py
"""
PageClass for Dashboard Page
Covers: TC_LOGIN_001, TC_LOGIN_07 (post-login validation, session expiration)
Ensures dashboard access and session management.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object Model for the Dashboard/Home Page.
    Covers:
    - Post-login redirection
    - Session expiration handling
    """

    DASHBOARD_HEADER = (By.ID, "dashboardHeader")  # Assumed locator

    def __init__(self, driver: WebDriver):
        """
        Initializes the DashboardPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_dashboard_displayed(self) -> bool:
        """
        Validates that the dashboard/home page is displayed.
        :return: True if dashboard header is visible, else False
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_session_active(self) -> bool:
        """
        Checks if session is still active (dashboard visible).
        :return: True if dashboard is displayed, False otherwise
        """
        return self.is_dashboard_displayed()
