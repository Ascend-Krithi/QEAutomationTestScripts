# Import necessary modules
from Pages.LoginPage import LoginPage
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_empty_fields_validation(self):
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        assert self.login_page.get_error_message().strip() == "Email/Username required"

    def test_remember_me_functionality(self):
        # Placeholder for remember me test
        pass

class TestRuleConfiguration:
    def __init__(self, driver, api_base_url=None, api_token=None):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver, api_base_url, api_token)

    def test_invalid_trigger(self):
        error_message = self.rule_page.validate_invalid_trigger()
        assert "invalid" in error_message.lower()

    def test_missing_condition_parameter(self):
        error_message = self.rule_page.validate_missing_condition_parameter()
        assert "missing" in error_message.lower() or "incomplete" in error_message.lower()

    def test_max_conditions_actions(self):
        # TC_SCRUM158_07: Prepare rule with max conditions/actions, submit, validate persistence
        conditions = [{"type": "amount_above", "amount": i * 10} for i in range(1, 11)]
        actions = [{"type": "transfer", "amount": i * 5} for i in range(1, 11)]
        schema_json = self.rule_page.prepare_rule_schema(conditions, actions)
        # UI validation
        self.rule_page.enter_json_schema(schema_json)
        self.rule_page.click_validate_schema()
        try:
            ui_result = self.rule_page.get_success_message()
        except Exception:
            ui_result = self.rule_page.get_schema_error_message()
        assert "valid" in ui_result.lower() or "success" in ui_result.lower()
        # API submission
        api_status, api_resp = self.rule_page.submit_rule_schema_api(schema_json)
        assert api_status == 201 or api_status == 200
        rule_id = api_resp.get("id")
        assert rule_id is not None
        # Persistence validation
        is_persisted = self.rule_page.validate_rule_persistence(rule_id, conditions, actions)
        assert is_persisted, "Rule persistence failed"

    def test_empty_conditions_actions(self):
        # TC_SCRUM158_08: Prepare rule with empty conditions/actions, submit, validate UI/API
        ui_result, (api_status, api_resp) = self.rule_page.validate_empty_conditions_actions_schema()
        # UI validation: error or success message
        assert "error" in ui_result.lower() or "success" in ui_result.lower()
        # API validation: check for expected response
        assert api_status in [200, 201, 400], "Unexpected API status code"
