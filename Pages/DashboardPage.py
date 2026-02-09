# DashboardPage.py
"""
Selenium PageClass for Dashboard Page
Validates successful login by checking dashboard elements.

Industry Best Practices:
- Locators encapsulated as class attributes
- Explicit waits for element visibility
- Clear docstrings and method documentation
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class DashboardPage:
    """
    Page Object for Dashboard Page.
    """
    # Locators (assumed based on repo conventions)
    dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
    user_profile_icon = (By.ID, "profile-icon")

    def __init__(self, driver):
        """
        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        """
        Validate that the dashboard page is loaded.
        Returns:
            bool: True if dashboard header and profile icon are visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.dashboard_header))
            self.wait.until(EC.visibility_of_element_located(self.user_profile_icon))
            return True
        except TimeoutException:
            return False
