import sys
from pathlib import Path
from collections import Counter

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.enrich_corpus import RENTAL_SOURCES, OFFER_SOURCES, INSURANCE_SOURCES

def calibrate_clause_favorability(doc_type: str, text: str, initial_fav: str, ctype: str) -> str:
    t = text.lower()
    
    if doc_type == "rental_agreement":
        if ctype == "late_fees_penalty":
            if any(k in t for k in ["daily late fee", "daily penalty", "per day thereafter", "10%"]):
                return "unfavorable"
            elif any(k in t for k in ["$50", "$40", "no grace period", "3rd of the month"]):
                return "needs_review"
            return "fair"
        elif ctype == "entry_notice_access":
            if any(k in t for k in ["without prior notice", "without appointment", "any time during regular"]):
                return "unfavorable"
            elif any(k in t for k in ["twelve (12)", "12 hours", "12-hour"]):
                return "needs_review"
            return "fair"
        elif ctype == "subletting":
            if any(k in t for k in ["strictly forbidden", "strictly prohibited", "incurable lease violation"]):
                return "unfavorable"
            elif any(k in t for k in ["sole discretion", "unauthorized occupant residing more than 3"]):
                return "needs_review"
            return "fair"
        elif ctype == "dispute_resolution":
            if any(k in t for k in ["waive any right to a trial by jury", "waives right to a jury trial", "binding arbitration"]):
                return "unfavorable"
            return "fair"
        elif ctype == "indemnification":
            if any(k in t for k in ["regardless of cause", "exempting landlord", "waiving landlord"]):
                return "unfavorable"
            elif any(k in t for k in ["all claims, liabilities, damages"]):
                return "needs_review"
            return "fair"
        elif ctype == "renewal_auto_renewal":
            if any(k in t for k in ["10% rent escalation", "solely by landlord", "90 days"]):
                return "unfavorable"
            elif any(k in t for k in ["60 days", "sixty (60) days"]):
                return "needs_review"
            return "fair"
        elif ctype == "maintenance_repairs":
            if any(k in t for k in ["sole expense", "financially responsible for all minor", "clogged drains"]):
                return "unfavorable"
            return "fair"
        elif ctype == "pet_policy":
            if any(k in t for k in ["$500.00", "$20.00 per day", "non-refundable pet fee"]):
                return "unfavorable"
            elif any(k in t for k in ["monthly pet rent", "monthly pet fee"]):
                return "needs_review"
            return "fair"
        return initial_fav

    elif doc_type == "job_offer_letter":
        if ctype == "at_will_employment":
            if any(k in t for k in ["sole discretion", "modify your title, compensation"]):
                return "unfavorable"
            return "needs_review"  # Standard at-will means termination without cause/notice
        elif ctype == "non_compete_non_solicit":
            if any(k in t for k in ["24 months", "aggressive", "competitive business"]):
                return "unfavorable"
            return "needs_review"  # Restrictions on outside activities / soliciting colleagues
        elif ctype == "arbitration_dispute_resolution":
            if any(k in t for k in ["binding aaa arbitration", "waive right to participate in any class action", "binding arbitration"]):
                return "unfavorable"
            return "needs_review"  # Mandatory internal grievance process
        elif ctype == "termination_conditions":
            if any(k in t for k in ["probationary period", "forfeited immediately", "without severance", "without administrative appeal"]):
                return "unfavorable"
            elif any(k in t for k in ["signing a standard release", "conditioned on"]):
                return "needs_review"
            return "fair"
        elif ctype == "intellectual_property_assignment":
            if any(k in t for k in ["whether or not conceived on company time", "all inventions, developments"]):
                return "unfavorable"
            elif any(k in t for k in ["su-18", "patent agreement", "assign all rights", "assigning to the university"]):
                return "needs_review"
            return "fair"
        elif ctype == "start_date_contingencies":
            if any(k in t for k in ["5 business days", "3 business days", "48 hours"]):
                return "needs_review"
            return "fair"
        elif ctype == "bonus_incentive":
            if any(k in t for k in ["discretionary", "legislative appropriations", "subject to board approval"]):
                return "needs_review"
            return "fair"
        elif ctype == "confidentiality_nda":
            if any(k in t for k in ["salaries", "discussing"]):
                return "unfavorable"
            return "fair"
        return initial_fav

    elif doc_type == "insurance_policy":
        if ctype == "exclusions":
            if any(k in t for k in ["water damage", "flood", "sewer backup", "earth movement", "earthquake"]):
                return "unfavorable"
            elif any(k in t for k in ["mold", "fungi", "bacteria"]):
                return "needs_review"
            return "fair"
        elif ctype == "deductible_premium":
            if any(k in t for k in ["2%", "percentage", "hurricane deductible", "windstorm"]):
                return "needs_review"
            return "fair"
        elif ctype == "claims_process":
            if any(k in t for k in ["30 calendar days", "regardless of whether insurer suffered actual prejudice", "bar recovery"]):
                return "unfavorable"
            elif any(k in t for k in ["one (1) year", "statutory notice"]):
                return "needs_review"
            return "fair"
        elif ctype == "grace_period":
            if any(k in t for k in ["without grace period", "lapse immediately"]):
                return "unfavorable"
            return "fair"
        elif ctype == "dispute_resolution_appraisal":
            if any(k in t for k in ["suit against us", "one (1) year"]):
                return "needs_review"
            return "fair"
        elif ctype == "misrepresentation_fraud_clause":
            if any(k in t for k in ["immaterial", "whether material or immaterial"]):
                return "unfavorable"
            return "fair"
        return initial_fav

# Apply calibration
for doc_type, sources in [("rental_agreement", RENTAL_SOURCES), ("job_offer_letter", OFFER_SOURCES), ("insurance_policy", INSURANCE_SOURCES)]:
    for d in sources:
        new_clauses = []
        for c in d["clauses"]:
            text, ctype, fav = c[0], c[1], c[2]
            cal_fav = calibrate_clause_favorability(doc_type, text, fav, ctype)
            new_clauses.append((text, ctype, cal_fav))
        d["clauses"] = new_clauses

    favs = Counter(c[2] for d in sources for c in d["clauses"])
    print(f"=== CALIBRATED {doc_type.upper()} ===")
    for f, cnt in sorted(favs.items(), key=lambda x: -x[1]):
        print(f"  {f:15s}: {cnt:3d} ({cnt/sum(favs.values())*100:.1f}%)")
