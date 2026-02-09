# Existing imports
import pytest
from Pages.RuleConfigurationPage import RuleConfigurationPage

# Existing test class and methods remain unchanged

@pytest.mark.asyncio
async def test_TC_SCRUM158_01_valid_rule_schema_submission(page):
    """
    TC_SCRUM158_01: Prepare a valid rule schema with all supported trigger, condition, and action types, submit and verify storage.
    """
    rule_config_page = RuleConfigurationPage(page)
    schema = {
        "trigger": {
            "type": "event",
            "parameters": {"event_type": "login"}
        },
        "conditions": [
            {"type": "ip_range", "parameters": {"range": "192.168.1.0/24"}},
            {"type": "device", "parameters": {"device_type": "mobile"}}
        ],
        "actions": [
            {"type": "notify", "parameters": {"channel": "email"}},
            {"type": "block", "parameters": {"duration": 60}}
        ]
    }
    await rule_config_page.prepare_and_submit_schema(schema)
    await rule_config_page.verify_rule_storage(schema)

@pytest.mark.asyncio
async def test_TC_SCRUM158_02_multiple_conditions_actions(page):
    """
    TC_SCRUM158_02: Prepare a schema with multiple conditions and actions, submit and verify all are stored.
    """
    rule_config_page = RuleConfigurationPage(page)
    schema = {
        "trigger": {
            "type": "schedule",
            "parameters": {"cron": "0 0 * * *"}
        },
        "conditions": [
            {"type": "geo_location", "parameters": {"country": "US"}},
            {"type": "user_group", "parameters": {"group": "admins"}},
            {"type": "custom_attr", "parameters": {"attr": "beta_user"}}
        ],
        "actions": [
            {"type": "log", "parameters": {"level": "warning"}},
            {"type": "notify", "parameters": {"channel": "slack"}},
            {"type": "escalate", "parameters": {"priority": "high"}}
        ]
    }
    await rule_config_page.prepare_and_submit_schema(schema)
    await rule_config_page.verify_rule_storage(schema)
