"""Fixture-only tests. CI should not hit live shops."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config, database, fetch
from src.category_tracker import run_query, summarize
from src.stores.example_mart import ExampleMartEngine


class TestHardDenyCircuit(unittest.TestCase):
    def setUp(self):
        fetch.reset_circuits()

    def test_acl_body_trips_after_streak(self):
        body = "Access control list denies the request from this endpoint"
        self.assertTrue(fetch.is_hard_deny_body(body))
        fetch.record_hard_deny("demo")
        self.assertFalse(fetch.circuit_blocks("demo"))
        fetch.record_hard_deny("demo")
        self.assertTrue(fetch.circuit_blocks("demo"))

    def test_success_clears_streak(self):
        fetch.record_hard_deny("demo")
        fetch.record_success("demo")
        fetch.record_hard_deny("demo")
        self.assertFalse(fetch.circuit_blocks("demo"))


class TestExampleMart(unittest.TestCase):
    def test_parses_fixture(self):
        offers = ExampleMartEngine().search("GPU", limit=10)
        self.assertGreaterEqual(len(offers), 2)
        self.assertTrue(all(o.store == "ExampleMart" for o in offers))
        self.assertTrue(all("example.invalid" in o.url for o in offers))

    def test_query_filter(self):
        offers = ExampleMartEngine().search("DDR5", limit=10)
        self.assertEqual(len(offers), 1)
        self.assertIn("DDR5", offers[0].title)


class TestOrchestration(unittest.TestCase):
    def test_run_query_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "t.db"
            old = config.DATABASE_PATH
            config.DATABASE_PATH = str(db)
            try:
                offers = run_query("GPU", persist=True)
                self.assertTrue(offers)
                conn = database.connect(str(db))
                n = conn.execute("SELECT COUNT(*) FROM price_observations").fetchone()[0]
                conn.close()
                self.assertEqual(n, len(offers))
                self.assertIn("ExampleMart", summarize(offers))
            finally:
                config.DATABASE_PATH = old

    def test_live_fetch_blocked_in_demo(self):
        self.assertTrue(config.DEMO_FIXTURES_ONLY)
        result = fetch.fetch_url("x", "https://example.com/")
        self.assertFalse(result.ok)
        self.assertIn("DEMO_FIXTURES_ONLY", result.error)


if __name__ == "__main__":
    unittest.main()
