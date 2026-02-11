# ServiceLogPage.py
"""
PageClass for verifying rule evaluation service logs.
"""

import os

class ServiceLogPage:
    def __init__(self, log_path='rule_evaluation_service.log'):
        self.log_path = log_path

    def verify_rule_evaluated(self, rule_id):
        if not os.path.exists(self.log_path):
            return False
        with open(self.log_path, 'r') as log_file:
            for line in log_file:
                if f"Rule evaluated: {rule_id}" in line:
                    return True
        return False
