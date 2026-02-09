# FinancialTransferPage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class FinancialTransferPage:
    """
    Page Object Model for Financial Transfer operations.
    Handles preparing and submitting JSON payloads, validating errors for missing fields, and interacting with relevant UI elements.
    """

    # Locators (extracted from Locators.json)
    TRANSFER_BUTTON = (By.ID, "transferBtn")
    PAYLOAD_TEXTAREA = (By.ID, "payloadInput")
    SUBMIT_BUTTON = (By.ID, "submitTransfer")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error-message")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.success-message")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the FinancialTransferPage.
        :param driver: Selenium WebDriver instance
        :param timeout: Default timeout for waiting operations
        """
        self.driver = driver
        self.timeout = timeout

    def open_transfer_dialog(self):
        """
        Opens the financial transfer dialog/modal by clicking the transfer button.
        """
        transfer_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.TRANSFER_BUTTON)
        )
        transfer_btn.click()

    def enter_payload(self, payload: dict):
        """
        Enters the JSON payload into the payload textarea.
        :param payload: Dictionary representing the financial transfer JSON
        """
        payload_textarea = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PAYLOAD_TEXTAREA)
        )
        payload_textarea.clear()
        payload_textarea.send_keys(self._format_payload(payload))

    def submit_transfer(self):
        """
        Submits the financial transfer request.
        """
        submit_btn = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        )
        submit_btn.click()

    def get_error_message(self):
        """
        Retrieves any error message displayed after submission.
        :return: Error message string or None
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text
        except TimeoutException:
            return None

    def get_success_message(self):
        """
        Retrieves the success message displayed after successful transfer.
        :return: Success message string or None
        """
        try:
            success_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return success_elem.text
        except TimeoutException:
            return None

    def validate_missing_fields(self, payload: dict, required_fields: list) -> list:
        """
        Validates if any required fields are missing from the payload.
        :param payload: Dictionary representing the financial transfer JSON
        :param required_fields: List of required field names
        :return: List of missing field names
        """
        missing = [field for field in required_fields if field not in payload]
        return missing

    @staticmethod
    def _format_payload(payload: dict) -> str:
        """
        Formats the payload dictionary as a pretty JSON string.
        :param payload: Dictionary
        :return: JSON string
        """
        import json
        return json.dumps(payload, indent=2)
