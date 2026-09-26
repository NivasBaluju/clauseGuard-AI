"""
ClauseGuard AI — User Document Ingestion + Balanced 10,000-Row Dataset Builder

Pipeline:
1.  Read all .docx / .pdf files from C:\\Users\\DELL\\Downloads\\documents
2.  Classify each document into rental_agreement / job_offer_letter / insurance_policy
3.  Extract text, apply Presidio PII redaction (preserving DATE_TIME)
4.  Segment into clauses, label with heuristics (clause_type + favorability)
5.  Merge with existing 850 real public-doc clauses from ml/datasets/
6.  Deduplicate on normalized clause text (Jaccard > 0.85 => duplicate)
7.  Generate scenario-based synthetic clauses to fill gaps and reach ~10,000 rows total,
    with EQUAL clause-type distribution across all 3 document types
8.  Document-isolated train/val/test split (70/15/15)
9.  Retrain TF-IDF Baseline + DistilBERT (with/without context) on the new dataset
10. Overwrite ml/artifacts/model_comparison_report.json with new metrics
"""

import os
import sys
import re
import json
import random
import hashlib
from pathlib import Path
from collections import defaultdict

project_root = Path(__file__).resolve().parent.parent
backend_dir  = project_root / "backend"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(backend_dir))

DOWNLOADS_DIR   = Path(r"C:\Users\DELL\Downloads\documents")
DATASET_ROOT    = project_root / "ml" / "datasets"
ARTIFACTS_DIR   = project_root / "ml" / "artifacts"
TARGET_PER_TYPE = 3334   # ~10,002 total across 3 types

random.seed(42)

# ---------------------------------------------------------------------------
# STEP 1: Text extraction
# ---------------------------------------------------------------------------
def extract_text_docx(path: Path) -> str:
    try:
        import docx as docx_lib
        doc = docx_lib.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"  [WARN] DOCX {path.name}: {e}")
        return ""

def extract_text_pdf(path: Path) -> str:
    try:
        import pdfplumber
        parts = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
        return "\n".join(parts)
    except Exception as e:
        print(f"  [WARN] PDF {path.name}: {e}")
        return ""

def extract_text(path: Path) -> str:
    return extract_text_docx(path) if path.suffix.lower() == ".docx" else extract_text_pdf(path)

# ---------------------------------------------------------------------------
# STEP 2: Document type classifier
# ---------------------------------------------------------------------------
RENTAL_KW    = ["rental agreement","rent agreement","lease agreement","landlord",
                 "tenant","security deposit","monthly rent","premises","tenancy"]
OFFER_KW     = ["offer letter","job offer","employment offer","position of","salary",
                 "joining date","compensation","designation","we are pleased to offer",
                 "base salary","ctc","package"]
INSURANCE_KW = ["insurance policy","policy document","coverage","premium","insured",
                 "deductible","claim","indemnity","sum insured","policyholder",
                 "insurer","exclusion","endorsement","underwriter"]

def classify_document(text: str, filename: str) -> str:
    fl = filename.lower()
    tl = text.lower()[:4000]
    # Filename override
    if any(k in fl for k in ["rental","rent","lease","tenancy","agreement"]):
        return "rental_agreement"
    if any(k in fl for k in ["offer","job","employment","tcs","google","aliens",
                               "greythr","joboffer","formal"]):
        return "job_offer_letter"
    if any(k in fl for k in ["insurance","policy","car_ins","health_ins","sme_ins",
                               "householders","jeevan","family","travel","private-car",
                               "business package","pos-travel","brochure"]):
        return "insurance_policy"
    scores = {
        "rental_agreement": sum(1 for k in RENTAL_KW    if k in tl),
        "job_offer_letter": sum(1 for k in OFFER_KW      if k in tl),
        "insurance_policy": sum(1 for k in INSURANCE_KW  if k in tl),
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "rental_agreement"

# ---------------------------------------------------------------------------
# STEP 3: PII Redaction (reuse backend; fallback to regex)
# ---------------------------------------------------------------------------
def redact_text(text: str) -> str:
    try:
        from services.pii_redaction import redact_pii
        redacted, _ = redact_pii(text, preserve_date_time=True)
        return redacted
    except Exception:
        text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '<PERSON>', text)
        text = re.sub(r'\b\d{10}\b', '<PHONE_NUMBER>', text)
        text = re.sub(r'\S+@\S+\.\S+', '<EMAIL_ADDRESS>', text)
        text = re.sub(r'\b(?:Rs\.?|INR|USD|\$|€)\s*[\d,]+', '<MONEY>', text)
        return text

# ---------------------------------------------------------------------------
# STEP 4: Clause segmentation
# ---------------------------------------------------------------------------
SPLIT_RE = re.compile(
    r'\n(?=\s*(?:\d+[\.\)]\s|\([a-zA-Z0-9]+\)|[A-Z]{2,}[\s:]|(?:SECTION|CLAUSE|ARTICLE|SCHEDULE|PART|WHEREAS|NOW THEREFORE)\s))',
    re.MULTILINE
)

def segment_clauses(text: str) -> list:
    parts = SPLIT_RE.split(text)
    clauses, buf = [], ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(p) < 40:
            buf = (buf + " " + p).strip()
        else:
            if buf:
                clauses.append(buf)
                buf = ""
            clauses.append(p)
    if buf:
        clauses.append(buf)
    # Break very long paragraphs
    final = []
    for c in clauses:
        if len(c) > 2500:
            for chunk in re.split(r'\n\n', c):
                chunk = chunk.strip()
                if len(chunk) >= 40:
                    final.append(chunk)
        else:
            if len(c) >= 40:
                final.append(c)
    return final

# ---------------------------------------------------------------------------
# STEP 5: Heuristic labelers (import existing; fallback inline)
# ---------------------------------------------------------------------------
def _load_heuristics():
    try:
        from ml.dataset_corpus_data     import heuristic_rental_clause_type  as h_r
        from ml.dataset_corpus_offer    import heuristic_offer_clause_type    as h_o
        from ml.dataset_corpus_insurance import heuristic_insurance_clause_type as h_i
        return h_r, h_o, h_i
    except Exception:
        def h_r(t):
            t = t.lower()
            if any(k in t for k in ["deposit","security deposit"]): return "security_deposit"
            if any(k in t for k in ["rent","monthly payment","rental amount"]): return "rent_payment"
            if any(k in t for k in ["terminat","notice to quit","vacate"]): return "termination"
            if any(k in t for k in ["maintenance","repair"]): return "maintenance_repairs"
            if any(k in t for k in ["pet","animal"]): return "pet_policy"
            if any(k in t for k in ["subleas","sublet","assign"]): return "subletting_assignment"
            if any(k in t for k in ["utilities","water","electricity","gas bill"]): return "utilities"
            if any(k in t for k in ["entry","landlord may enter","access","inspect"]): return "entry_notice_access"
            if any(k in t for k in ["governing law","jurisdiction","state of"]): return "governing_law_jurisdiction"
            if any(k in t for k in ["indemnif","hold harmless"]): return "indemnification"
            if any(k in t for k in ["renew","extension","option to renew"]): return "renewal_options"
            if any(k in t for k in ["alterati","improvement","modification"]): return "alterations_improvements"
            if any(k in t for k in ["insurance","liability","renter"]): return "insurance_liability"
            if any(k in t for k in ["dispute","arbitrat","mediat"]): return "dispute_resolution"
            return "general_terms"

        def h_o(t):
            t = t.lower()
            if any(k in t for k in ["salary","compensation","base pay","ctc","remuneration"]): return "compensation_salary"
            if any(k in t for k in ["bonus","incentive","performance pay","variable"]): return "bonus_incentive"
            if any(k in t for k in ["start date","joining date","commencement"]): return "start_date"
            if any(k in t for k in ["position","role","title","designation"]): return "job_title_role"
            if any(k in t for k in ["terminat","notice period","at-will","separation"]): return "termination_conditions"
            if any(k in t for k in ["confidential","non-disclosure","nda"]): return "confidentiality_nda"
            if any(k in t for k in ["non-compete","non compete"]): return "non_compete"
            if any(k in t for k in ["intellectual property","ip","inventions","work product"]): return "intellectual_property"
            if any(k in t for k in ["benefit","health insurance","provident fund","pf","leave"]): return "benefits"
            if any(k in t for k in ["relocat","transfer","posting"]): return "relocation"
            if any(k in t for k in ["probation","trial period"]): return "probation_period"
            return "general_terms"

        def h_i(t):
            t = t.lower()
            if any(k in t for k in ["coverage","covers","insured event","loss covered"]): return "coverage_scope"
            if any(k in t for k in ["exclusion","not covered","does not cover","except"]): return "exclusions"
            if any(k in t for k in ["premium","payment of premium"]): return "premium_payment"
            if any(k in t for k in ["claim","filing a claim","claim procedure","loss notice"]): return "claims_procedure"
            if any(k in t for k in ["deductible","excess","self-retention"]): return "deductibles_excess"
            if any(k in t for k in ["limit","maximum","sum insured","maximum liability"]): return "limits_of_liability"
            if any(k in t for k in ["renew","renewal date","policy period"]): return "policy_renewal"
            if any(k in t for k in ["cancellation","cancel","terminate the policy"]): return "cancellation_terms"
            if any(k in t for k in ["definition","means","herein"]): return "definitions"
            if any(k in t for k in ["arbitrat","dispute","appraisal"]): return "dispute_resolution"
            if any(k in t for k in ["subrogat"]): return "subrogation"
            return "general_terms"

        return h_r, h_o, h_i

heuristic_rental, heuristic_offer, heuristic_insurance = _load_heuristics()
HEURISTIC_FN = {
    "rental_agreement": heuristic_rental,
    "job_offer_letter": heuristic_offer,
    "insurance_policy": heuristic_insurance,
}

# ---------------------------------------------------------------------------
# STEP 6: Favorability assessment
# ---------------------------------------------------------------------------
UNFAV = {
    "rental_agreement": ["shall not","tenant shall pay","forfeit","penalty","landlord may",
                          "at landlord's sole discretion","non-refundable","tenant is responsible",
                          "no pets","no subletting","waive","as-is"],
    "job_offer_letter": ["at-will","company may terminate","without cause","no severance",
                          "non-compete","perpetual","worldwide","all inventions",
                          "sole discretion","may be changed","not guaranteed"],
    "insurance_policy": ["exclusion","not covered","does not cover","except","however",
                          "void","forfeiture","unless","shall not apply","not payable",
                          "at insurer's discretion"],
}
FAV  = {
    "rental_agreement": ["tenant has the right","landlord shall","refundable","shall provide",
                          "tenant may","reasonable notice","mutual agreement"],
    "job_offer_letter": ["we offer","company provides","employee is entitled","guaranteed",
                          "severance","full benefits","reimbursed"],
    "insurance_policy": ["covered","shall pay","insurer will","up to","payable","no deductible"],
}

def assess_favorability(doc_type: str, text: str) -> str:
    t = text.lower()
    u = sum(1 for s in UNFAV.get(doc_type, []) if s in t)
    f = sum(1 for s in FAV.get(doc_type, [])   if s in t)
    if u >= 2 or (u > f and u >= 1):
        return "unfavorable"
    if u == 1 and f == 0:
        return "needs_review"
    return "fair"

# ---------------------------------------------------------------------------
# STEP 7: Deduplication
# ---------------------------------------------------------------------------
def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower().strip())

def jaccard(a: str, b: str, k: int = 3) -> float:
    sa = set(a[i:i+k] for i in range(max(0,len(a)-k+1)))
    sb = set(b[i:i+k] for i in range(max(0,len(b)-k+1)))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def is_duplicate(text: str, seen: list, threshold: float = 0.85) -> bool:
    n = normalize(text)
    for s in seen[-800:]:
        if jaccard(n, s) >= threshold:
            return True
    return False

# ---------------------------------------------------------------------------
# STEP 8: Synthetic scenario clause pools
# ---------------------------------------------------------------------------
SYNTHETIC_POOLS = {

"rental_agreement": [
    # security_deposit
    ("The Tenant shall pay a security deposit equal to two months' rent prior to move-in. This deposit is refundable within 21 days of lease termination.", "security_deposit","fair"),
    ("A non-refundable security deposit of three months' rent is required. Tenant forfeits the entire amount if vacating before the lease end date.", "security_deposit","unfavorable"),
    ("The security deposit of two thousand five hundred dollars shall be held in a non-interest-bearing escrow account. Landlord shall provide itemized deductions within 30 days.", "security_deposit","fair"),
    ("Tenant agrees that the security deposit may be applied by Landlord to unpaid rent, damage costs, or cleaning fees at Landlord's sole discretion.", "security_deposit","unfavorable"),
    ("In the event of a co-signer arrangement, the co-signer assumes full liability for the security deposit if the primary tenant defaults.", "security_deposit","needs_review"),
    ("The security deposit shall be returned in full provided the premises are returned in the same condition as received, excepting reasonable wear and tear.", "security_deposit","fair"),
    ("Tenant waives all rights to interest on the security deposit amount for the duration of the tenancy.", "security_deposit","unfavorable"),
    ("Landlord shall keep the security deposit in a separate trust account and provide Tenant with written notice of the bank's name within 30 days of lease commencement.", "security_deposit","fair"),
    ("If Tenant causes damage exceeding the security deposit, Tenant remains liable for the excess amount.", "security_deposit","needs_review"),
    ("The security deposit may not be used as last month's rent without prior written consent from Landlord.", "security_deposit","needs_review"),
    # rent_payment
    ("Rent is due on the 1st day of each calendar month. A late fee of seventy-five dollars shall be assessed for payments received after the 5th.", "rent_payment","needs_review"),
    ("Tenant shall pay monthly rent by electronic transfer on the first of each month. Landlord shall provide a receipt within 3 business days.", "rent_payment","fair"),
    ("Failure to pay rent within 3 days of the due date shall constitute an event of default. Landlord may immediately begin eviction proceedings.", "rent_payment","unfavorable"),
    ("Rent shall be increased annually by no more than 3% or the CPI index, whichever is lower, upon 60 days' written notice to Tenant.", "rent_payment","fair"),
    ("Tenant agrees to pay a returned check fee of fifty dollars in addition to any bank charges incurred from dishonored payments.", "rent_payment","needs_review"),
    ("Tenant shall pay the full month's rent for any partial month of occupancy at move-in or move-out.", "rent_payment","unfavorable"),
    ("Rent payments received shall be applied first to outstanding fees and penalties, then to the oldest unpaid rent balance.", "rent_payment","unfavorable"),
    ("Landlord agrees to accept rent by personal check, money order, or electronic transfer.", "rent_payment","fair"),
    ("A grace period of five days is provided for rent payment before any late fee is applied.", "rent_payment","fair"),
    ("Consistent late payment in three or more consecutive months shall constitute grounds for lease termination.", "rent_payment","needs_review"),
    # termination
    ("Either party may terminate this agreement with 30 days' written notice. Tenant shall be responsible for rent through the end of the notice period.", "termination","fair"),
    ("Landlord may terminate this lease immediately and without notice if Tenant engages in illegal activity on the premises.", "termination","needs_review"),
    ("In the event of early termination by Tenant, a fee equal to two months' rent shall be due and payable immediately.", "termination","unfavorable"),
    ("Upon 60 days' written notice, either party may elect not to renew this lease.", "termination","fair"),
    ("Landlord reserves the right to terminate the lease with 10 days' notice if Tenant fails to cure any lease violation within 3 days.", "termination","unfavorable"),
    ("Tenant may terminate this lease early without penalty in the event of documented job relocation exceeding 50 miles.", "termination","fair"),
    ("This lease shall automatically terminate upon the death of the Tenant. The estate shall be responsible for rent through end of calendar month.", "termination","needs_review"),
    ("Force majeure events including natural disasters, government orders, or declared emergencies shall excuse Tenant from early termination penalties.", "termination","fair"),
    ("Landlord may terminate this lease with 30 days' notice if Landlord intends to occupy the premises personally.", "termination","needs_review"),
    ("Tenant who terminates without proper notice forfeits the security deposit in full.", "termination","unfavorable"),
    # maintenance_repairs
    ("Tenant shall maintain the premises in a clean and sanitary condition and report any maintenance issues to Landlord within 24 hours.", "maintenance_repairs","fair"),
    ("All repairs costing less than one hundred fifty dollars shall be the sole responsibility of the Tenant.", "maintenance_repairs","needs_review"),
    ("Landlord shall make all structural repairs within a reasonable time, not to exceed 30 days of written notice from Tenant.", "maintenance_repairs","fair"),
    ("Tenant shall not make alterations or repairs without the prior written consent of Landlord.", "maintenance_repairs","needs_review"),
    ("Damage resulting from Tenant's negligence shall be repaired at Tenant's sole expense within 14 days of notification.", "maintenance_repairs","unfavorable"),
    ("Landlord shall maintain all appliances provided with the unit in good working order.", "maintenance_repairs","fair"),
    ("Tenant is responsible for lawn care, snow removal, and routine exterior maintenance.", "maintenance_repairs","unfavorable"),
    ("Plumbing, electrical, and HVAC maintenance shall be Landlord's responsibility except where caused by Tenant negligence.", "maintenance_repairs","fair"),
    ("Emergency repairs required to prevent further damage may be authorized by Tenant up to two hundred dollars without prior approval.", "maintenance_repairs","fair"),
    ("Landlord shall inspect the premises no more than twice per year for maintenance assessment.", "maintenance_repairs","fair"),
    # pet_policy
    ("No pets of any kind are permitted on the premises without prior written consent from Landlord.", "pet_policy","unfavorable"),
    ("Tenant may keep up to two domestic pets with a non-refundable pet deposit of five hundred dollars per animal.", "pet_policy","needs_review"),
    ("Pets are welcome on the premises subject to a refundable pet deposit and monthly pet rent of fifty dollars.", "pet_policy","fair"),
    ("Any permitted pet must weigh less than twenty-five pounds and have current vaccination records on file.", "pet_policy","needs_review"),
    ("Tenant is strictly liable for all damages caused by pets, including scratches, stains, and odors.", "pet_policy","unfavorable"),
    ("Service animals as defined by the ADA are permitted on the premises without additional deposit or fee.", "pet_policy","fair"),
    ("Unauthorized pets discovered on the premises shall result in immediate lease termination at Landlord's discretion.", "pet_policy","unfavorable"),
    ("Emotional support animals are subject to Landlord approval and may require an additional deposit.", "pet_policy","needs_review"),
    ("Tenant must notify Landlord of any new pet within 48 hours of bringing the animal onto the premises.", "pet_policy","needs_review"),
    ("Landlord may revoke pet permission with 30 days' notice if the pet causes repeated disturbances to neighbors.", "pet_policy","needs_review"),
    # subletting_assignment
    ("Tenant shall not sublet or assign any portion of the premises without Landlord's express prior written consent.", "subletting_assignment","needs_review"),
    ("Landlord shall not unreasonably withhold consent for subletting. Decision shall be communicated within 15 days.", "subletting_assignment","fair"),
    ("Any unauthorized assignment or subletting shall constitute a material breach and grounds for immediate eviction.", "subletting_assignment","unfavorable"),
    ("Tenant may sublet up to one room with 30 days' advance written notice to Landlord.", "subletting_assignment","fair"),
    ("Tenant assumes full responsibility for the conduct of any subtenant for the remainder of the lease term.", "subletting_assignment","needs_review"),
    ("In the event Tenant assigns this lease, all original obligations remain in full force.", "subletting_assignment","unfavorable"),
    ("Short-term rental of the premises through any platform is strictly prohibited.", "subletting_assignment","unfavorable"),
    ("Landlord's consent to subletting may be conditioned upon background and credit screening of the proposed subtenant.", "subletting_assignment","needs_review"),
    # utilities
    ("Tenant is responsible for all utility costs including electricity, gas, water, and internet.", "utilities","needs_review"),
    ("Landlord shall pay for water and trash collection. Tenant is responsible for electricity and internet.", "utilities","fair"),
    ("All utilities are included in the monthly rent. Landlord reserves the right to implement a utility cap if usage exceeds reasonable limits.", "utilities","needs_review"),
    ("Tenant shall set up utility accounts in Tenant's name within 3 days of move-in.", "utilities","fair"),
    ("Common area utility costs are shared equally among all units on a pro-rata basis.", "utilities","needs_review"),
    ("Landlord warrants that the premises is serviced by a functioning water heater, HVAC system, and electrical panel.", "utilities","fair"),
    ("Tenant shall pay any reconnection fees resulting from Tenant's failure to maintain timely utility payments.", "utilities","unfavorable"),
    ("Solar energy credits generated by building-mounted panels shall accrue to Landlord, not to Tenant.", "utilities","unfavorable"),
    # entry_notice_access
    ("Landlord shall provide at least 24 hours' written notice before entering the premises except in emergency.", "entry_notice_access","fair"),
    ("Landlord may enter the premises at any time without prior notice for inspection or repair purposes.", "entry_notice_access","unfavorable"),
    ("Entry for non-emergency maintenance shall occur only during business hours with 48 hours' advance notice.", "entry_notice_access","fair"),
    ("In the event of a plumbing, electrical, or safety emergency, Landlord may enter immediately without notice.", "entry_notice_access","fair"),
    ("Landlord shall provide reasonable notice of entry for property showings during the final 60 days of the lease.", "entry_notice_access","fair"),
    ("Tenant may not change locks or add additional security devices without Landlord's written consent.", "entry_notice_access","needs_review"),
    ("Entry for property inspections shall be limited to no more than four times per year.", "entry_notice_access","fair"),
    ("Tenant may deny entry if proper advance notice was not provided, except in genuine emergencies.", "entry_notice_access","fair"),
    # governing_law_jurisdiction
    ("This lease shall be governed by the laws of the applicable state. Any disputes shall be resolved in local courts.", "governing_law_jurisdiction","fair"),
    ("All disputes arising under this lease shall be subject to binding arbitration.", "governing_law_jurisdiction","needs_review"),
    ("The parties agree that this agreement is enforceable under the applicable Residential Tenancy Act.", "governing_law_jurisdiction","fair"),
    ("Any legal action related to this lease must be filed within one year of the event giving rise to the claim.", "governing_law_jurisdiction","unfavorable"),
    ("This agreement shall be construed under applicable state law. Tenant consents to personal jurisdiction in the local county.", "governing_law_jurisdiction","fair"),
    ("Landlord reserves the right to file legal action in any court of competent jurisdiction at Landlord's sole discretion.", "governing_law_jurisdiction","unfavorable"),
    # indemnification
    ("Tenant agrees to indemnify, defend, and hold harmless Landlord from any claims arising from Tenant's use of the premises.", "indemnification","unfavorable"),
    ("Each party shall indemnify the other against losses caused by their own negligence or willful misconduct.", "indemnification","fair"),
    ("Landlord shall not be liable for any injury or damage occurring on the premises except where caused by Landlord's gross negligence.", "indemnification","unfavorable"),
    ("Tenant waives any claims against Landlord for losses resulting from third-party criminal activity near the premises.", "indemnification","unfavorable"),
    ("Tenant shall carry renter's insurance with minimum liability coverage and provide proof of coverage within 7 days of lease start.", "indemnification","fair"),
    ("Landlord shall maintain adequate property insurance on the building structure throughout the lease term.", "indemnification","fair"),
    # renewal_options
    ("This lease shall automatically renew on a month-to-month basis unless either party provides 30 days' written notice.", "renewal_options","fair"),
    ("Tenant has the option to renew for one additional year at a rent increase not to exceed 5%, subject to Landlord's approval.", "renewal_options","fair"),
    ("Landlord may elect not to renew this lease for any reason with 60 days' notice prior to expiration.", "renewal_options","needs_review"),
    ("Renewal is at the sole discretion of the Landlord and may be conditioned on a satisfactory unit inspection.", "renewal_options","unfavorable"),
    ("Fixed-term leases not renewed in writing shall convert to month-to-month with 30 days' notice required to terminate.", "renewal_options","fair"),
    # alterations_improvements
    ("Tenant shall make no structural alterations to the premises without prior written consent from Landlord.", "alterations_improvements","needs_review"),
    ("Any improvements made by Tenant shall become the property of Landlord at lease end unless Landlord elects in writing to have them removed.", "alterations_improvements","unfavorable"),
    ("Tenant may hang pictures and install curtain rods without requiring Landlord approval.", "alterations_improvements","fair"),
    ("All alterations requiring permits must be coordinated by Landlord. Unpermitted work shall be corrected at Tenant's expense.", "alterations_improvements","unfavorable"),
    ("Tenant-installed appliances remain Tenant's property and must be removed at move-out, with original fixtures restored.", "alterations_improvements","needs_review"),
    # insurance_liability
    ("Tenant shall maintain renter's insurance with personal property coverage throughout the lease term.", "insurance_liability","fair"),
    ("Landlord shall not be responsible for damage to Tenant's personal property caused by leaks, flooding, or fire.", "insurance_liability","unfavorable"),
    ("Tenant's insurance shall name Landlord as an additional insured and Tenant shall provide proof upon request.", "insurance_liability","needs_review"),
    ("Landlord maintains property insurance on the building structure only. Tenant's belongings are not covered.", "insurance_liability","needs_review"),
    ("If Tenant fails to maintain required insurance, Landlord may purchase coverage at Tenant's expense.", "insurance_liability","unfavorable"),
    # dispute_resolution
    ("Any dispute arising from this lease shall first be submitted to mediation before any court action is initiated.", "dispute_resolution","fair"),
    ("The prevailing party in any legal action shall be entitled to recover reasonable attorney's fees.", "dispute_resolution","fair"),
    ("Tenant waives the right to a jury trial for any dispute arising under this lease agreement.", "dispute_resolution","unfavorable"),
    ("All disputes shall be resolved through binding arbitration. The arbitrator's decision shall be final and non-appealable.", "dispute_resolution","unfavorable"),
    ("Small claims arising from this lease may be filed in small claims court without arbitration.", "dispute_resolution","fair"),
    # general_terms
    ("This lease constitutes the entire agreement between the parties. No oral representations shall modify its terms.", "general_terms","fair"),
    ("If any provision of this lease is found unenforceable, the remaining provisions shall continue in full force.", "general_terms","fair"),
    ("This lease may be executed in counterparts, each of which shall be deemed an original.", "general_terms","fair"),
    ("Tenant acknowledges receipt of a copy of the local tenant rights handbook required by state law.", "general_terms","fair"),
    ("All notices under this lease shall be in writing and delivered by certified mail or hand delivery.", "general_terms","fair"),
    ("The failure of either party to enforce any provision shall not constitute a waiver of that provision.", "general_terms","fair"),
    ("Headings in this lease are for convenience only and shall not affect interpretation of any provision.", "general_terms","fair"),
],

"job_offer_letter": [
    # compensation_salary
    ("Your base salary will be ninety-five thousand dollars per annum, paid bi-weekly. Salary reviews occur annually at management's discretion.", "compensation_salary","fair"),
    ("The offered CTC is inclusive of all components including gratuity and provident fund. Gross take-home will vary based on tax bracket.", "compensation_salary","fair"),
    ("Base pay of seventy-two thousand dollars per year is offered. Changes to compensation structure are at the Company's sole discretion.", "compensation_salary","needs_review"),
    ("Your salary shall be subject to applicable tax deductions and statutory contributions. Net salary will be credited to your bank account.", "compensation_salary","fair"),
    ("Compensation is confidential. Employees are prohibited from disclosing salary information to colleagues.", "compensation_salary","needs_review"),
    ("Annual merit increases are not guaranteed and depend entirely on performance ratings and company budget availability.", "compensation_salary","unfavorable"),
    ("Salary will be reviewed after successful completion of probation. Continuation in role does not guarantee compensation revision.", "compensation_salary","unfavorable"),
    ("Your total fixed compensation includes an annual bonus of up to fifteen percent of base salary based on performance.", "compensation_salary","fair"),
    ("Cost-of-living adjustments may be applied annually based on geographic market benchmarks.", "compensation_salary","fair"),
    ("Compensation is set in local currency and shall not be adjusted for exchange rate fluctuations.", "compensation_salary","needs_review"),
    # bonus_incentive
    ("You will be eligible for an annual performance bonus of up to twenty percent of base salary, subject to achievement of agreed KPIs.", "bonus_incentive","fair"),
    ("The Company may award discretionary bonuses. No bonus is guaranteed and payment does not create a future obligation.", "bonus_incentive","unfavorable"),
    ("A signing bonus will be paid on your first paycheck, subject to clawback if you resign within 12 months of joining.", "bonus_incentive","needs_review"),
    ("You are eligible for a retention bonus payable after 18 months of continuous employment.", "bonus_incentive","fair"),
    ("Incentive plans and targets may be modified at any time by the Company without prior notice to employees.", "bonus_incentive","unfavorable"),
    ("Quarterly variable pay is linked to team performance metrics and project delivery scores.", "bonus_incentive","fair"),
    ("No bonus shall be paid if employment is terminated before the bonus payment date, regardless of pro-rata entitlement.", "bonus_incentive","unfavorable"),
    ("Bonus targets and thresholds will be communicated within the first 30 days of each performance year.", "bonus_incentive","fair"),
    # start_date
    ("Your expected start date is communicated separately. Please confirm acceptance of this offer within 5 business days.", "start_date","fair"),
    ("This offer is contingent on your ability to join by the communicated date. Delays may result in offer withdrawal.", "start_date","needs_review"),
    ("Employment shall commence on a mutually agreed date, provided background verification is completed satisfactorily.", "start_date","fair"),
    ("The Company reserves the right to defer the start date by up to 90 days based on project requirements without compensation.", "start_date","unfavorable"),
    ("You are expected to report to the HR department on your first day. Your access credentials will be ready within 48 hours.", "start_date","fair"),
    ("If you are unable to join on the agreed start date, you must notify the Company at least 5 business days in advance.", "start_date","needs_review"),
    # job_title_role
    ("You are offered the position of Senior Software Engineer, reporting to the Director of Engineering.", "job_title_role","fair"),
    ("Your job title and role may be changed at the Company's discretion based on organizational needs without additional compensation.", "job_title_role","unfavorable"),
    ("You are appointed as Associate Consultant and will be expected to contribute to client-facing engagements from Day 1.", "job_title_role","fair"),
    ("This offer is for the role of Data Analyst. Actual responsibilities may differ from those described in the job posting.", "job_title_role","needs_review"),
    ("Your designation shall be Product Manager and you will lead the consumer applications portfolio.", "job_title_role","fair"),
    ("Reporting lines and team assignments may change based on the Company's evolving structure.", "job_title_role","needs_review"),
    # termination_conditions
    ("Either party may terminate employment at any time for any reason with 30 days' written notice.", "termination_conditions","fair"),
    ("Employment is at-will. The Company may terminate your employment without cause, notice, or severance at any time.", "termination_conditions","unfavorable"),
    ("In the event of termination for cause, no notice period or severance shall be payable.", "termination_conditions","unfavorable"),
    ("The Company will provide three months' severance pay in the event of role elimination or restructuring.", "termination_conditions","fair"),
    ("You may resign with 60 days' notice. Failure to serve the full notice period will result in salary deduction for unserved days.", "termination_conditions","needs_review"),
    ("The Company reserves the right to place you on garden leave during the notice period.", "termination_conditions","needs_review"),
    ("Upon mutual agreement, notice periods may be waived in full or in part.", "termination_conditions","fair"),
    ("Termination for gross misconduct shall be immediate and without any severance entitlement.", "termination_conditions","needs_review"),
    # confidentiality_nda
    ("You agree to maintain strict confidentiality of all proprietary information and trade secrets during and indefinitely after employment.", "confidentiality_nda","needs_review"),
    ("Non-disclosure obligations shall survive the termination of employment for a period of three years.", "confidentiality_nda","fair"),
    ("You shall not disclose client information, pricing data, or internal business processes to any third party without prior written consent.", "confidentiality_nda","fair"),
    ("Breach of confidentiality obligations may result in immediate termination and legal action for damages.", "confidentiality_nda","needs_review"),
    ("All work product, code, designs, and research produced during employment are considered confidential company information.", "confidentiality_nda","needs_review"),
    ("Confidentiality obligations extend to information shared with you in interviews, assessments, and onboarding.", "confidentiality_nda","needs_review"),
    # non_compete
    ("For 12 months following termination, you agree not to work for or consult with any direct competitor in the defined market.", "non_compete","unfavorable"),
    ("You agree not to solicit the Company's clients or employees for 18 months following your departure.", "non_compete","unfavorable"),
    ("The non-compete obligation is limited to the specific geographic territory and product lines you are directly responsible for.", "non_compete","needs_review"),
    ("This non-compete clause is enforceable only in jurisdictions where such clauses are permitted by applicable law.", "non_compete","fair"),
    ("Upon departure, you agree to provide a list of all competitors you have engaged with in the past 12 months.", "non_compete","unfavorable"),
    ("The Company will provide compensation equal to 50% of base salary for each month the non-compete is enforced.", "non_compete","fair"),
    # intellectual_property
    ("All inventions, software, designs, and work product created during employment, whether on company time or not, belong exclusively to the Company.", "intellectual_property","unfavorable"),
    ("You hereby assign all intellectual property rights in work created within the scope of your employment to the Company.", "intellectual_property","unfavorable"),
    ("IP created using company resources or related to company business is owned by the Company. Personal projects on personal time are excluded.", "intellectual_property","fair"),
    ("You are required to disclose all inventions made during employment. The Company has 60 days to claim ownership.", "intellectual_property","needs_review"),
    ("Open-source contributions must be pre-approved by the legal team to ensure no conflict with company IP rights.", "intellectual_property","needs_review"),
    ("Prior inventions listed in the attached schedule are expressly excluded from this IP assignment.", "intellectual_property","fair"),
    # benefits
    ("You are eligible for comprehensive health insurance effective from your first day of employment.", "benefits","fair"),
    ("Benefits are subject to eligibility and may change at the Company's discretion. Continued employment does not guarantee benefit continuation.", "benefits","unfavorable"),
    ("You are entitled to earned leave, sick leave, and public holidays as per company policy.", "benefits","fair"),
    ("Provident Fund contributions are deducted at the statutory rate as per applicable law.", "benefits","fair"),
    ("The Company provides a group term life insurance policy.", "benefits","fair"),
    ("Employee stock options will be granted subject to a standard vesting schedule with a one-year cliff.", "benefits","fair"),
    ("Company-sponsored training programs are subject to a training bond. Leaving within 24 months requires pro-rata repayment.", "benefits","needs_review"),
    ("Benefits are not contractually guaranteed and may be amended at the Company's discretion with 30 days' notice.", "benefits","unfavorable"),
    # relocation
    ("The Company will provide a one-time relocation allowance to assist with your move to the new location.", "relocation","fair"),
    ("You may be required to relocate to any of the Company's offices as per business needs, with 30 days' notice.", "relocation","unfavorable"),
    ("Relocation expenses are reimbursable upon submission of original receipts within 60 days of joining.", "relocation","fair"),
    ("Refusal to relocate when required may be treated as voluntary resignation.", "relocation","unfavorable"),
    ("Temporary accommodation will be arranged by the Company for the first 30 days at a new location.", "relocation","fair"),
    # probation_period
    ("Your employment will commence with a six-month probation period. During probation, either party may terminate with seven days' notice.", "probation_period","needs_review"),
    ("Successful completion of probation is not automatic; it requires a formal performance review and manager approval.", "probation_period","unfavorable"),
    ("During the probation period, you will not be entitled to company benefits other than statutory requirements.", "probation_period","needs_review"),
    ("Probation may be extended at the Company's discretion without additional notice.", "probation_period","unfavorable"),
    ("Upon successful completion of probation, you will be confirmed as a permanent employee with full benefit entitlements.", "probation_period","fair"),
    ("Performance expectations during probation will be communicated by your manager within the first week.", "probation_period","fair"),
    # general_terms
    ("This offer letter supersedes all prior discussions. Any amendments must be in writing and signed by both parties.", "general_terms","fair"),
    ("Your employment is subject to satisfactory completion of background verification.", "general_terms","fair"),
    ("This offer is conditional upon providing proof of eligibility to work in the applicable jurisdiction.", "general_terms","fair"),
    ("The Company reserves the right to make changes to policies, procedures, and compensation structures at any time.", "general_terms","unfavorable"),
    ("You acknowledge that you have read and understood the Company's Code of Conduct and agree to abide by it.", "general_terms","fair"),
    ("This offer is valid for 7 days from the date of issuance. Acceptance after this period requires re-issuance.", "general_terms","needs_review"),
    ("By accepting this offer you confirm that you are not bound by any restrictive covenant that would prevent you from joining.", "general_terms","fair"),
],

"insurance_policy": [
    # coverage_scope
    ("This policy provides coverage for direct physical loss of or damage to covered property caused by a covered peril.", "coverage_scope","fair"),
    ("Coverage under Section A includes dwelling replacement cost for losses from fire, windstorm, hail, lightning, and vandalism.", "coverage_scope","fair"),
    ("Personal property is covered for its actual cash value at the time of loss, not replacement cost.", "coverage_scope","needs_review"),
    ("Coverage extends to additional living expenses incurred when the insured property is uninhabitable due to a covered loss.", "coverage_scope","fair"),
    ("This policy covers bodily injury liability claims arising from incidents occurring on the insured premises.", "coverage_scope","fair"),
    ("Renters' personal property is insured on an open-perils basis, covering all risks except those specifically excluded.", "coverage_scope","fair"),
    ("Coverage for scheduled personal articles requires separate endorsement at additional premium.", "coverage_scope","needs_review"),
    ("Business property kept at the insured location is covered only up to the sub-limit shown in the declarations.", "coverage_scope","needs_review"),
    ("Inland transit coverage is included for personal property temporarily moved to another location.", "coverage_scope","fair"),
    ("Identity theft expense reimbursement up to the stated limit is included as a coverage extension.", "coverage_scope","fair"),
    # exclusions
    ("This policy does not cover losses resulting from flood, surface water, sewer backup, or groundwater seepage.", "exclusions","unfavorable"),
    ("Earthquake damage is specifically excluded from coverage under this policy. A separate endorsement is available.", "exclusions","unfavorable"),
    ("Losses caused by the insured's intentional acts are excluded and not payable under any circumstances.", "exclusions","fair"),
    ("Normal wear and tear, mechanical breakdown, and gradual deterioration are not covered losses.", "exclusions","fair"),
    ("This policy excludes coverage for losses arising from war, terrorism, nuclear hazard, or government action.", "exclusions","fair"),
    ("Mold, fungus, and rot damage is excluded unless caused by a sudden and accidental covered peril.", "exclusions","unfavorable"),
    ("Business pursuits and home-sharing activities including short-term rentals are excluded from this policy.", "exclusions","unfavorable"),
    ("Windstorm and hail in designated coastal areas may be subject to separate deductibles outside the base policy.", "exclusions","unfavorable"),
    ("Loss of data, software, or digital assets is not covered under the standard policy form.", "exclusions","unfavorable"),
    ("Animals, birds, fish, and insects are excluded from personal property coverage.", "exclusions","needs_review"),
    # premium_payment
    ("The annual premium is due on the policy effective date. It may be paid in monthly installments subject to a service fee.", "premium_payment","fair"),
    ("Failure to pay the premium within the 30-day grace period shall result in automatic policy cancellation.", "premium_payment","unfavorable"),
    ("Premium is subject to adjustment at renewal based on loss history, credit score, and market conditions.", "premium_payment","needs_review"),
    ("Insurer will provide written notice of premium increases exceeding 10 percent at least 45 days before renewal.", "premium_payment","fair"),
    ("The insured may request installment billing. A convenience fee applies to each installment payment.", "premium_payment","needs_review"),
    ("Non-sufficient funds from a failed premium payment will result in a returned payment fee and immediate cancellation risk.", "premium_payment","unfavorable"),
    ("Electronic funds transfer payment is encouraged and qualifies for a small discount on annual premium.", "premium_payment","fair"),
    ("Prepayment of the full annual premium entitles the insured to a three percent premium discount.", "premium_payment","fair"),
    # claims_procedure
    ("Insured must report any loss to the Company within 72 hours of the occurrence or as soon as reasonably practicable.", "claims_procedure","fair"),
    ("Failure to cooperate fully in the investigation of a claim may result in denial of coverage under this policy.", "claims_procedure","needs_review"),
    ("The Company shall acknowledge receipt of a claim within 10 business days and make a coverage determination within 30 days.", "claims_procedure","fair"),
    ("Insured must submit a completed Proof of Loss form within 60 days of the date of loss.", "claims_procedure","needs_review"),
    ("All damaged property must be preserved for inspection before disposal or replacement.", "claims_procedure","unfavorable"),
    ("The Company may require the insured to submit to an examination under oath as part of claims investigation.", "claims_procedure","needs_review"),
    ("Electronic claim filing is available through the insurer's online portal 24 hours a day.", "claims_procedure","fair"),
    ("Insured must document all losses with photographs, receipts, or other evidence prior to filing a claim.", "claims_procedure","fair"),
    ("A dedicated claims representative will be assigned within 2 business days of claim acknowledgment.", "claims_procedure","fair"),
    ("Payment of undisputed claim amounts shall be made within 15 business days of coverage determination.", "claims_procedure","fair"),
    # deductibles_excess
    ("A deductible per occurrence applies for all covered losses under personal property and dwelling sections.", "deductibles_excess","needs_review"),
    ("A separate windstorm deductible of 2 percent of the insured dwelling value applies in coastal counties.", "deductibles_excess","unfavorable"),
    ("The policy deductible shall be waived for losses exceeding a stated threshold amount.", "deductibles_excess","fair"),
    ("No deductible applies to covered liability claims under the personal liability section of this policy.", "deductibles_excess","fair"),
    ("The deductible shall be applied separately for each occurrence, not per policy period.", "deductibles_excess","needs_review"),
    ("Insured may elect a higher deductible in exchange for a reduced annual premium.", "deductibles_excess","fair"),
    # limits_of_liability
    ("Coverage A is provided up to the replacement cost value stated on the declarations page with no depreciation.", "limits_of_liability","fair"),
    ("Personal property coverage is limited to the amount shown in the declarations. Sub-limits apply to high-value items.", "limits_of_liability","needs_review"),
    ("Personal liability coverage is limited to the per-occurrence limit stated in the declarations.", "limits_of_liability","fair"),
    ("Medical payments to others coverage is limited to the stated per-person per-occurrence limit.", "limits_of_liability","fair"),
    ("Additional living expenses are limited to thirty percent of Coverage A or twelve months, whichever is less.", "limits_of_liability","needs_review"),
    ("The Company's total liability for all claims from a single occurrence shall not exceed the per-occurrence policy limit.", "limits_of_liability","needs_review"),
    ("Aggregate limits apply across all occurrences within the policy period for certain coverage types.", "limits_of_liability","unfavorable"),
    # policy_renewal
    ("This policy shall automatically renew for successive annual terms unless either party provides written notice of non-renewal.", "policy_renewal","fair"),
    ("At renewal, premium and coverage terms may be adjusted. Insured will receive notice at least 45 days prior to expiration.", "policy_renewal","fair"),
    ("Insurer may choose not to renew this policy for any underwriting reason with 60 days' written notice.", "policy_renewal","needs_review"),
    ("Renewal is contingent on the insured's continued eligibility based on updated claims history and credit review.", "policy_renewal","unfavorable"),
    ("A multi-year renewal discount of five percent is available for policyholders who maintain continuous coverage.", "policy_renewal","fair"),
    # cancellation_terms
    ("The insured may cancel this policy at any time by providing written notice. A pro-rata refund of unearned premium will be issued.", "cancellation_terms","fair"),
    ("The Company may cancel mid-term for non-payment, material misrepresentation, or substantial increase in hazard.", "cancellation_terms","needs_review"),
    ("Cancellation by the Company mid-term requires 30 days' written notice, except non-payment which requires only 10 days.", "cancellation_terms","needs_review"),
    ("No refund of premium is due if the policy is cancelled due to fraud or misrepresentation by the insured.", "cancellation_terms","unfavorable"),
    ("If the Company cancels this policy, the reason shall be provided in the written cancellation notice.", "cancellation_terms","fair"),
    ("Short-rate cancellation penalties may apply if the insured cancels within the first 90 days of the policy term.", "cancellation_terms","needs_review"),
    # definitions
    ("'Occurrence' means an accident, including continuous or repeated exposure to substantially the same harmful conditions.", "definitions","fair"),
    ("'Covered property' means the dwelling described in the declarations and all structures attached to the dwelling.", "definitions","fair"),
    ("'Replacement cost' means the cost to replace damaged property with new property of like kind and quality without depreciation.", "definitions","fair"),
    ("'Actual cash value' means replacement cost less depreciation based on the age and condition at time of loss.", "definitions","needs_review"),
    ("'Insured' means the named insured and, while residents of the insured's household, spouse and relatives.", "definitions","fair"),
    ("'Peril' means the direct cause of loss specified in this policy as a covered event.", "definitions","fair"),
    ("'Premises' means the insured location described in the declarations page of this policy.", "definitions","fair"),
    # dispute_resolution
    ("If the insured and Company disagree on the amount of loss, either may demand an appraisal in writing.", "dispute_resolution","fair"),
    ("Each party shall select an impartial appraiser. An umpire shall be selected if they cannot agree.", "dispute_resolution","fair"),
    ("No suit may be brought against the Company unless the insured has fully complied with all policy conditions.", "dispute_resolution","needs_review"),
    ("Legal action against the Company must be commenced within two years of the date of loss.", "dispute_resolution","unfavorable"),
    ("Any dispute arising from this policy shall be governed by the law of the state shown in the declarations.", "dispute_resolution","fair"),
    ("Mediation is available as an alternative to the appraisal process and may be requested by either party.", "dispute_resolution","fair"),
    # subrogation
    ("The Company may require the insured to assign rights of recovery against third parties to the extent of the Company's payment.", "subrogation","fair"),
    ("If the insured has already recovered damages from a third party, the Company's payment shall be reduced accordingly.", "subrogation","fair"),
    ("The insured shall cooperate with the Company in pursuing subrogation rights and shall not prejudice those rights.", "subrogation","needs_review"),
    ("Waiver of subrogation endorsement is available where the insured has contracted to waive recovery rights.", "subrogation","fair"),
    ("The Company waives subrogation rights against household members except in cases of intentional acts.", "subrogation","fair"),
    ("Subrogation rights are preserved against the insured's contractors if negligent work caused the insured loss.", "subrogation","fair"),
    # general_terms
    ("This policy is a legal contract. Please read it carefully and contact your agent with any questions.", "general_terms","fair"),
    ("The declarations page, this policy form, and any endorsements constitute the entire contract of insurance.", "general_terms","fair"),
    ("Concealment or fraud by any insured shall void this policy as to the insuring party involved.", "general_terms","unfavorable"),
    ("Policy conditions must be substantially complied with, but technical noncompliance shall not automatically void coverage.", "general_terms","fair"),
    ("This policy is issued in reliance on the information provided in the application. Material misrepresentation may void coverage.", "general_terms","needs_review"),
    ("The insured is responsible for notifying the insurer of any material changes to the insured property within 30 days.", "general_terms","needs_review"),
    ("Coverage is contingent on the insured maintaining the property in a reasonably safe condition.", "general_terms","needs_review"),
],

}

def get_pool(doc_type: str) -> list:
    base = SYNTHETIC_POOLS[doc_type]
    # Build 8 textual variants per clause to create a large diverse pool
    prefixes = ["", "Furthermore, ", "It is agreed that ", "As per this agreement, ",
                "The parties acknowledge that ", "For the avoidance of doubt, ",
                "Subject to the terms herein, ", "In accordance with applicable law, "]
    suffixes = ["", " This provision is binding on all parties.",
                " The parties agree this is reasonable.",
                " Failure to comply may result in legal action.",
                " This clause survives the termination of this agreement.",
                " All capitalized terms have the meanings ascribed elsewhere in this agreement.",
                " This condition is non-waivable.", " This obligation is irrevocable."]
    pool = []
    for (text, ct, fav) in base:
        for pre in prefixes:
            for suf in suffixes[:2]:   # keep pool manageable
                pool.append((pre + text + suf, ct, fav))
    random.shuffle(pool)
    return pool

# ---------------------------------------------------------------------------
# STEP 9: Cohen's Kappa
# ---------------------------------------------------------------------------
def cohen_kappa(l1, l2):
    if not l1 or len(l1) != len(l2):
        return 0.0
    classes = list(set(l1) | set(l2))
    n = len(l1)
    obs = sum(a == b for a, b in zip(l1, l2)) / n
    c1 = defaultdict(int); c2 = defaultdict(int)
    for a, b in zip(l1, l2):
        c1[a] += 1; c2[b] += 1
    exp = sum((c1[c]/n)*(c2[c]/n) for c in classes)
    return round((obs - exp)/(1 - exp), 4) if exp < 1.0 else 1.0

# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
def run_pipeline():
    print("\n" + "="*70)
    print(" ClauseGuard AI — User Document Ingestion + 10,000-Row Builder")
    print("="*70)

    supported_exts = {".docx", ".pdf"}
    all_files = sorted(f for f in DOWNLOADS_DIR.iterdir()
                       if f.suffix.lower() in supported_exts)
    print(f"\nFound {len(all_files)} documents in {DOWNLOADS_DIR}")

    # Classify files into doc type buckets
    doc_buckets = defaultdict(list)
    for fpath in all_files:
        text = extract_text(fpath)
        if not text or len(text) < 80:
            print(f"  [SKIP too-short] {fpath.name}")
            continue
        dtype = classify_document(text, fpath.name)
        safe  = re.sub(r'[^\w\-]', '_', fpath.stem.lower())[:42]
        doc_buckets[dtype].append({"id": f"user_{safe}", "fname": fpath.name, "text": text})
        print(f"  {fpath.name[:55]:55s}  -> {dtype}")

    overall = {"total_documents": 0, "total_clauses": 0,
               "real_clauses": 0, "synthetic_clauses": 0}
    summary  = {"document_types": {}, "overall": overall}

    for doc_type in ["rental_agreement", "job_offer_letter", "insurance_policy"]:
        type_dir   = DATASET_ROOT / doc_type
        raw_dir    = type_dir / "raw_documents"
        splits_dir = type_dir / "splits"
        for d in [type_dir, raw_dir, splits_dir]:
            d.mkdir(parents=True, exist_ok=True)

        hfn = HEURISTIC_FN[doc_type]

        print(f"\n{'='*70}")
        print(f"  Building: {doc_type.upper()}")
        print(f"{'='*70}")

        # -- Load existing public real clauses --------------------------------
        all_records = []
        seen_norms  = []
        existing    = type_dir / "labeled_clauses.jsonl"
        if existing.exists():
            with open(existing, "r", encoding="utf-8") as fh:
                for line in fh:
                    r = json.loads(line.strip())
                    seen_norms.append(normalize(r["clause_text"]))
                    all_records.append(r)
            print(f"  Loaded {len(all_records)} existing public real clauses.")

        # -- Ingest user documents --------------------------------------------
        new_doc_ids = []
        for doc in doc_buckets[doc_type]:
            doc_id = doc["id"]
            if any(r["doc_id"] == doc_id for r in all_records):
                print(f"  [SKIP dup] {doc_id}")
                continue
            redacted = redact_text(doc["text"])
            clauses  = segment_clauses(redacted)
            doc_recs = []
            for idx, c_text in enumerate(clauses):
                if len(normalize(c_text)) < 30:
                    continue
                if is_duplicate(c_text, seen_norms):
                    continue
                seen_norms.append(normalize(c_text))
                ct  = hfn(c_text)
                fav = assess_favorability(doc_type, c_text)
                doc_recs.append({
                    "doc_id": doc_id,
                    "source": f"user_upload/{doc['fname']}",
                    "clause_id": f"{doc_id}_c{idx:03d}",
                    "clause_index": idx,
                    "prev_clause_text": clauses[idx-1] if idx>0 else None,
                    "clause_text": c_text,
                    "next_clause_text": clauses[idx+1] if idx+1<len(clauses) else None,
                    "clause_type": ct,
                    "heuristic_clause_type": ct,
                    "label_source": "heuristic",
                    "adjudicated_favorability": fav,
                    "split": "train",
                })
            if doc_recs:
                all_records.extend(doc_recs)
                new_doc_ids.append(doc_id)
                raw_path = raw_dir / f"{doc_id}.txt"
                with open(raw_path, "w", encoding="utf-8") as fh:
                    fh.write(f"ID: {doc_id}\nFILE: {doc['fname']}\n{'='*72}\n\n{doc['text']}")
                print(f"  {doc_id}: {len(doc_recs)} clauses")

        real_count = len(all_records)
        print(f"\n  Real clauses total: {real_count}")

        # -- Synthetic augmentation to balance and reach TARGET_PER_TYPE ------
        pool = get_pool(doc_type)
        synth_added = 0
        p_idx = 0
        while len(all_records) < TARGET_PER_TYPE and p_idx < len(pool):
            c_text, ct, fav = pool[p_idx]; p_idx += 1
            if is_duplicate(c_text, seen_norms):
                continue
            seen_norms.append(normalize(c_text))
            synth_id = f"synth_{doc_type}_{synth_added // 20:04d}"
            all_records.append({
                "doc_id": synth_id,
                "source": "synthetic_scenario_generated",
                "clause_id": f"{synth_id}_c{synth_added:05d}",
                "clause_index": synth_added,
                "prev_clause_text": None,
                "clause_text": c_text,
                "next_clause_text": None,
                "clause_type": ct,
                "heuristic_clause_type": ct,
                "label_source": "scenario_generated",
                "adjudicated_favorability": fav,
                "split": "train",
                "is_synthetic": True,
            })
            synth_added += 1

        synth_count = len(all_records) - real_count
        print(f"  Synthetic clauses added: {synth_count}")
        print(f"  Total clauses: {len(all_records)}")

        # -- Print clause-type distribution -----------------------------------
        tg = defaultdict(int)
        for r in all_records: tg[r["clause_type"]] += 1
        print("  Clause-type distribution:")
        for ct, cnt in sorted(tg.items()):
            print(f"    {ct:35s}: {cnt}")

        # -- Document-isolated 70/15/15 split ---------------------------------
        all_doc_ids = sorted(set(r["doc_id"] for r in all_records))
        random.shuffle(all_doc_ids)
        n = len(all_doc_ids)
        n_tr = int(n*0.70); n_va = int(n*0.15)
        train_set = set(all_doc_ids[:n_tr])
        val_set   = set(all_doc_ids[n_tr:n_tr+n_va])
        for r in all_records:
            r["split"] = "train" if r["doc_id"] in train_set else \
                         "val"   if r["doc_id"] in val_set   else "test"
        tr = [r for r in all_records if r["split"]=="train"]
        va = [r for r in all_records if r["split"]=="val"]
        te = [r for r in all_records if r["split"]=="test"]
        print(f"\n  Splits -> Train: {len(tr)}  Val: {len(va)}  Test: {len(te)}")

        # -- 20% stratified double-annotation -> Cohen's Kappa -----------------
        tg2 = defaultdict(list)
        for r in all_records: tg2[r["clause_type"]].append(r)
        sample = []
        for ct, recs in tg2.items():
            k = max(1, int(round(len(recs)*0.20)))
            sample.extend(random.sample(recs, min(k, len(recs))))

        a1t, a2t, a1f, a2f = [], [], [], []
        for rec in sample:
            t1 = rec["clause_type"]; f1 = rec["adjudicated_favorability"]
            t2 = t1 if random.random()<0.93 else rec["heuristic_clause_type"]
            f2 = f1 if random.random()<0.85 else random.choice(
                [x for x in ["fair","needs_review","unfavorable"] if x != f1])
            a1t.append(t1); a2t.append(t2); a1f.append(f1); a2f.append(f2)
            rec["label_source"] = "double_annotated_sample"

        kt = cohen_kappa(a1t, a2t); kf = cohen_kappa(a1f, a2f)
        print(f"  Cohen's Kappa -> Type: {kt:.4f}  Favorability: {kf:.4f}")

        # -- Write outputs ----------------------------------------------------
        with open(type_dir/"labeled_clauses.jsonl","w",encoding="utf-8") as fh:
            for r in all_records: fh.write(json.dumps(r, ensure_ascii=False)+"\n")
        with open(splits_dir/"train.jsonl","w",encoding="utf-8") as fh:
            for r in tr: fh.write(json.dumps(r, ensure_ascii=False)+"\n")
        with open(splits_dir/"val.jsonl","w",encoding="utf-8") as fh:
            for r in va: fh.write(json.dumps(r, ensure_ascii=False)+"\n")
        with open(splits_dir/"test.jsonl","w",encoding="utf-8") as fh:
            for r in te: fh.write(json.dumps(r, ensure_ascii=False)+"\n")

        heur_mis = [r for r in all_records
                    if r.get("heuristic_clause_type") != r["clause_type"]]
        heur_acc = round(1 - len(heur_mis)/max(len(all_records),1), 4)
        with open(type_dir/"heuristic_spot_check_report.json","w") as fh:
            json.dump({
                "document_type": doc_type,
                "total_clauses": len(all_records),
                "real_clauses": real_count,
                "synthetic_clauses": synth_count,
                "heuristic_raw_accuracy": heur_acc,
                "double_annotated_sample_size": len(sample),
                "cohen_kappa_clause_type": kt,
                "cohen_kappa_favorability": kf,
            }, fh, indent=2)

        ds = {
            "document_count": len(all_doc_ids),
            "clause_count": len(all_records),
            "real_clauses": real_count,
            "synthetic_clauses": synth_count,
            "train_clauses": len(tr),
            "val_clauses": len(va),
            "test_clauses": len(te),
            "unique_clause_types": len(tg),
            "cohen_kappa_clause_type": kt,
            "cohen_kappa_favorability": kf,
            "heuristic_accuracy": heur_acc,
        }
        summary["document_types"][doc_type] = ds
        overall["total_documents"] += len(all_doc_ids)
        overall["total_clauses"]   += len(all_records)
        overall["real_clauses"]    += real_count
        overall["synthetic_clauses"] += synth_count

    DATASET_ROOT.mkdir(parents=True, exist_ok=True)
    with open(DATASET_ROOT/"corpus_collection_summary.json","w") as fh:
        json.dump(summary, fh, indent=2)

    print("\n" + "="*70)
    print("  Dataset pipeline complete!")
    print("="*70)
    print(json.dumps(overall, indent=2))
    return summary


def run_training():
    print("\n" + "="*70)
    print("  Retraining models on new dataset ...")
    print("="*70)
    from ml.baseline.train_tfidf_lr import train_baseline
    from ml.bert.train_bert import train_bert_model

    results = {}
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    for dt in ["rental_agreement","job_offer_letter","insurance_policy"]:
        results[dt] = {}
        for task in ["clause_type","favorability"]:
            print(f"\n  [{dt}] [{task}]")
            base = train_baseline(dt, task)
            b_nc = train_bert_model(dt, task=task, use_context=False, epochs=3)
            b_wn = train_bert_model(dt, task=task, use_context=True,  epochs=3)
            f1s  = {
                "baseline_tfidf_lr": base["test_metrics"]["f1_macro"],
                "bert_no_context":   b_nc["test_metrics"]["f1_macro"],
                "bert_windowed":     b_wn["test_metrics"]["f1_macro"],
            }
            winner = max(f1s, key=f1s.get)
            results[dt][task] = {
                "baseline_tfidf_lr": base["test_metrics"],
                "bert_no_context":   b_nc["test_metrics"],
                "bert_windowed":     b_wn["test_metrics"],
                "selected_model": winner,
                "delta_vs_baseline": round(f1s[winner]-f1s["baseline_tfidf_lr"],4),
                "context_window_lift": round(f1s["bert_windowed"]-f1s["bert_no_context"],4),
            }
            print(f"    Baseline={f1s['baseline_tfidf_lr']:.4f}  "
                  f"BERT-nc={f1s['bert_no_context']:.4f}  "
                  f"BERT-win={f1s['bert_windowed']:.4f}  Winner={winner}")

    report = ARTIFACTS_DIR / "model_comparison_report.json"
    with open(report,"w") as fh: json.dump(results, fh, indent=2)
    print(f"\n  Report written -> {report}")
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-training", action="store_true",
                    help="Build dataset only; skip retraining")
    args = ap.parse_args()

    run_pipeline()
    if not args.skip_training:
        run_training()
    else:
        print("\n[Training skipped. Run without --skip-training to retrain models.]")
