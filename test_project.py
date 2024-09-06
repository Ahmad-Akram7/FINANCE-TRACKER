import unittest
import sqlite3
import os
from io import StringIO
from contextlib import redirect_stdout
from project import (
    create_database,
    execute_query,
    fetch_query,
    add_transaction,
    get_report
)

DATABASE_FILE = 'finance_tracker_test.db'

class TestFinanceTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test database."""
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)
        create_database()

    def setUp(self):
        """Clear the database before each test."""
        execute_query('DELETE FROM transactions')

    def test_add_transaction(self):
        """Test adding a transaction."""
        add_transaction('income', 100.0, 'salary')
        results = fetch_query('SELECT type, amount, category FROM transactions')
        self.assertEqual(results, [('income', 100.0, 'salary')])

    def test_get_report(self):
        """Test generating a report."""
        add_transaction('income', 100.0, 'salary')
        add_transaction('expense', 50.0, 'food')
        add_transaction('savings', 25.0, 'emergency fund')

        with StringIO() as buf, redirect_stdout(buf):
            get_report()
            output = buf.getvalue()

        self.assertIn("Total Income: $100.00", output)
        self.assertIn("Total Expenses: $50.00", output)
        self.assertIn("Total Savings: $25.00", output)
        self.assertIn("Net Savings: $50.00", output)

if __name__ == "__main__":
    unittest.main()
