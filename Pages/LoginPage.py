from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    PageClass for Login functionality.
    """

    # Locators (can be updated from Locators.json in future)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    ERROR_MESSAGE = (By.ID, "loginErrorMsg")  # Example for system response

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_login(self, url: str):
        """Navigate to the login page."""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def enter_username(self, username: str):
        """Enter username in the username field."""
        username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_elem.clear()
        username_elem.send_keys(username)

    def enter_password(self, password: str):
        """Enter password in the password field."""
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        """Click the login button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def get_error_message(self) -> str:
        """Get the error message after login attempt, if any."""
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except Exception:
            return ""

    def is_logged_in(self) -> bool:
        """
        Checks if login was successful.
        This should be customized based on application behavior (e.g., URL change, presence of profile element).
        """
        # Example: check if profile page loads
        # return self.wait.until(EC.url_contains("/profile"))
        # For now, simply return True if error message is not present
        return self.get_error_message() == ""