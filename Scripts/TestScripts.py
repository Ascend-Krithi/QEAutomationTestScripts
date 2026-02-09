# Import necessary modules
import pytest
from selenium import webdriver
from RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('

# --- Appended Selenium Test Methods for TC_SCRUM158_03 and TC_SCRUM158_04 ---

class TestRuleConfiguration:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_TC_SCRUM158_03_valid_rule_metadata_and_schema(self):
        # Set Rule Metadata
        self.rule_page.set_rule_id("RC_158_03")
        self.rule_page.set_rule_name("Deposit After Threshold")
        description = "Deposit triggered after balance threshold"
        tags = ["deposit", "threshold", "automation"]
        self.rule_page.enter_rule_metadata(description, tags)
        # Validate Schema
        self.rule_page.validate_schema()
        assert self.rule_page.is_schema_valid(), "Schema should be valid for correct metadata"
        # Submit Rule
        self.rule_page.submit_rule()
        # Assert Metadata Matches
        assert self.rule_page.assert_metadata_matches(description, tags), "Metadata should match expected values"

    def test_TC_SCRUM158_04_invalid_schema_feedback(self):
        # Set Rule Metadata with invalid schema (missing tags)
        self.rule_page.set_rule_id("RC_158_04")
        self.rule_page.set_rule_name("Deposit Missing Tags")
        description = "Deposit rule missing tags"
        tags = []  # Intentionally empty to trigger schema error
        self.rule_page.enter_rule_metadata(description, tags)
        # Validate Schema
        self.rule_page.validate_schema()
        # Assert Schema Error Message Appears
        error = self.rule_page.get_schema_error()
        assert error is not None, "Schema error feedback should be displayed"
        assert "tags" in error.lower(), "Error message should mention missing tags"
