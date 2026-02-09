import pytest
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
        await self.login_page.fill_email(''.'

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM158_03_create_rule_schema_with_metadata(self):
        # Step 1: Navigate to Rule Configuration
        await self.rule_page.navigate()
        # Step 2: Fill rule form with metadata
        await self.rule_page.get_rule_name_field().fill('AutoRule158_03')
        await self.rule_page.get_rule_metadata_field().fill('MetaDataValue')
        await self.rule_page.get_trigger_field().fill('OnCreate')
        await self.rule_page.get_condition_field().fill('ConditionX')
        await self.rule_page.get_action_field().fill('ActionY')
        # Step 3: Submit rule
        await self.rule_page.get_submit_button().click()
        # Step 4: Validate rule creation
        assert await self.rule_page.get_success_message().text_content() == 'Rule created successfully'
        # Step 5: Retrieve and check metadata
        rule = await self.rule_page.get_rule_by_name('AutoRule158_03')
        assert rule['metadata'] == 'MetaDataValue'

    async def test_TC_SCRUM158_04_submit_schema_missing_trigger(self):
        # Step 1: Navigate to Rule Configuration
        await self.rule_page.navigate()
        # Step 2: Fill rule form without trigger
        await self.rule_page.get_rule_name_field().fill('AutoRule158_04')
        await self.rule_page.get_rule_metadata_field().fill('MetaDataValue')
        await self.rule_page.get_condition_field().fill('ConditionX')
        await self.rule_page.get_action_field().fill('ActionY')
        # Step 3: Submit rule
        await self.rule_page.get_submit_button().click()
        # Step 4: Validate error response
        assert await self.rule_page.get_error_message().text_content() == 'Trigger field is required'
        assert await self.rule_page.get_response_code() == 400
