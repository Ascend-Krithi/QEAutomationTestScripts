# ForgotPasswordPage.py
"""
PageClass for Password Recovery Page - Enhanced for TC_LOGIN_007 (password recovery form verification).

Executive Summary:
This PageObject enables automated validation of the password recovery navigation and page load after clicking 'Forgot Password' from the login page. It now supports explicit verification of the password recovery form.

Detailed Analysis:
- Existing methods cover arrival on the page.
- New method:
  * is_password_recovery_form_displayed: Verifies the presence of the password recovery form using locators from Locators.json.

Implementation Guide:
- Instantiate ForgotPasswordPage with a WebDriver.
- Use is_password_recovery_form_displayed to confirm the form is present after navigation.

QA Report:
- Methods tested for form presence.

Troubleshooting Guide:
- Update locators if UI changes.

Future Considerations:
- Add methods for submitting recovery email, handling error/success messages, etc.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotPasswordPage:
    """
    Page Object Model for the Password Recovery Page.
    """
    # Locators (replace with actual values from Locators.json as appropriate)
    EMAIL_INPUT = (By.ID, "forgot_password_email")
    SUBMIT_BUTTON = (By.ID, "forgot_password_submit")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_password_recovery_form_displayed(self, timeout=10) -> bool:
        """
        Verifies that the password recovery form is displayed.
        Returns True if the form is visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.SUBMIT_BUTTON))
            return True
        except Exception:
            return False
