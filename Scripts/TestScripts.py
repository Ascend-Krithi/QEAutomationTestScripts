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

    def test_TC_SCRUM158_05_invalid_trigger_schema(self):
        """TC_SCRUM158_05: Prepare rule schema with invalid trigger value, submit, expect schema invalid and error about invalid value."""
        rule_data = {
            'name': 'Invalid Trigger Rule',
            'description': 'Rule with invalid trigger value',
            'trigger': 'unknown_trigger',
            'conditions': [{'field': 'amount', 'operator': '>', 'value': 50}],
            'actions': [{'type': 'notify', 'params': {'message': 'Amount above 50'}}],
            'schema': {
                'type': 'object',
                'properties': {
                    'trigger': {'type': 'string'},
                    'conditions': {'type': 'array'},
                    'actions': {'type': 'array'}
                },
                'required': ['trigger', 'conditions', 'actions']
            }
        }
        fill_rule_form(rule_data['name'], rule_data['description'])
        try:
            select_trigger_type(rule_data['trigger'])
        except ValueError as ve:
            error_msg = str(ve)
        else:
            error_msg = get_ui_error_message()
        add_condition(rule_data['conditions'][0]['field'], rule_data['conditions'][0]['operator'], rule_data['conditions'][0]['value'])
        add_multiple_actions(rule_data['actions'])
        edit_json_schema(rule_data['schema'])
        try:
            schema_valid = validate_schema()
        except ValueError as ve:
            schema_valid = False
            schema_error = str(ve)
        else:
            schema_error = get_schema_error_message()
        self.assertFalse(schema_valid, "Schema should be invalid for unknown trigger.")
        self.assertTrue('Unsupported trigger type' in error_msg or 'invalid value' in schema_error, "Error message should indicate invalid trigger value.")

    def test_TC_SCRUM158_06_condition_missing_required_params(self):
        """TC_SCRUM158_06: Prepare rule schema with a condition missing required parameters, submit, expect schema invalid and error about incomplete condition."""
        rule_data = {
            'name': 'Condition Missing Params Rule',
            'description': 'Rule with condition missing required parameters',
            'trigger': 'date',
            'conditions': [{'type': 'amount_above'}],
            'actions': [{'type': 'notify', 'params': {'message': 'Amount above'}}],
            'schema': {
                'type': 'object',
                'properties': {
                    'conditions': {'type': 'array'},
                    'actions': {'type': 'array'}
                },
                'required': ['conditions', 'actions']
            }
        }
        fill_rule_form(rule_data['name'], rule_data['description'])
        select_trigger_type(rule_data['trigger'])
        # Only type provided, missing threshold/source/operator
        add_condition(rule_data['conditions'][0].get('type', ''), '', '')
        add_multiple_actions(rule_data['actions'])
        edit_json_schema(rule_data['schema'])
        try:
            schema_valid = validate_schema()
        except ValueError as ve:
            schema_valid = False
            schema_error = str(ve)
        else:
            schema_error = get_schema_error_message()
        self.assertFalse(schema_valid, "Schema should be invalid for incomplete condition.")
        self.assertTrue('incomplete condition' in schema_error or 'missing required' in schema_error, "Error message should indicate incomplete condition.")
