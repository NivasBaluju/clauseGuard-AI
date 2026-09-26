import unittest
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.risk.risk_engine import (
    compute_clause_risk,
    compute_document_risk,
    compute_risk_band,
    get_risk_config,
)

class TestRiskEngine(unittest.TestCase):
    def setUp(self):
        self.config = get_risk_config()

    def test_fair_clause_risk(self):
        # Fair clause should have 0 risk regardless of base weight
        score = compute_clause_risk("security_deposit", "fair", 1.0, config=self.config)
        self.assertEqual(score, 0.0)

    def test_unfavorable_clause_risk(self):
        # Termination base weight is 1.0, unfavorable multiplier is 1.0 -> 100.0
        score = compute_clause_risk("termination", "unfavorable", 1.0, config=self.config)
        self.assertEqual(score, 100.0)

    def test_needs_review_clause_risk(self):
        # Rent payment base weight is 0.6, needs_review multiplier is 0.5 -> 30.0
        score = compute_clause_risk("rent_payment_terms", "needs_review", 1.0, config=self.config)
        self.assertEqual(score, 30.0)

    def test_sequence_adjustment_pair(self):
        # renewal_auto_renewal -> termination has a +0.1 bump
        normal_score = compute_clause_risk("termination", "needs_review", 1.0, prior_clause_type=None, config=self.config)
        bumped_score = compute_clause_risk("termination", "needs_review", 1.0, prior_clause_type="renewal_auto_renewal", config=self.config)
        self.assertGreater(bumped_score, normal_score)

    def test_document_risk_composite(self):
        clause_scores = [20.0, 40.0, 60.0]  # mean = 40.0
        missing = [{"severity": "high"}]     # penalty = 15.0
        # overall = 0.7 * 40.0 + 0.3 * 15.0 = 28.0 + 4.5 = 32.5
        overall = compute_document_risk(clause_scores, missing, config=self.config)
        self.assertEqual(overall, 32.5)

    def test_risk_bands(self):
        self.assertEqual(compute_risk_band(15.0, config=self.config), "low")
        self.assertEqual(compute_risk_band(35.0, config=self.config), "medium")
        self.assertEqual(compute_risk_band(65.0, config=self.config), "high")
        self.assertEqual(compute_risk_band(85.0, config=self.config), "critical")

    def test_bounds(self):
        score_low = compute_clause_risk("pet_policy", "fair", 0.0, config=self.config)
        self.assertGreaterEqual(score_low, 0.0)
        score_high = compute_document_risk([100.0] * 10, [{"severity": "high"}] * 10, config=self.config)
        self.assertLessEqual(score_high, 100.0)

if __name__ == "__main__":
    unittest.main()
