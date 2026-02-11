
import pytest
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

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
        await self.login_page.fill_email('testuser@example.com')
        await self.login_page.fill_password('securepassword')
        await self.login_page.check_remember_me()
        await self.login_page.submit_login('testuser@example.com', 'securepassword')
        # Add assertions as needed

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM_158_001_create_rule(self):
        # Step 1: Navigate to Rule Configuration Page
        await self.rule_page.navigate_to_rule_configuration()
        # Step 2: Click "Create Rule"
        await self.rule_page.click_create_rule_button()
        # Step 3: Fill Rule Details
        await self.rule_page.fill_rule_name("AutoTest Rule")
        await self.rule_page.select_rule_type("Validation")
        await self.rule_page.set_rule_condition("Status == 'Open'")
        # Step 4: Save Rule
        await self.rule_page.click_save_rule_button()
        # Step 5: Verify Rule appears in list
        rule_exists = await self.rule_page.is_rule_in_list("AutoTest Rule")
        assert rule_exists, "Rule was not created successfully"

    async def test_TC_SCRUM_158_002_edit_rule(self):
        # Step 1: Navigate to Rule Configuration Page
        await self.rule_page.navigate_to_rule_configuration()
        # Step 2: Find and Edit Rule
        await self.rule_page.select_rule_from_list("AutoTest Rule")
        await self.rule_page.click_edit_rule_button()
        # Step 3: Update Rule Details
        await self.rule_page.update_rule_condition("Status == 'Closed'")
        # Step 4: Save Changes
        await self.rule_page.click_save_rule_button()
        # Step 5: Verify Rule was updated
        updated_condition = await self.rule_page.get_rule_condition("AutoTest Rule")
        assert updated_condition == "Status == 'Closed'", "Rule condition was not updated"
