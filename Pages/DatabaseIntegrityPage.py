# DatabaseIntegrityPage.py
"""
PageClass for verifying database integrity after rule creation and injection attempts.
"""

import psycopg2

class DatabaseIntegrityPage:
    def __init__(self, db_params):
        self.db_params = db_params

    def check_rules_table_exists(self):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'rules')")
        exists = cur.fetchone()[0]
        cur.close()
        conn.close()
        return exists

    def verify_rule_stored(self, trigger_type):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM rules WHERE trigger_type=%s", (trigger_type,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None
