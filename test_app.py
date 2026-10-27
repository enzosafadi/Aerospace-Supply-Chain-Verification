"""Unit tests for the local workflow and tamper-evident event chain."""
import os
import tempfile
import unittest
from pathlib import Path
import app

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app.DB = Path(self.temp.name) / "test.sqlite3"
        app.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def create(self):
        return app.create_order({"supplier":"Demo Supplier","part":"A-101","quantity":2,"unit_cost":30})["id"]

    def test_create_order(self):
        order_id = self.create()
        self.assertEqual(app.list_orders()[0]["total"], 60)
        self.assertTrue(app.verify_history(order_id)["valid"])

    def test_full_workflow(self):
        order_id = self.create()
        for action in ("approve", "deliver", "verify"):
            app.advance(order_id, action)
        self.assertEqual(app.list_orders()[0]["status"], "verified")
        self.assertEqual(app.verify_history(order_id)["events"], 4)

    def test_invalid_transition(self):
        order_id = self.create()
        with self.assertRaises(ValueError):
            app.advance(order_id, "deliver")

    def test_detect_tampering(self):
        order_id = self.create()
        with app.connect() as conn:
            conn.execute("UPDATE events SET actor='tampered' WHERE order_id=?", (order_id,))
        self.assertFalse(app.verify_history(order_id)["valid"])

if __name__ == "__main__":
    unittest.main()

