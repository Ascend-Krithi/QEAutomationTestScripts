# DashboardPage.py
"""
PageClass for Dashboard Page
Covers: TC_Login_07 (session expiration after browser reopen), TC_LOGIN_001 (redirect to dashboard after login)
Strict adherence to Selenium Python best practices, atomic methods, robust locator handling, and comprehensive docstrings.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    """
    Page Object Model for the Dashboard Page.
    Covers:
    - TC_Login_07: Session expiration validation after browser reopen.
    - TC_LOGIN_001: Successful login redirect to dashboard.
    """

    DASHBOARD_HEADER = (By.ID, "dashboardHeader")  # Assumed locator for dashboard
    LOGIN_PAGE_INDICATOR = (By.ID, "loginBtn")     # Used to detect redirect to login after session expiry

    def __init__(self, driver: WebDriver):
        """
        Initializes the DashboardPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_on_dashboard(self) -> bool:
        """
        Checks if the dashboard page is displayed.
        :return: True if dashboard is shown, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_session_expired(self) -> bool:
        """
        Checks if session has expired (user is redirected to login page).
        :return: True if session expired, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_PAGE_INDICATOR))
            return True
        except Exception:
            return False
