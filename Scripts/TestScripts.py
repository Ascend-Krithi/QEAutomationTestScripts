
import unittest
from RuleConfigurationPage import (
    fill_rule_form,
    select_trigger_type,
    add_condition,
    add_multiple_actions,
    edit_json_schema,
    validate_schema,
    submit_rule,
    get_schema_error_message,
    get_ui_error_message
)

class TestRuleConfiguration(unittest.TestCase):
    # Existing test methods here...

    def test_TC_SCRUM158_09_create_rule_with_minimum_required_fields(self):
        """TC_SCRUM158_09: Create rule with minimum required fields, supported trigger, valid schema."""
        rule_data = {
            'name': 'Minimum Rule',
            'description': 'Rule with minimum required fields',
            'trigger': 'balance_above',
            'conditions': [{'field': 'balance', 'operator': '>', 'value': 100}],
            'actions': [{'type': 'notify', 'params': {'message': 'Balance above 100'}}],
            'schema': {
                'type': 'object',
                'properties': {
                    'balance': {'type': 'number'}
                },
                'required': ['balance']
            }
        }
        fill_rule_form(rule_data['name'], rule_data['description'])
        select_trigger_type(rule_data['trigger'])
        add_condition(rule_data['conditions'][0]['field'], rule_data['conditions'][0]['operator'], rule_data['conditions'][0]['value'])
        add_multiple_actions(rule_data['actions'])
        edit_json_schema(rule_data['schema'])
        schema_valid = validate_schema()
        self.assertTrue(schema_valid, "Schema should be valid for minimum required fields.")
        submit_rule()
        ui_error = get_ui_error_message()
        self.assertIsNone(ui_error, "UI should not show any error for valid rule creation.")

    def test_TC_SCRUM158_10_create_rule_with_unsupported_trigger(self):
        """TC_SCRUM158_10: Attempt to create rule with unsupported trigger, expect schema validation error."""
        rule_data = {
            'name': 'Unsupported Trigger Rule',
            'description': 'Rule with unsupported trigger',
            'trigger': 'future_trigger',
            'conditions': [{'field': 'date', 'operator': '==', 'value': '2024-07-01'}],
            'actions': [{'type': 'notify', 'params': {'message': 'Date matched'}}],
            'schema': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'format': 'date'}
                },
                'required': ['date']
            }
        }
        fill_rule_form(rule_data['name'], rule_data['description'])
        select_trigger_type(rule_data['trigger'])
        add_condition(rule_data['conditions'][0]['field'], rule_data['conditions'][0]['operator'], rule_data['conditions'][0]['value'])
        add_multiple_actions(rule_data['actions'])
        edit_json_schema(rule_data['schema'])
        schema_valid = validate_schema()
        self.assertFalse(schema_valid, "Schema should be invalid for unsupported trigger.")
        error_msg = get_schema_error_message()
        self.assertIsNotNone(error_msg, "Schema error message should be displayed for unsupported trigger.")
        submit_rule()
        ui_error = get_ui_error_message()
        self.assertIsNotNone(ui_error, "UI should show error for unsupported trigger rule creation.")

# Existing test methods continue below (if any)...
