import re
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ml.dataset_corpus_data import RENTAL_SOURCES
from ml.dataset_corpus_offer import OFFER_SOURCES
from ml.dataset_corpus_insurance import INSURANCE_SOURCES

# 1. RENTAL ENRICHMENT
# For rental documents 5 to 25, add standard clauses if not already present
rental_enrichments = {
    "wa_seattle_housing_lease_05": [
        ("SECTION 10: LATE PAYMENT CHARGES\nIf monthly rent is not received by the fifth (5th) day of the month, Tenant shall pay a late charge not to exceed $10.00 in strict accordance with the Seattle Municipal Code.", "late_fees_penalty", "fair"),
        ("SECTION 11: ALTERATIONS AND FIXTURES\nTenant shall make no alterations, painting, or physical modifications without Landlord's prior written approval. Unauthorized alterations must be restored at Tenant's expense.", "alterations_improvements", "fair"),
        ("SECTION 12: RENTER'S LIABILITY INSURANCE\nTenant is strongly advised to maintain a renter's insurance policy covering personal property and tenant liability up to $100,000.00.", "insurance_liability", "fair"),
        ("SECTION 13: INDEMNIFICATION\nTenant agrees to defend and indemnify Landlord from and against claims and damages arising solely from Tenant's own negligence or intentional misconduct on the premises.", "indemnification", "fair"),
        ("SECTION 14: DISPUTE RESOLUTION AND MEDIATION\nParties agree to seek resolution through the City of Seattle Housing Dispute Resolution Center before initiating eviction litigation in court.", "dispute_resolution", "fair"),
        ("SECTION 15: LEASE RENEWAL\nUnless terminated for just cause with statutory 60-day notice, this lease shall automatically continue on a month-to-month basis at the end of the term.", "renewal_auto_renewal", "fair"),
    ],
    "ma_legalservices_lease_06": [
        ("CLAUSE 10: LATE FEE LIMITATIONS (M.G.L. c. 186 s. 15B)\nNo late fee or penalty may be assessed unless rent remains unpaid for thirty (30) full days after the due date. Any late fee assessed after 30 days shall not exceed $35.00.", "late_fees_penalty", "fair"),
        ("CLAUSE 11: ALTERATIONS AND PAINTING\nTenant shall make no structural alterations, painting, or wallpapering without prior written consent of Landlord.", "alterations_improvements", "fair"),
        ("CLAUSE 12: TENANT PROPERTY INSURANCE\nLandlord's property insurance does not insure Tenant's personal belongings against theft, fire, or water damage. Tenant is advised to procure renter's insurance.", "insurance_liability", "fair"),
        ("CLAUSE 13: UTILITIES ALLOCATION\nTenant pays separately metered electricity and heating gas. Landlord pays cold water, municipal sewerage, and trash collection pursuant to the State Sanitary Code.", "utilities", "fair"),
        ("CLAUSE 14: DISPUTE RESOLUTION\nParties may submit controversies to mediation through the Massachusetts Housing Court Alternative Dispute Resolution Department.", "dispute_resolution", "fair"),
        ("CLAUSE 15: MONTH-TO-MONTH EXTENSION\nUpon term expiration, this agreement converts to a month-to-month tenancy terminable by thirty (30) days written notice.", "renewal_auto_renewal", "fair"),
    ],
    "co_boulder_model_lease_07": [
        ("SECTION 10: LATE FEES AND BOULDER ORDINANCE\nIf rent is not paid by the 7th of the month, a reasonable administrative fee of $35.00 shall be assessed. No daily compounding charges shall apply.", "late_fees_penalty", "fair"),
        ("SECTION 11: PREMISES ALTERATIONS\nTenant shall not paint walls, drill into masonry, or install permanent fixtures without advance written permission from Landlord.", "alterations_improvements", "fair"),
        ("SECTION 12: TENANT INSURANCE\nTenant is encouraged to maintain renter's insurance covering personal property and premises liability up to $100,000.00.", "insurance_liability", "fair"),
        ("SECTION 13: INDEMNIFICATION RESTRICTIONS\nTenant indemnifies Landlord against liabilities resulting directly from the negligent acts or omissions of Tenant or Tenant's invitees.", "indemnification", "fair"),
        ("SECTION 14: AUTOMATIC RENEWAL TERMS\nThis lease shall automatically renew on a month-to-month basis at the end of the term unless sixty (60) days advance written notice of non-renewal is provided.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by the laws of the State of Colorado and the municipal code of the City of Boulder.", "governing_law_jurisdiction", "fair"),
    ],
    "umich_housing_lease_08": [
        ("10. LATE FEES AND DELINQUENCY\nRent unpaid by the 6th day of the month shall incur a $25.00 late charge. Landlord shall not assess daily late charges.", "late_fees_penalty", "fair"),
        ("11. ALTERATIONS RESTRICTION\nTenant shall make no modifications or alterations to the dwelling unit without written authorization from Wolverine Management.", "alterations_improvements", "fair"),
        ("12. RENTER'S INSURANCE\nTenant is required to maintain a renter's insurance policy throughout the academic term with personal liability coverage of at least $100,000.00.", "insurance_liability", "fair"),
        ("13. INDEMNITY\nTenant agrees to hold Landlord harmless from losses arising out of Tenant's own negligence or breach of lease rules.", "indemnification", "fair"),
        ("14. DISPUTE RESOLUTION\nParties agree to explore mediation through University of Michigan Student Legal Services before commencing court litigation in Washtenaw County.", "dispute_resolution", "fair"),
        ("15. AUTOMATIC EXTENSION\nLease expires August 10, 2025, and does not automatically renew unless both parties execute an extension addendum 60 days in advance.", "renewal_auto_renewal", "fair"),
    ],
    "uw_madison_sls_lease_09": [
        ("9. LATE CHARGE PROVISIONS\nA late payment fee of $30.00 will be assessed if rent is not received by 5:00 PM on the 5th day of the month.", "late_fees_penalty", "fair"),
        ("10. ALTERATION RULES\nTenant shall not paint, refinish floors, or make structural additions without Landlord's advance written consent.", "alterations_improvements", "fair"),
        ("11. INSURANCE REQUIREMENT\nTenant is advised and required to secure renter's insurance covering personal liability and property loss.", "insurance_liability", "fair"),
        ("12. INDEMNITY OBLIGATIONS\nTenant agrees to indemnify Landlord from claims arising solely from negligent acts committed by Tenant or Tenant's guests on the premises.", "indemnification", "fair"),
        ("13. DISPUTE RESOLUTION\nParties may utilize the Tenant Resource Center mediation service to resolve landlord-tenant disputes informally.", "dispute_resolution", "fair"),
        ("14. AUTOMATIC EXTENSION AND RENEWAL\nThis lease expires on August 14, 2025, and requires sixty (60) days advance written notice of renewal or termination.", "renewal_auto_renewal", "fair"),
        ("15. GOVERNING LAW\nGoverned by the laws of the State of Wisconsin and Dane County ordinances.", "governing_law_jurisdiction", "fair"),
    ],
    "uc_berkeley_sls_lease_10": [
        ("CLAUSE 9: LATE PAYMENT CHARGES\nIf rent is not received by the 5th calendar day of the month, a reasonable administrative fee of $35.00 shall be assessed.", "late_fees_penalty", "fair"),
        ("CLAUSE 10: ALTERATIONS RESTRICTION\nTenant shall make no structural alterations, painting, or lock changes without prior written approval of Landlord.", "alterations_improvements", "fair"),
        ("CLAUSE 11: RENTER'S INSURANCE\nTenant is advised to maintain renter's insurance with at least $100,000.00 liability protection during tenancy.", "insurance_liability", "fair"),
        ("CLAUSE 12: INDEMNIFICATION\nTenant agrees to indemnify Landlord from claims resulting from Tenant's negligent acts or omissions on the property.", "indemnification", "fair"),
        ("CLAUSE 13: UTILITY BILLING\nTenant is responsible for PG&E gas and electric services. Landlord pays municipal water, trash, and sewer.", "utilities", "fair"),
        ("CLAUSE 14: LEASE RENEWAL AND EXTENSION\nUpon expiration of the term, this tenancy continues month-to-month under Berkeley Rent Stabilization Ordinance provisions.", "renewal_auto_renewal", "fair"),
        ("CLAUSE 15: GOVERNING LAW\nGoverned by the laws of California and the City of Berkeley Rent Stabilization Ordinance.", "governing_law_jurisdiction", "fair"),
    ],
    "unc_chapelhill_sls_lease_11": [
        ("SECTION 9: LATE PAYMENT CHARGES\nUnder NCGS 42-46, a late fee of $15.00 or 5% of monthly rent shall be assessed if rent is late by five days or more.", "late_fees_penalty", "fair"),
        ("SECTION 10: PROPERTY ALTERATIONS\nTenant shall not paint, wallpaper, or make physical alterations without Landlord's written authorization.", "alterations_improvements", "fair"),
        ("SECTION 11: RENTER'S INSURANCE POLICY\nTenant is required to maintain an active renter's insurance policy with $100,000.00 personal liability coverage.", "insurance_liability", "fair"),
        ("SECTION 12: INDEMNIFICATION\nTenant indemnifies Landlord against claims caused by Tenant's own negligence or breach of tenancy terms.", "indemnification", "fair"),
        ("SECTION 13: DISPUTE MEDIATION\nParties agree to seek resolution through the Orange County Dispute Settlement Center prior to initiating judicial proceedings.", "dispute_resolution", "fair"),
        ("SECTION 14: AUTOMATIC EXTENSION\nTenancy converts to month-to-month upon expiration unless terminated with 30 days written notice.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by North Carolina law and the North Carolina Residential Rental Agreements Act.", "governing_law_jurisdiction", "fair"),
    ],
    "cornell_offcampus_lease_12": [
        ("9. LATE FEES (RPL 238-a)\nPursuant to NY Real Property Law Section 238-a, late fees are capped at $50.00 or 5% of rent after a 5-day grace period.", "late_fees_penalty", "fair"),
        ("10. ALTERATIONS AND PAINTING\nTenant shall make no modifications or alterations to walls or structural components without Landlord's written consent.", "alterations_improvements", "fair"),
        ("11. RENTER'S INSURANCE\nTenant is strongly advised to maintain personal property and liability insurance up to $100,000.00.", "insurance_liability", "fair"),
        ("12. INDEMNITY ALLOCATION\nTenant indemnifies Landlord against liability resulting from Tenant's negligence or intentional misconduct.", "indemnification", "fair"),
        ("13. UTILITIES AND SERVICES\nTenant pays NYSEG electric and gas. Landlord pays City of Ithaca water, sewer, and regular refuse collection.", "utilities", "fair"),
        ("14. DISPUTE RESOLUTION\nParties may submit disputes to mediation through the Community Dispute Resolution Center of Tompkins County.", "dispute_resolution", "fair"),
        ("15. AUTOMATIC EXTENSION\nLease term ends July 31, 2025. Any renewal must be agreed upon in writing at least 60 days before expiration.", "renewal_auto_renewal", "fair"),
    ],
    "nys_ag_tenants_rights_lease_13": [
        ("ARTICLE 9: ALTERATIONS AND FIXTURES\nTenant shall not make structural modifications, paint, or install major appliances without Landlord's advance written consent.", "alterations_improvements", "fair"),
        ("ARTICLE 10: RENTER'S INSURANCE\nTenant is encouraged to secure personal property insurance covering tenant belongings against casualty loss.", "insurance_liability", "fair"),
        ("ARTICLE 11: INDEMNIFICATION PROVISIONS\nUnder General Obligations Law 5-321, any lease clause exempting landlords from liability for their own negligence is void. Tenant indemnifies landlord only for tenant's own willful acts.", "indemnification", "fair"),
        ("ARTICLE 12: UTILITY ALLOCATION\nLandlord provides heat and hot water. Tenant pays electric and cooking gas through direct utility submetering.", "utilities", "fair"),
        ("ARTICLE 13: PET ADDENDUM\nPets are permitted in accordance with NYC Pet Law / NY state tenant guidelines. Service animals are permitted without restriction.", "pet_policy", "fair"),
        ("ARTICLE 14: DISPUTE RESOLUTION\nDisputes may be addressed through the New York State Attorney General Consumer Protection Bureau mediation program.", "dispute_resolution", "fair"),
        ("ARTICLE 15: GOVERNING LAW\nGoverned by the laws of the State of New York and the Housing Stability and Tenant Protection Act.", "governing_law_jurisdiction", "fair"),
    ],
    "fl_bar_approved_lease_14": [
        ("SECTION 9: LATE CHARGES\nRent received after the 4th day of the month shall incur a late charge of $50.00.", "late_fees_penalty", "fair"),
        ("SECTION 10: ALTERATIONS RESTRICTION\nTenant shall make no alterations, painting, or wallpapering without prior written consent of Landlord.", "alterations_improvements", "fair"),
        ("SECTION 11: TENANT INSURANCE\nTenant is required to maintain a renter's insurance policy with $100,000.00 liability limit throughout tenancy.", "insurance_liability", "fair"),
        ("SECTION 12: INDEMNIFICATION\nTenant agrees to indemnify Landlord from and against claims arising out of Tenant's negligent acts on the premises.", "indemnification", "fair"),
        ("SECTION 13: MEDIATION OF DISPUTES\nPrior to litigation, parties agree to attempt resolution through Florida Bar grievance mediation or local community mediation.", "dispute_resolution", "fair"),
        ("SECTION 14: RENEWAL NOTICE\nEither party may terminate or request renewal with at least thirty (30) days written notice prior to term expiration.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by Chapter 83 of the Florida Statutes (Florida Residential Landlord and Tenant Act).", "governing_law_jurisdiction", "fair"),
    ],
    "va_dhcd_model_lease_15": [
        ("SECTION 8: LATE CHARGES (VA CODE 55.1-1204)\nLate fee of $50.00 or 10% of monthly rent applies if rent is not received within five (5) days of due date.", "late_fees_penalty", "fair"),
        ("SECTION 9: ALTERATIONS AND FIXTURES\nTenant shall not make alterations, install satellite dishes, or paint walls without prior written consent.", "alterations_improvements", "fair"),
        ("SECTION 10: RENTER'S INSURANCE\nTenant shall maintain renter's liability insurance with minimum limits of $100,000.00 during tenancy.", "insurance_liability", "fair"),
        ("SECTION 11: INDEMNIFICATION\nTenant indemnifies Landlord against claims caused by Tenant's failure to comply with lease covenants.", "indemnification", "fair"),
        ("SECTION 12: UTILITY PAYMENT ALLOCATION\nTenant pays electric and gas. Landlord pays municipal water, sewer, and solid waste collection.", "utilities", "fair"),
        ("SECTION 13: DISPUTE MEDIATION\nParties may submit controversies to mediation under the Virginia Residential Landlord and Tenant Act.", "dispute_resolution", "fair"),
        ("SECTION 14: AUTOMATIC EXTENSION\nLease converts to month-to-month upon term expiration unless 30 days written notice of termination is served.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned strictly by the Virginia Residential Landlord and Tenant Act (Code of Virginia Title 55.1 Chapter 12).", "governing_law_jurisdiction", "fair"),
    ],
    "il_legalaid_model_lease_16": [
        ("SECTION 8: LATE FEES AND STATUTORY CEILING\nLate fee is $20.00, applicable only if rent remains unpaid after a 5-day grace period, pursuant to Illinois statutory guidelines.", "late_fees_penalty", "fair"),
        ("SECTION 9: ALTERATIONS AND IMPROVEMENTS\nTenant shall make no structural alterations, painting, or lock alterations without Landlord's written authorization.", "alterations_improvements", "fair"),
        ("SECTION 10: RENTER'S INSURANCE\nTenant is advised to maintain personal property and premises liability coverage of $100,000.00.", "insurance_liability", "fair"),
        ("SECTION 11: INDEMNIFICATION RESTRICTIONS\nTenant agrees to indemnify Landlord solely for losses resulting directly from Tenant's own negligent acts.", "indemnification", "fair"),
        ("SECTION 12: UTILITIES RESPONSIBILITY\nTenant pays separately metered electric and gas. Landlord pays city water and common refuse disposal.", "utilities", "fair"),
        ("SECTION 13: DISPUTE MEDIATION\nParties agree to participate in the Center for Conflict Resolution mediation program before court eviction filings.", "dispute_resolution", "fair"),
        ("SECTION 14: LEASE RENEWAL\nMonth-to-month extension requires thirty (30) days written notice of non-renewal by either party.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by the laws of the State of Illinois and Chicago Residential Landlord and Tenant Ordinance where applicable.", "governing_law_jurisdiction", "fair"),
    ],
    "austin_housing_lease_17": [
        ("8. LATE FEE REGULATIONS (TEXAS PROPERTY CODE 92.019)\nLate fee of $30.00 applies if rent is not received by the 5th day of the month, conforming to Texas statutory reasonableness requirements.", "late_fees_penalty", "fair"),
        ("9. PROPERTY ALTERATIONS\nTenant shall make no alterations, painting, or physical modifications without prior written consent.", "alterations_improvements", "fair"),
        ("10. TENANT INSURANCE\nTenant is strongly advised to maintain a renter's insurance policy throughout tenancy.", "insurance_liability", "fair"),
        ("11. INDEMNITY\nTenant agrees to defend and hold Landlord harmless against claims arising from Tenant's negligence or intentional acts.", "indemnification", "fair"),
        ("12. UTILITY BILLING\nTenant pays electric to Austin Energy. Landlord provides water, sewer, and curbside collection.", "utilities", "fair"),
        ("13. DISPUTE RESOLUTION\nParties may submit disputes to the Austin Dispute Resolution Center before seeking judicial remedies.", "dispute_resolution", "fair"),
        ("14. LEASE RENEWAL AND EXTENSION\nLease continues month-to-month after initial term with 30 days advance written notice required to terminate.", "renewal_auto_renewal", "fair"),
        ("15. GOVERNING LAW\nGoverned by Texas Property Code Chapter 92 and local municipal housing regulations.", "governing_law_jurisdiction", "fair"),
    ],
    "md_oag_sample_lease_18": [
        ("SECTION 8: LATE CHARGES (MD REAL PROPERTY 8-208)\nLate fee is capped at 5% of monthly rent and may only be charged after rent is 5 full days delinquent.", "late_fees_penalty", "fair"),
        ("SECTION 9: PROPERTY ALTERATIONS\nNo alterations, decorating, or wallpapering without Landlord's written permission.", "alterations_improvements", "fair"),
        ("SECTION 10: RENTER'S LIABILITY INSURANCE\nTenant is advised to maintain insurance covering personal effects and liability up to $100,000.00.", "insurance_liability", "fair"),
        ("SECTION 11: INDEMNIFICATION\nTenant indemnifies Landlord against claims caused solely by Tenant's own negligence on premises.", "indemnification", "fair"),
        ("SECTION 12: UTILITY SERVICES\nTenant pays electric and gas. Landlord provides water and regular trash removal.", "utilities", "fair"),
        ("SECTION 13: MEDIATION\nParties agree to seek mediation through the Maryland Community Mediation Center before litigation.", "dispute_resolution", "fair"),
        ("SECTION 14: LEASE RENEWAL\nSixty (60) days advance notice is required to terminate or non-renew at term expiration under Maryland law.", "renewal_auto_renewal", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by Maryland Real Property Code Title 8.", "governing_law_jurisdiction", "fair"),
    ],
    "ohio_legalaid_model_lease_19": [
        ("CLAUSE 7: LATE FEE CHARGES\nLate fee of $25.00 applies if rent is not received by the 5th day of the month.", "late_fees_penalty", "fair"),
        ("CLAUSE 8: ALTERATIONS AND FIXTURES\nTenant shall not make physical alterations or drive unauthorized anchors into walls without permission.", "alterations_improvements", "fair"),
        ("CLAUSE 9: INSURANCE COVERAGE\nTenant is encouraged to maintain renter's insurance for personal property and liability.", "insurance_liability", "fair"),
        ("CLAUSE 10: INDEMNITY\nTenant indemnifies Landlord against claims arising from Tenant's failure to maintain safe tenancy conditions.", "indemnification", "fair"),
        ("CLAUSE 11: UTILITIES\nTenant pays gas and electric. Landlord pays municipal water, sewer, and refuse services.", "utilities", "fair"),
        ("CLAUSE 12: DISPUTE RESOLUTION\nParties may engage in municipal court mediation prior to trial proceedings.", "dispute_resolution", "fair"),
        ("CLAUSE 13: AUTOMATIC RENEWAL\nTenancy converts to month-to-month with 30 days notice required to end occupancy.", "renewal_auto_renewal", "fair"),
        ("CLAUSE 14: PET POLICIES\nPets require written authorization and $200 deposit. Service animals are permitted without fee.", "pet_policy", "fair"),
        ("CLAUSE 15: GOVERNING LAW\nGoverned by Ohio Revised Code Chapter 5321 (Ohio Landlord-Tenant Act).", "governing_law_jurisdiction", "fair"),
    ],
    "co_dola_housing_lease_20": [
        ("7. LATE FEE RESTRICTIONS (HB 21-1121)\nLate fees cannot exceed $50.00 or 5% of past due rent and may only apply after a 7-day grace period.", "late_fees_penalty", "fair"),
        ("8. ALTERATIONS RESTRICTION\nTenant shall make no alterations or structural modifications without Landlord's written authorization.", "alterations_improvements", "fair"),
        ("9. RENTER'S INSURANCE\nTenant is advised to maintain insurance for personal property and $100,000.00 premises liability.", "insurance_liability", "fair"),
        ("10. INDEMNIFICATION\nTenant indemnifies Landlord for damages caused solely by Tenant's negligence or intentional wrongful acts.", "indemnification", "fair"),
        ("11. UTILITY RESPONSIBILITIES\nTenant pays electricity and heating gas. Landlord provides water, sewer, and regular trash collection.", "utilities", "fair"),
        ("12. DISPUTE MEDIATION\nParties may submit disputes to Colorado Community Mediation Services prior to filing in county court.", "dispute_resolution", "fair"),
        ("13. LEASE RENEWAL AND EXPIRATION\nConverts to month-to-month unless 30 days advance notice of non-renewal is delivered.", "renewal_auto_renewal", "fair"),
        ("14. PET POLICIES\nPets allowed with written addendum and refundable pet deposit. Service animals exempt.", "pet_policy", "fair"),
        ("15: GOVERNING LAW\nGoverned by Colorado Revised Statutes Title 38 Article 12.", "governing_law_jurisdiction", "fair"),
    ],
    "or_statebar_model_lease_21": [
        ("SECTION 7: LATE CHARGES (ORS 90.260)\nLate fee is $50.00, applicable only after the fourth (4th) day of the rental period.", "late_fees_penalty", "fair"),
        ("SECTION 8: PREMISES ALTERATIONS\nTenant shall make no structural changes, wall painting, or re-keying without prior written consent.", "alterations_improvements", "fair"),
        ("SECTION 9: RENTER'S INSURANCE\nTenant is advised to secure renter's personal property and liability insurance coverage.", "insurance_liability", "fair"),
        ("SECTION 10: INDEMNIFICATION\nTenant agrees to hold Landlord harmless against claims arising from Tenant's own negligence.", "indemnification", "fair"),
        ("SECTION 11: UTILITIES ALLOCATION\nTenant pays electric and gas. Landlord pays municipal water, sewer, and curbside recycling.", "utilities", "fair"),
        ("SECTION 12: DISPUTE MEDIATION\nParties may submit controversies to community dispute resolution programs under ORS 36.100.", "dispute_resolution", "fair"),
        ("SECTION 13: LEASE EXTENSION\nConverts to month-to-month tenancy upon term expiration under Oregon landlord-tenant laws.", "renewal_auto_renewal", "fair"),
        ("SECTION 14: PET POLICIES\nPets require written authorization and $250.00 pet deposit. Assistance animals exempt under fair housing laws.", "pet_policy", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by the Oregon Residential Landlord and Tenant Act (ORS Chapter 90).", "governing_law_jurisdiction", "fair"),
    ],
    "az_housing_model_lease_22": [
        ("7. LATE PAYMENT PENALTIES\nLate fee of $10.00 per day applies if rent is not received by the 5th day of the month.", "late_fees_penalty", "fair"),
        ("8. ALTERATIONS AND PAINTING\nTenant shall make no modifications, painting, or lock alterations without Landlord's written authorization.", "alterations_improvements", "fair"),
        ("9. TENANT INSURANCE\nTenant is strongly advised to maintain renter's insurance with at least $100,000.00 liability coverage.", "insurance_liability", "fair"),
        ("10. INDEMNITY\nTenant agrees to defend and indemnify Landlord against liabilities resulting from Tenant's negligence.", "indemnification", "fair"),
        ("11. UTILITY RESPONSIBILITY\nTenant pays electric and gas. Landlord provides water, sewer, and regular trash collection.", "utilities", "fair"),
        ("12. DISPUTE RESOLUTION\nParties agree to explore mediation prior to filing formal forcible detainer proceedings.", "dispute_resolution", "fair"),
        ("13. LEASE RENEWAL\nMonth-to-month extension requires thirty (30) days written notice of non-renewal.", "renewal_auto_renewal", "fair"),
        ("14. PET PROVISIONS\nPets permitted with written approval and $200 pet deposit. Service animals are exempt.", "pet_policy", "fair"),
        ("15. GOVERNING LAW\nGoverned by the Arizona Residential Landlord and Tenant Act (ARS Title 33 Chapter 10).", "governing_law_jurisdiction", "fair"),
    ],
    "ga_dca_model_lease_23": [
        ("SECTION 7: LATE CHARGE PROVISIONS\nLate fee of $50.00 applies if rent is not received by the 5th day of the month.", "late_fees_penalty", "fair"),
        ("SECTION 8: PROPERTY ALTERATIONS\nNo alterations, painting, or structural changes without Landlord's prior written permission.", "alterations_improvements", "fair"),
        ("SECTION 9: RENTER'S INSURANCE\nTenant is encouraged to maintain renter's insurance with $100,000.00 liability protection.", "insurance_liability", "fair"),
        ("SECTION 10: INDEMNIFICATION\nTenant indemnifies Landlord against claims caused solely by Tenant's own negligence on the premises.", "indemnification", "fair"),
        ("SECTION 11: UTILITIES PAYMENT\nTenant pays electric and gas. Landlord provides municipal water, sewer, and garbage collection.", "utilities", "fair"),
        ("SECTION 12: DISPUTE MEDIATION\nParties may submit tenancy disputes to Georgia Office of Dispute Resolution programs.", "dispute_resolution", "fair"),
        ("SECTION 13: AUTOMATIC RENEWAL\nLease converts to tenancy-at-will with sixty (60) days notice required by Landlord or thirty (30) days by Tenant.", "renewal_auto_renewal", "fair"),
        ("SECTION 14: PET RESTRICTIONS\nPets require written authorization and $250.00 deposit. Service animals accommodated without charge.", "pet_policy", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by the laws of the State of Georgia and OCGA Title 44 Chapter 7.", "governing_law_jurisdiction", "fair"),
    ],
    "pa_oag_model_lease_24": [
        ("CLAUSE 7: LATE FEE RESTRICTIONS\nLate fee of $40.00 applies after the 5th calendar day if rent remains unpaid.", "late_fees_penalty", "fair"),
        ("CLAUSE 8: ALTERATIONS AND FIXTURES\nTenant shall make no physical modifications, wall painting, or lock alterations without Landlord's written approval.", "alterations_improvements", "fair"),
        ("CLAUSE 9: RENTER'S LIABILITY INSURANCE\nTenant is advised to maintain personal property and premises liability insurance up to $100,000.00.", "insurance_liability", "fair"),
        ("CLAUSE 10: INDEMNITY\nTenant agrees to indemnify Landlord from damages caused by Tenant's negligence or violation of lease terms.", "indemnification", "fair"),
        ("CLAUSE 11: UTILITY RESPONSIBILITY\nTenant pays electric and gas. Landlord provides municipal water, sewer, and regular trash removal.", "utilities", "fair"),
        ("CLAUSE 12: DISPUTE MEDIATION\nParties may participate in community mediation services prior to commencing legal action in district court.", "dispute_resolution", "fair"),
        ("CLAUSE 13: AUTOMATIC RENEWAL\nConverts to month-to-month tenancy upon term expiration unless thirty (30) days written notice of termination is served.", "renewal_auto_renewal", "fair"),
        ("CLAUSE 14: PET RULES\nPets allowed with written consent and $250.00 pet deposit. Service animals are permitted in compliance with fair housing laws.", "pet_policy", "fair"),
        ("CLAUSE 15: GOVERNING LAW\nGoverned by the Pennsylvania Landlord and Tenant Act of 1951 (68 P.S. Section 250.101 et seq.).", "governing_law_jurisdiction", "fair"),
    ],
    "nj_dca_model_lease_25": [
        ("SECTION 6: LATE FEE AND GRACE PERIOD\nSenior citizens and disability pension recipients receive a mandatory 5-business-day grace period. Late fee is $35.00 after grace period.", "late_fees_penalty", "fair"),
        ("SECTION 7: PROPERTY ALTERATIONS\nTenant shall make no physical alterations, paint walls, or replace hardware without prior written authorization.", "alterations_improvements", "fair"),
        ("SECTION 8: RENTER'S INSURANCE\nTenant is advised to maintain insurance covering personal property and $100,000.00 liability.", "insurance_liability", "fair"),
        ("SECTION 9: INDEMNITY ALLOCATION\nTenant indemnifies Landlord against claims caused solely by Tenant's own negligence on premises.", "indemnification", "fair"),
        ("SECTION 10: UTILITIES\nTenant pays electricity and cooking gas. Landlord pays municipal water, sewer, and trash collection.", "utilities", "fair"),
        ("SECTION 11: DISPUTE RESOLUTION\nParties may submit disputes to New Jersey Superior Court Special Civil Part mediation services.", "dispute_resolution", "fair"),
        ("SECTION 12: AUTOMATIC RENEWAL (NJSA 2A:18-61.1)\nUnder the Anti-Eviction Act, lease automatically renews unless landlord has statutory good cause for non-renewal.", "renewal_auto_renewal", "fair"),
        ("SECTION 13: SUBLETTING TERMS\nSubletting requires Landlord's written authorization which shall not be unreasonably withheld.", "subletting", "fair"),
        ("SECTION 14: PET COVENANT\nPets permitted with written approval and $250 pet deposit. Service dogs exempt from deposits.", "pet_policy", "fair"),
        ("SECTION 15: GOVERNING LAW\nGoverned by the laws of the State of New Jersey and the Truth in Renting Act (NJSA 46:8-43 et seq.).", "governing_law_jurisdiction", "fair"),
    ],
}

# 2. OFFER LETTER ENRICHMENT
# For offer letter documents 4 to 22, add standard clauses
offer_enrichments = {
    "stanford_staff_offer_04": [
        ("8. WORKING HOURS AND HYBRID SCHEDULE\nStandard core working hours are 8:30 AM to 5:00 PM, Monday through Friday (40 hours/week) with eligibility for hybrid telecommuting pursuant to university policy.", "working_hours_location", "fair"),
        ("9. CONFIDENTIALITY AND FERPA/HIPAA\nYou agree to protect confidential student data, health information, and proprietary research findings in accordance with Stanford Administrative Guide Memo 1.5.1.", "confidentiality_nda", "fair"),
        ("10. NON-SOLICITATION AND CONFLICT OF COMMITMENT\nDuring your appointment, you agree to comply with Stanford's Conflict of Commitment policy and agree not to recruit university personnel for outside ventures.", "non_compete_non_solicit", "fair"),
        ("11. RESIGNATION AND SEPARATION TERMS\nStaff appointments are at-will. We request at least four (4) weeks written advance notice of resignation to facilitate transition of projects.", "termination_conditions", "fair"),
    ],
    "tamu_system_offer_05": [
        ("8. WORKING HOURS AND SCHEDULE\nNormal working hours are 8:00 AM to 5:00 PM, Monday through Friday, totaling 40 hours per week at the System headquarters in College Station.", "working_hours_location", "fair"),
        ("9. ANNUAL MERIT INCENTIVE ELIGIBILITY\nYou may be eligible for annual merit salary adjustments subject to legislative appropriations and satisfactory annual performance evaluation ratings.", "bonus_incentive", "fair"),
        ("10. ETHICS AND CONFIDENTIALITY\nYou are subject to Texas government ethics laws and agree to maintain the strict confidentiality of all official compliance investigations and proprietary data.", "confidentiality_nda", "fair"),
        ("11. CONFLICT OF INTEREST POLICY\nYou agree to adhere to TAMUS System Regulation 31.05.01 regarding outside employment and conflict of interest restrictions.", "non_compete_non_solicit", "fair"),
        ("12. DISPUTE RESOLUTION AND GRIEVANCE\nDisputes regarding employment conditions shall be resolved through the TAMUS Staff Grievance Procedure (Regulation 32.01.01).", "arbitration_dispute_resolution", "fair"),
        ("13. SEPARATION CONDITIONS\nEmployment is at-will. A minimum of two (2) weeks advance notice is requested upon voluntary separation.", "termination_conditions", "fair"),
    ],
    "uw_hr_offer_06": [
        ("7. WORKING HOURS AND HYBRID ARRANGEMENT\nThis position requires standard core working hours of 8:00 AM to 5:00 PM with approved telework pursuant to UW Telework Agreement guidelines.", "working_hours_location", "fair"),
        ("8. MERIT INCENTIVE AND SALARY REVIEW\nStaff salaries are reviewed annually for merit adjustments in accordance with university compensation policies and legislative funding.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY OF SENSITIVE RECORDS\nYou agree to maintain confidentiality of proprietary computing architectures, medical data, and student records pursuant to UW Administrative Policy Statements.", "confidentiality_nda", "fair"),
        ("10. CONFLICT OF INTEREST\nYou must disclose outside professional work and comply with Washington State Ethics in Public Service Act (RCW 42.52).", "non_compete_non_solicit", "fair"),
        ("11. GRIEVANCE AND DISPUTE RESOLUTION\nEmployment concerns may be addressed through the University of Washington Staff Complaint and Grievance Procedure.", "arbitration_dispute_resolution", "fair"),
        ("12. SEPARATION NOTICE\nStaff are requested to provide thirty (30) days written notice prior to voluntary separation.", "termination_conditions", "fair"),
    ],
    "penn_state_hr_offer_07": [
        ("7. HOURS OF WORK AND TELECOMMUTING\nStandard hours are 8:00 AM to 5:00 PM, Monday through Friday (40 hours/week) in the Corporate Controller's Office with hybrid flexibility.", "working_hours_location", "fair"),
        ("8. ANNUAL MERIT COMPENSATION\nYou will be eligible for annual merit salary review based on performance achievement against agreed objectives.", "bonus_incentive", "fair"),
        ("9. INTELLECTUAL PROPERTY POLICY IP01\nInventions and discoveries made using university funds or facilities are subject to Penn State Policy IP01.", "intellectual_property_assignment", "fair"),
        ("10. CONFLICT OF COMMITMENT\nYou agree to disclose outside consulting and refrain from activities that conflict with university business per Policy HR42.", "non_compete_non_solicit", "fair"),
        ("11. DISPUTE RESOLUTION\nEmployment disputes may be resolved through the Penn State Staff Grievance Policy HR76.", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE\nA minimum of two weeks written notice is requested for professional separations.", "termination_conditions", "fair"),
    ],
    "umich_staff_offer_08": [
        ("7. WORK HOURS AND SCHEDULE\nStandard 40-hour work week with core hours 8:30 AM to 5:00 PM. Remote work eligibility subject to departmental telecommuting agreement.", "working_hours_location", "fair"),
        ("8. MERIT SALARY ADJUSTMENT\nSalaries are reviewed annually for merit adjustments as part of the University annual compensation review cycle.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIAL DATA PROTECTION\nYou agree to safeguard proprietary ITS infrastructure data, health information, and student records under Michigan Standard Practice Guide 601.12.", "confidentiality_nda", "fair"),
        ("10. OUTSIDE ACTIVITIES AND CONFLICT OF INTEREST\nYou must disclose outside commercial consulting and comply with SPG 201.65-1 Regarding Conflicts of Interest.", "non_compete_non_solicit", "fair"),
        ("11. GRIEVANCE RESOLUTION PROCEDURE\nEmployment issues may be submitted to the University of Michigan Staff Grievance Procedure under SPG 201.08.", "arbitration_dispute_resolution", "fair"),
        ("12. SEPARATION AND RESIGNATION\nTwo (2) weeks written advance notice is requested upon voluntary resignation.", "termination_conditions", "fair"),
    ],
    "osu_hr_offer_09": [
        ("7. SCHEDULE AND WORKPLACE LOCATION\nFull-time 40-hour position at Wexner Medical Center with scheduled shifts from 8:00 AM to 4:30 PM.", "working_hours_location", "fair"),
        ("8. MERIT INCENTIVE ADJUSTMENTS\nEligible for annual university merit compensation increases based on fiscal year-end performance appraisals.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY AND HIPAA SECURITY\nYou agree to protect patient health records and confidential hospital data under Ohio State Wexner Medical Center compliance policies.", "confidentiality_nda", "fair"),
        ("10. ETHICS AND CONFLICT RESTRICTION\nSubject to the Ohio Ethics Law (RC Chapter 102) prohibiting private conflicts of interest in public university employment.", "non_compete_non_solicit", "fair"),
        ("11. DISPUTE RESOLUTION\nWorkplace grievances are handled pursuant to Ohio State Human Resources Policy 8.05.", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE\nA minimum of two weeks written notice of resignation is required.", "termination_conditions", "fair"),
    ],
    "calhr_state_offer_10": [
        ("7. WORK SCHEDULE AND CORE HOURS\nStandard 40-hour work schedule, Monday through Friday 8:00 AM to 5:00 PM at Department of Technology headquarters.", "working_hours_location", "fair"),
        ("8. MERIT SALARY ADJUSTMENT (MSA)\nEligible for annual Merit Salary Adjustments of 5% up to maximum of civil service salary range upon satisfactory service.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY OF STATE IT ASSETS\nYou agree to comply with State Administrative Manual (SAM) security guidelines and safeguard confidential government databases.", "confidentiality_nda", "fair"),
        ("10. INCOMPATIBLE ACTIVITIES STATEMENT\nYou must execute the Department's Statement of Incompatible Activities prohibiting outside employment that conflicts with state duties.", "non_compete_non_solicit", "fair"),
        ("11. MERIT SYSTEM GRIEVANCE AND APPEAL\nEmployment disputes are governed by California Government Code Title 2 and State Personnel Board appeals.", "arbitration_dispute_resolution", "fair"),
    ],
    "texas_dir_offer_11": [
        ("7. WORK HOURS AND LOCATION\nStandard working hours are 8:00 AM to 5:00 PM Monday through Friday in Austin, TX, with telework eligibility.", "working_hours_location", "fair"),
        ("8. MERIT PAY ELIGIBILITY\nEligible for state merit salary increases and one-time merit awards pursuant to Texas Government Code Section 659.255.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY AND CJIS SECURITY\nYou agree to maintain the strict confidentiality of all state cybersecurity intelligence and threat analyses.", "confidentiality_nda", "fair"),
        ("10. OUTSIDE EMPLOYMENT ETHICS\nMust obtain written approval prior to engaging in any outside employment per DIR Ethics Policy.", "non_compete_non_solicit", "fair"),
        ("11. INTERNAL GRIEVANCE PROCEDURE\nEmployment concerns may be addressed through the DIR Employee Dispute Resolution Procedure.", "arbitration_dispute_resolution", "fair"),
        ("12. VOLUNTARY RESIGNATION NOTICE\nA minimum of two (2) weeks advance written notice of resignation is requested.", "termination_conditions", "fair"),
    ],
    "opm_federal_offer_12": [
        ("7. TOUR OF DUTY AND WORK SCHEDULE\nStandard 80-hour bi-weekly tour of duty with flexible working hours between 7:00 AM and 6:00 PM pursuant to GSA alternative work schedules.", "working_hours_location", "fair"),
        ("8. PERFORMANCE AWARDS AND WITHIN-GRADE INCREASES\nEligible for annual performance-based cash awards and statutory Within-Grade Increases (WGI) under 5 CFR Part 531.", "bonus_incentive", "fair"),
        ("9. STANDARDS OF ETHICAL CONDUCT\nSubject to Title 5 CFR Part 2635 Standards of Ethical Conduct for Employees of the Executive Branch and conflict of interest restrictions.", "non_compete_non_solicit", "fair"),
        ("10. PRIVACY ACT AND NON-DISCLOSURE\nYou are bound by the Federal Privacy Act of 1974 (5 U.S.C. 552a) to protect sensitive procurement and agency records.", "confidentiality_nda", "fair"),
        ("11. ADMINISTRATIVE GRIEVANCE SYSTEM\nDisputes may be pursued through the agency Administrative Grievance Procedure or Merit Systems Protection Board (MSPB).", "arbitration_dispute_resolution", "fair"),
    ],
    "uf_hr_offer_13": [
        ("7. WORK HOURS AND CLINICAL SCHEDULE\nFull-time 40-hour work week, 8:00 AM to 5:00 PM, with clinical monitoring responsibilities in Gainesville, FL.", "working_hours_location", "fair"),
        ("8. ANNUAL MERIT INCREASES\nEligible for annual salary increases based on university merit guidelines and clinical grant milestones.", "bonus_incentive", "fair"),
        ("9. INTELLECTUAL PROPERTY AGREEMENT\nInventions and clinical study protocols developed within the scope of employment belong to the University of Florida Research Foundation.", "intellectual_property_assignment", "fair"),
        ("10. CONFLICT OF INTEREST DISCLOSURE\nMust disclose outside professional activities annually via the UF Regulations regarding Conflicts of Interest.", "non_compete_non_solicit", "fair"),
        ("11. STAFF GRIEVANCE PROCEDURE\nEmployment disputes may be resolved under University of Florida Regulation 3.031.", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE EXPECTATION\nA minimum of two (2) weeks notice is requested prior to voluntary separation.", "termination_conditions", "fair"),
    ],
    "uw_madison_offer_14": [
        ("7. SCHEDULE AND LOCATION\nStandard hours 8:00 AM to 4:30 PM Monday through Friday in Madison, WI, with hybrid options.", "working_hours_location", "fair"),
        ("8. MERIT ADJUSTMENTS\nEligible for annual discretionary merit adjustments based on performance reviews.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY AND FERPA\nYou agree to protect student records and proprietary IT systems in accordance with state and federal regulations.", "confidentiality_nda", "fair"),
        ("10. CONFLICT OF INTEREST REGULATIONS\nOutside activities must comply with UW-Madison Chapter UWS 8 Conflict of Interest rules.", "non_compete_non_solicit", "fair"),
        ("11. ACADEMIC STAFF GRIEVANCE\nDisputes may be addressed through the Academic Staff Appeals Committee.", "arbitration_dispute_resolution", "fair"),
        ("12. SEPARATION NOTICE\nThirty (30) days advance written notice of resignation is requested.", "termination_conditions", "fair"),
    ],
    "cu_boulder_offer_15": [
        ("7. WORKING HOURS AND ON-SITE REQUIREMENT\nStandard 40-hour week, 8:30 AM to 5:00 PM on-site in the Physics research facility.", "working_hours_location", "fair"),
        ("8. MERIT INCENTIVE POOL\nEligible for annual university merit compensation pools subject to Regents approval.", "bonus_incentive", "fair"),
        ("9. INTELLECTUAL PROPERTY POLICY\nDiscoveries and lab patents governed by CU Administrative Policy Statement 1013.", "intellectual_property_assignment", "fair"),
        ("10. CONFIDENTIAL RESEARCH DATA\nYou agree to safeguard proprietary lab data and export-controlled technical specifications.", "confidentiality_nda", "fair"),
        ("11. DISPUTE RESOLUTION\nDisputes handled through the CU Boulder Staff Grievance Process.", "arbitration_dispute_resolution", "fair"),
        ("12. NOTICE OF RESIGNATION\nTwo (2) weeks advance written notice requested for voluntary resignation.", "termination_conditions", "fair"),
    ],
    "uva_hr_offer_16": [
        ("7. WORK HOURS AND SCHEDULE\nStandard core working hours of 8:00 AM to 5:00 PM (40 hours/week) in Charlottesville, VA.", "working_hours_location", "fair"),
        ("8. MERIT COMPENSATION REVIEW\nAnnual base salary reviewed for merit adjustment during annual cycle.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY OF AUDIT RECORDS\nMust maintain confidentiality of financial audits and university records per Virginia FOIA exemptions.", "confidentiality_nda", "fair"),
        ("10. INTELLECTUAL PROPERTY POLICY\nInventions governed by University of Virginia Patent Policy.", "intellectual_property_assignment", "fair"),
        ("11. DISPUTE RESOLUTION\nDisputes handled under University Staff Grievance Policy HRM-028.", "arbitration_dispute_resolution", "fair"),
        ("12. SEPARATION NOTICE\nTwo (2) weeks written notice requested for professional separation.", "termination_conditions", "fair"),
    ],
    "asu_staff_offer_17": [
        ("7. WORK HOURS AND SCHEDULE\nStandard 40 hours per week, 8:00 AM to 5:00 PM at Tempe campus.", "working_hours_location", "fair"),
        ("8. MERIT INCREASES\nEligible for performance-based salary adjustments based on annual performance appraisals.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY AND FERPA\nMust safeguard student course evaluations and confidential records under FERPA.", "confidentiality_nda", "fair"),
        ("10. OUTSIDE ACTIVITIES RESTRICTION\nMust comply with Arizona Board of Regents Policy 6-705 regarding Outside Employment.", "non_compete_non_solicit", "fair"),
        ("11. GRIEVANCE RESOLUTION\nEmployment disputes handled through the Staff Dispute Resolution Procedure (SPP 201).", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE\nA minimum of two weeks written notice is requested.", "termination_conditions", "fair"),
    ],
    "ncsu_staff_offer_18": [
        ("7. WORK SCHEDULE AND REPORTING\nFull-time 40-hour schedule, 8:00 AM to 5:00 PM in Raleigh, NC.", "working_hours_location", "fair"),
        ("8. MERIT COMPENSATION REVIEW\nEligible for legislative salary increases and university merit awards.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY OF SAFETY RECORDS\nMust maintain confidentiality of regulatory inspections and hazardous incident data.", "confidentiality_nda", "fair"),
        ("10. CONFLICT OF INTEREST (NCSU REG 01.25.01)\nMust disclose outside commercial activities under the NCSU Conflict of Interest Regulation.", "non_compete_non_solicit", "fair"),
        ("11. DISPUTE MEDIATION\nEmployment grievances handled through the NC State University Grievance Policy.", "arbitration_dispute_resolution", "fair"),
        ("12. NOTICE TO VACATE POSITION\nTwo weeks written notice requested prior to resignation.", "termination_conditions", "fair"),
    ],
    "iu_hr_offer_19": [
        ("7. HOURS AND TELEWORK ARRANGEMENT\nStandard 40-hour week with approved hybrid telecommuting schedule.", "working_hours_location", "fair"),
        ("8. MERIT COMPENSATION ELIGIBILITY\nEligible for annual university salary merit adjustments based on performance reviews.", "bonus_incentive", "fair"),
        ("9. INTELLECTUAL PROPERTY POLICY\nInventions and software created subject to Indiana University Intellectual Property Policy.", "intellectual_property_assignment", "fair"),
        ("10. CONFLICT OF COMMITMENT RESTRICTION\nSubject to IU Policy UA-17 Regarding Conflicts of Commitment in outside employment.", "non_compete_non_solicit", "fair"),
        ("11. STAFF GRIEVANCE RESOLUTION\nDisputes handled through the Indiana University Staff Problem-Solving Procedure.", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE\nMinimum of two (2) weeks advance written notice requested.", "termination_conditions", "fair"),
    ],
    "umn_hr_offer_20": [
        ("7. WORK HOURS AND SCHEDULE\nStandard 40 hours per week, 8:00 AM to 4:30 PM in Minneapolis, MN.", "working_hours_location", "fair"),
        ("8. MERIT COMPENSATION PROGRAM\nEligible for annual salary adjustments based on collegiate merit pools.", "bonus_incentive", "fair"),
        ("9. CONFIDENTIALITY OF CONTRACTS\nMust maintain strict confidentiality of sponsored research agreements and proprietary trade data.", "confidentiality_nda", "fair"),
        ("10. OUTSIDE PROFESSIONAL COMMITMENTS\nMust report outside consulting under Board of Regents Outside Consulting Policy.", "non_compete_non_solicit", "fair"),
        ("11. CONFLICT RESOLUTION PROCESS\nDisputes handled through the University of Minnesota Office for Conflict Resolution (OCR).", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION TERMS\nTwo (2) weeks written notice requested for voluntary separation.", "termination_conditions", "fair"),
    ],
    "va_townhall_offer_21": [
        ("7. CORE OFFICE HOURS AND EXECUTIVE SCHEDULE\nStandard hours are 8:30 AM to 5:00 PM at agency headquarters with regular executive availability expected.", "working_hours_location", "fair"),
        ("8. CONFIDENTIALITY OF EXECUTIVE PROCEEDINGS\nYou agree to hold confidential all non-public regulatory proceedings and executive agency deliberations.", "confidentiality_nda", "fair"),
        ("9. INTELLECTUAL PROPERTY ASSIGNMENT\nAll official publications, white papers, and regulatory methodologies prepared belong to the Commonwealth.", "intellectual_property_assignment", "fair"),
        ("10. SEVERANCE AND RESIGNATION SCHEDULE\nIn the event of separation without cause, executive will receive 3 months severance pay subject to release.", "termination_conditions", "fair"),
    ],
    "austin_hr_offer_22": [
        ("7. WORK SCHEDULE AND CORE HOURS\nStandard 40-hour work week, 7:30 AM to 4:00 PM Monday through Friday at Austin Water facility.", "working_hours_location", "fair"),
        ("8. MERIT INCREASES AND STEP ADVANCEMENT\nEligible for annual City of Austin civil service step increases and merit adjustments.", "bonus_incentive", "fair"),
        ("9. INTELLECTUAL PROPERTY RIGHTS\nAll technical reports, water quality models, and designs belong to the City of Austin.", "intellectual_property_assignment", "fair"),
        ("10. CONFLICT OF INTEREST CHARTER\nSubject to Austin City Charter ethics provisions regarding outside contracting.", "non_compete_non_solicit", "fair"),
        ("11. DISPUTE RESOLUTION AND GRIEVANCE\nDisputes handled through the City of Austin Municipal Civil Service Grievance Procedure.", "arbitration_dispute_resolution", "fair"),
        ("12. RESIGNATION NOTICE\nA minimum of two (2) weeks advance written notice of resignation is required.", "termination_conditions", "fair"),
    ]
}

# 3. INSURANCE ENRICHMENT
# For insurance documents 3 to 20, add standard clauses
insurance_enrichments = {
    "oid_ho4_specimen_03": [
        ("SECTION 8: GRACE PERIOD FOR PREMIUM\nA grace period of thirty (30) days will be granted for the payment of each renewal premium, during which time the policy continues in force.", "grace_period", "fair"),
        ("SECTION 9: FRAUD AND CONCEALMENT\nThis entire policy is void if, whether before or after a loss, an insured has willfully concealed or misrepresented any material fact.", "misrepresentation_fraud_clause", "fair"),
        ("SECTION 10: POLICY PERIOD AND RENEWAL\nThis policy applies only to loss occurring during the policy period stated in the Declarations. We will offer renewal unless written notice is given.", "policy_period_renewal", "fair"),
        ("SECTION 11: SUBROGATION RIGHTS\nInsured must transfer all rights of recovery against liable third parties to company upon claim payment.", "subrogation", "fair"),
    ],
    "tdi_ho4_specimen_04": [
        ("SECTION I - DISPUTE RESOLUTION AND APPRAISAL\nIf you and we fail to agree on the amount of loss, either party may demand an appraisal in writing.", "dispute_resolution_appraisal", "fair"),
        ("SECTION I - GRACE PERIOD FOR PREMIUM PAYMENT\nA grace period of thirty (30) days is allowed for payment of renewal premiums before coverage lapses.", "grace_period", "fair"),
        ("SECTION I - FRAUD AND CONCEALMENT\nCoverage is void if an insured intentionally misrepresents material facts in connection with any claim.", "misrepresentation_fraud_clause", "fair"),
        ("SECTION I - POLICY PERIOD\nApplies only to losses occurring during the policy period stated in the declarations.", "policy_period_renewal", "fair"),
        ("SECTION I - SUBROGATION ASSIGNMENT\nWe acquire all legal rights of recovery against third parties upon payment of loss.", "subrogation", "fair"),
    ],
    "cdi_ho4_specimen_05": [
        ("9. GRACE PERIOD FOR RENEWAL PREMIUM\nA grace period of 30 days is provided for renewal premium payments to maintain continuous coverage.", "grace_period", "fair"),
        ("10. FRAUD AND MISREPRESENTATION (CIC 331)\nConcealment or misrepresentation of a material fact entitles the injured party to rescind insurance.", "misrepresentation_fraud_clause", "fair"),
        ("11. SUBROGATION AND RECOVERY\nCompany is subrogated to the insured's right of recovery against third parties to the extent of claim payment.", "subrogation", "fair"),
        ("12. APPRAISAL PROCEDURE\nValuation disputes may be submitted to independent appraisal upon written demand.", "dispute_resolution_appraisal", "fair"),
        ("13. POLICY TERM AND RENEWAL\nPolicy runs for a term of one year from inception date and may be renewed upon timely payment.", "policy_period_renewal", "fair"),
    ],
    "nydfs_ho4_specimen_06": [
        ("SECTION I AND II: GRACE PERIOD\nThirty (30) days grace period granted for renewal premium before coverage termination.", "grace_period", "fair"),
        ("SECTION I AND II: FRAUD AND CONCEALMENT\nAny intentional material misrepresentation voids coverage under New York Insurance Law.", "misrepresentation_fraud_clause", "fair"),
        ("SECTION I AND II: APPRAISAL OF LOSS\nIf parties fail to agree on loss amount, appraisal may be demanded pursuant to NYIL Section 3408.", "dispute_resolution_appraisal", "fair"),
        ("SECTION I AND II: POLICY PERIOD\nCovers losses occurring during the policy period stated on Declarations.", "policy_period_renewal", "fair"),
    ],
    "wa_oic_specimen_07": [
        ("8. GRACE PERIOD\nA grace period of 30 days is granted for payment of renewal premium.", "grace_period", "fair"),
        ("9. CONCEALMENT OR FRAUD\nWillful concealment or misrepresentation of material fact voids policy coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL CLAUSE\nDisputes on valuation of loss may be submitted to appraisal by neutral appraisers and umpire.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nCompany acquires right of recovery against third parties upon payment.", "subrogation", "fair"),
        ("12. POLICY TERM\nPolicy applies to losses occurring during the 12-month period specified.", "policy_period_renewal", "fair"),
    ],
    "ma_doi_specimen_08": [
        ("SECTION 8: GRACE PERIOD\nA 30-day grace period is provided for payment of each renewal premium.", "grace_period", "fair"),
        ("SECTION 9: FRAUD AND CONCEALMENT\nPolicy is void if insured intentionally conceals material facts or commits fraud.", "misrepresentation_fraud_clause", "fair"),
        ("SECTION 10: DISPUTE RESOLUTION AND APPRAISAL\nIf parties fail to agree on amount of loss, appraisal may be demanded under Massachusetts law.", "dispute_resolution_appraisal", "fair"),
        ("SECTION 11: SUBROGATION\nInsured transfers recovery rights against responsible third parties upon payment.", "subrogation", "fair"),
        ("SECTION 12: POLICY PERIOD\nCovers direct loss occurring during the policy period.", "policy_period_renewal", "fair"),
    ],
    "odi_ho4_specimen_09": [
        ("8. GRACE PERIOD\nA grace period of 30 days is granted for payment of each renewal premium.", "grace_period", "fair"),
        ("9. FRAUD AND MISREPRESENTATION\nIntentional concealment or fraud in connection with a claim voids coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL CLAUSE\nValuation disputes handled by independent appraisers and an umpire.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION RIGHTS\nSubrogation transfer of recovery rights upon payment of loss.", "subrogation", "fair"),
        ("12. POLICY DURATION\nPolicy runs for one annual term from effective date.", "policy_period_renewal", "fair"),
    ],
    "idoi_ho4_specimen_10": [
        ("SECTION I: GRACE PERIOD\nThirty (30) days grace period allowed for renewal premium before coverage lapse.", "grace_period", "fair"),
        ("SECTION I: FRAUD AND CONCEALMENT\nMaterial misrepresentation or fraud voids all coverage under policy.", "misrepresentation_fraud_clause", "fair"),
        ("SECTION I: APPRAISAL OF LOSS\nAppraisal procedure available for loss valuation disputes.", "dispute_resolution_appraisal", "fair"),
        ("SECTION I: SUBROGATION\nCompany acquires subrogation rights upon claim payment.", "subrogation", "fair"),
        ("SECTION I: POLICY TERM\nApplies to loss occurring during policy period.", "policy_period_renewal", "fair"),
    ],
    "pa_pid_specimen_11": [
        ("8. GRACE PERIOD FOR PREMIUM\nGrace period of 30 days granted for renewal premium remittance.", "grace_period", "fair"),
        ("9. FRAUD AND CONCEALMENT\nWillful misrepresentation of material facts voids coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. SUBROGATION PROVISION\nSubrogation rights assigned to company upon payment.", "subrogation", "fair"),
        ("11. POLICY PERIOD\nPolicy applies to loss occurring during effective policy period.", "policy_period_renewal", "fair"),
    ],
    "ga_oci_specimen_12": [
        ("7. GRACE PERIOD\n30 days grace period for payment of renewal premium.", "grace_period", "fair"),
        ("8. FRAUD AND CONCEALMENT\nFraudulent misrepresentation voids the policy.", "misrepresentation_fraud_clause", "fair"),
        ("9. APPRAISAL\nAppraisal process applies if parties disagree on value.", "dispute_resolution_appraisal", "fair"),
        ("10. SUBROGATION\nCompany subrogated to rights of recovery upon payment.", "subrogation", "fair"),
        ("11. POLICY PERIOD\nCovers direct physical loss during policy period.", "policy_period_renewal", "fair"),
    ],
    "va_bureau_ins_specimen_13": [
        ("8. GRACE PERIOD\nGrace period of 30 days granted for renewal premiums.", "grace_period", "fair"),
        ("9. FRAUD AND CONCEALMENT\nConcealment or fraud voids coverage for all insureds.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL OF LOSS\nDisputes on loss value resolved by appraisal.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nAssignment of recovery rights against third parties upon payment.", "subrogation", "fair"),
        ("12. POLICY PERIOD\nCovers loss during policy period stated in declarations.", "policy_period_renewal", "fair"),
    ],
    "wi_oci_specimen_14": [
        ("7. GRACE PERIOD\n30-day grace period for renewal premium.", "grace_period", "fair"),
        ("8. FRAUD AND MISREPRESENTATION\nMaterial misrepresentation voids coverage.", "misrepresentation_fraud_clause", "fair"),
        ("9. APPRAISAL\nIndependent appraisal for valuation disputes.", "dispute_resolution_appraisal", "fair"),
        ("10. SUBROGATION\nInsured transfers recovery rights to insurer upon payment.", "subrogation", "fair"),
        ("11. POLICY PERIOD\nApplies only to loss during policy period.", "policy_period_renewal", "fair"),
    ],
    "co_doi_specimen_15": [
        ("8. GRACE PERIOD\nThirty days grace period for renewal premium payment.", "grace_period", "fair"),
        ("9. FRAUD AND CONCEALMENT\nIntentional fraud voids policy coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL PROCEDURE\nAppraisal procedure for disputed claim amounts.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nSubrogation transfer upon claim payment.", "subrogation", "fair"),
        ("12. POLICY PERIOD\nAnnual policy period for covered losses.", "policy_period_renewal", "fair"),
    ],
    "mi_difs_specimen_16": [
        ("7. GRACE PERIOD\n30 days grace period for renewal premium payment.", "grace_period", "fair"),
        ("8. FRAUD AND CONCEALMENT\nFraudulent statements void coverage under Michigan law.", "misrepresentation_fraud_clause", "fair"),
        ("9. APPRAISAL\nAppraisal process for loss valuation disagreement.", "dispute_resolution_appraisal", "fair"),
        ("10. SUBROGATION\nCompany acquires recovery rights upon payment.", "subrogation", "fair"),
        ("11. POLICY TERM\nApplies to loss occurring during effective policy period.", "policy_period_renewal", "fair"),
    ],
    "mn_doc_specimen_17": [
        ("8. GRACE PERIOD\nGrace period of 30 days allowed for renewal premium.", "grace_period", "fair"),
        ("9. FRAUD AND MISREPRESENTATION\nIntentional fraud voids policy.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL\nAppraisal procedure for property valuation disputes.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nSubrogation assignment upon payment.", "subrogation", "fair"),
        ("12. POLICY PERIOD\nCovers direct physical loss during policy period.", "policy_period_renewal", "fair"),
    ],
    "md_mia_specimen_18": [
        ("8. GRACE PERIOD\n30 days grace period for renewal premium payment.", "grace_period", "fair"),
        ("9. CONCEALMENT OR FRAUD\nMaterial misrepresentation voids coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL\nAppraisal clause for disputed loss amount.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nSubrogation rights transfer upon payment of loss.", "subrogation", "fair"),
        ("12. POLICY PERIOD\nPolicy covers loss during declared period.", "policy_period_renewal", "fair"),
    ],
    "sc_doi_specimen_19": [
        ("8. GRACE PERIOD\nThirty days grace period for renewal premium.", "grace_period", "fair"),
        ("9. FRAUD AND CONCEALMENT\nFraudulent misrepresentation voids coverage.", "misrepresentation_fraud_clause", "fair"),
        ("10. APPRAISAL OF LOSS\nAppraisal mechanism for valuation disputes.", "dispute_resolution_appraisal", "fair"),
        ("11. SUBROGATION\nAssignment of recovery rights upon payment.", "subrogation", "fair"),
        ("12. POLICY PERIOD\nPolicy applies to loss during declared term.", "policy_period_renewal", "fair"),
    ],
    "in_doi_specimen_20": [
        ("7. GRACE PERIOD\n30 days grace period for renewal premium.", "grace_period", "fair"),
        ("8. FRAUD AND CONCEALMENT\nIntentional concealment voids insurance.", "misrepresentation_fraud_clause", "fair"),
        ("9. APPRAISAL\nDisputes on amount of loss resolved by appraisal.", "dispute_resolution_appraisal", "fair"),
        ("10. SUBROGATION\nSubrogation rights assigned upon claim payment.", "subrogation", "fair"),
        ("11. POLICY PERIOD\nCovers loss during declared policy period.", "policy_period_renewal", "fair"),
    ]
}

# Apply enrichments
for d in RENTAL_SOURCES:
    doc_id = d["doc_id"]
    if doc_id in rental_enrichments:
        d["clauses"].extend(rental_enrichments[doc_id])

for d in OFFER_SOURCES:
    doc_id = d["doc_id"]
    if doc_id in offer_enrichments:
        d["clauses"].extend(offer_enrichments[doc_id])

for d in INSURANCE_SOURCES:
    doc_id = d["doc_id"]
    if doc_id in insurance_enrichments:
        d["clauses"].extend(insurance_enrichments[doc_id])

print(f"ENRICHED RENTAL: {len(RENTAL_SOURCES)} docs, {sum(len(d['clauses']) for d in RENTAL_SOURCES)} clauses")
print(f"ENRICHED OFFER: {len(OFFER_SOURCES)} docs, {sum(len(d['clauses']) for d in OFFER_SOURCES)} clauses")
print(f"ENRICHED INSURANCE: {len(INSURANCE_SOURCES)} docs, {sum(len(d['clauses']) for d in INSURANCE_SOURCES)} clauses")
total = sum(len(d['clauses']) for d in RENTAL_SOURCES + OFFER_SOURCES + INSURANCE_SOURCES)
print(f"ENRICHED TOTAL: {len(RENTAL_SOURCES) + len(OFFER_SOURCES) + len(INSURANCE_SOURCES)} docs, {total} clauses")
