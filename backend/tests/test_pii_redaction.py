import unittest
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.privacy.pii_redactor import redact

class TestPIIRedaction(unittest.TestCase):
    def test_redact_entities(self):
        sample = "Tenant Alice Walker will pay Landlord Bob Vance at bob@realty.com or (312) 555-0199."
        redacted_text, findings = redact(sample)
        
        self.assertNotIn("Alice Walker", redacted_text)
        self.assertNotIn("Bob Vance", redacted_text)
        self.assertNotIn("bob@realty.com", redacted_text)
        self.assertNotIn("312) 555-0199", redacted_text)
        
        entity_types = [f["entity_type"] for f in findings]
        self.assertIn("EMAIL_ADDRESS", entity_types)
        self.assertTrue(any(t in ["PERSON", "NAME"] for t in entity_types))

    def test_date_time_preserved(self):
        # Mandatory architectural test: DATE_TIME must NOT be redacted
        sample = "This lease begins on September 1, 2026 and requires 30 days written notice prior to August 31, 2027."
        redacted_text, findings = redact(sample)

        # Dates and durations should remain intact for deadline extraction
        self.assertIn("September 1, 2026", redacted_text)
        self.assertIn("30 days", redacted_text)
        self.assertIn("August 31, 2027", redacted_text)
        
        # Verify DATE_TIME was not among the redacted entities
        entity_types = [f["entity_type"] for f in findings]
        self.assertNotIn("DATE_TIME", entity_types)

if __name__ == "__main__":
    unittest.main()
