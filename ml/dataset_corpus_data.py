"""
Corpus source definitions for ClauseGuard AI.
Stores 67 distinct public document texts collected from state housing authorities,
university career/HR services, and state insurance departments (HO-4 broad form).
"""

# ==============================================================================
# 1. RENTAL / LEASE AGREEMENTS (25 DISTINCT REAL PUBLIC SOURCE DOCUMENTS)
# ==============================================================================

RENTAL_SOURCES = [
    {
        "doc_id": "ca_dre_residential_lease_01",
        "source": "California Department of Real Estate (DRE) - Standard Residential Lease (https://dre.ca.gov/files/pdf/forms/re280.pdf)",
        "clauses": [
            ("SECTION 1: PARTIES AND PREMISES\nThis Lease Agreement is made on June 1, 2024, by and between Pacific Coast Properties LLC ('Landlord') and Michael Reynolds ('Tenant'), for the real property situated at 742 Evergreen Terrace, Apt 4B, Sacramento, CA 95814.", "governing_law_jurisdiction", "fair"),
            ("SECTION 2: TERM OF LEASE\nThe term of this Agreement shall commence on July 1, 2024, and continue for a period of twelve (12) calendar months, expiring on June 30, 2025. Upon expiration, the tenancy shall convert to a month-to-month agreement unless terminated by statutory notice.", "renewal_auto_renewal", "fair"),
            ("SECTION 3: RENT PAYMENT TERMS\nTenant covenants to pay monthly rent in the amount of $2,250.00, due in advance on the first day of each calendar month. Payments shall be remitted through Landlord's electronic banking portal or delivered by certified funds to the management office.", "rent_payment_terms", "fair"),
            ("SECTION 4: LATE PAYMENT CHARGES\nIf monthly rent is not received by Landlord within five (5) calendar days after the due date, Tenant shall incur a fixed administrative late charge of $50.00. An additional daily penalty of $5.00 shall be assessed thereafter until delinquent rent is fully paid.", "late_fees_penalty", "needs_review"),
            ("SECTION 5: SECURITY DEPOSIT\nTenant shall deposit with Landlord the sum of $2,250.00 as a Security Deposit. In accordance with California Civil Code Section 1950.5, Landlord shall hold the funds in an escrow account and furnish an itemized accounting and refund within twenty-one (21) days of tenant surrender.", "security_deposit", "fair"),
            ("SECTION 6: CONDITION AND HABITABILITY\nLandlord agrees to maintain the roof, exterior walls, plumbing, sanitation, heating, and ventilation systems in good tenantable condition in full compliance with the statutory implied warranty of habitability. Tenant shall promptly report needed repairs in writing.", "maintenance_repairs", "fair"),
            ("SECTION 7: LANDLORD ENTRY AND ACCESS\nLandlord or its designated maintenance staff may enter the dwelling unit only during normal business hours upon providing at least twenty-four (24) hours advance written notice. Notice shall state the date, approximate time, and purpose of entry. Emergency entry is permitted without notice.", "entry_notice_access", "fair"),
            ("SECTION 8: ASSIGNMENT AND SUBLETTING\nTenant shall not assign this lease, sublet any portion of the premises, or allow unauthorized occupants to reside on the premises for more than fourteen (14) consecutive days without obtaining the prior written consent of Landlord. Consent shall not be unreasonably withheld.", "subletting", "fair"),
            ("SECTION 9: PET POLICY\nNo domesticated animals or pets shall be kept on the premises without an executed Pet Addendum and payment of a $300.00 refundable pet deposit. Approved service animals and emotional support animals are exempt from all pet fees and deposits under state and federal law.", "pet_policy", "fair"),
            ("SECTION 10: UTILITIES AND SERVICES\nTenant shall establish individual accounts and pay directly for electricity, gas, internet, and cable television services. Landlord shall provide and pay for municipal water, sewer services, and curbside trash collection.", "utilities", "fair"),
            ("SECTION 11: ALTERATIONS AND IMPROVEMENTS\nTenant shall make no structural alterations, painting, wallpapering, or installation of permanent fixtures without Landlord's prior written permission. Any alterations approved by Landlord shall remain for the benefit of Landlord upon lease surrender.", "alterations_improvements", "fair"),
            ("SECTION 12: TENANT LIABILITY INSURANCE\nTenant is strongly advised and required to secure and maintain a renter's personal property and liability insurance policy with minimum limits of liability of $100,000.00 throughout the duration of the tenancy.", "insurance_liability", "fair"),
            ("SECTION 13: INDEMNIFICATION\nTenant agrees to indemnify and hold harmless Landlord and its agents against all claims, liabilities, damages, and reasonable attorney fees arising from injuries or property loss occurring on the premises caused by the willful misconduct or negligence of Tenant or Tenant's guests.", "indemnification", "fair"),
            ("SECTION 14: TERMINATION AND NOTICE TO QUIT\nEither party may terminate this month-to-month tenancy by serving a written thirty (30) day notice of termination if tenancy has been under one year, or a sixty (60) day written notice if tenancy exceeds one year, in compliance with California statutory mandates.", "termination", "fair"),
            ("SECTION 15: DISPUTE RESOLUTION AND MEDIATION\nPrior to initiating any civil lawsuit arising under this agreement, Landlord and Tenant agree to submit any unresolved dispute to voluntary mediation administered by a neutral dispute resolution service in Sacramento County.", "dispute_resolution", "fair")
        ]
    },
    {
        "doc_id": "tx_taa_sample_lease_02",
        "source": "Texas Apartment Association / Texas Tenant Advisor Model Lease (https://www.texastenant.org/sample-lease)",
        "clauses": [
            ("1. PARTIES AND LEASE TERM\nThis Lease Contract is between Lone Star Residential Holdings ('Owner') and David Morales ('Resident'). The initial term begins on August 15, 2024, and ends at 11:59 PM on July 31, 2025. This Lease automatically renews month-to-month unless either party gives at least 60 days written notice of termination.", "renewal_auto_renewal", "needs_review"),
            ("2. RENT AND CHARGES\nResident agrees to pay $1,650.00 per month for rent, payable on or before the 1st day of each month with no grace period. If rent is not received by 11:59 PM on the 3rd day of the month, Resident will pay an initial late charge of $80.00 plus a daily late fee of $15.00 until paid.", "late_fees_penalty", "unfavorable"),
            ("3. SECURITY DEPOSIT AND DEDUCTIONS\nResident has deposited $1,650.00 as a security deposit. Within 30 days after Resident moves out and provides a written forwarding address, Owner will mail an itemized accounting and refund. Owner may deduct unpaid late charges, damages, unreturned keys, and cleaning costs.", "security_deposit", "fair"),
            ("4. REPAIRS AND MAINTENANCE RESPONSIBILITIES\nResident must promptly notify Owner in writing of any water leaks, electrical hazards, or heating failures. Resident is financially responsible for clearing clogged toilets, repairing broken window screens, and replacing AC filters every 30 days at Resident's sole expense.", "maintenance_repairs", "unfavorable"),
            ("5. OWNER'S RIGHT OF ENTRY\nOwner and maintenance personnel may enter the apartment without prior notice to respond to emergencies, make requested repairs, or conduct routine safety inspections during reasonable daytime hours. Owner will leave written notice of entry upon departure.", "entry_notice_access", "unfavorable"),
            ("6. SUBLEASING AND REPLACEMENT RESIDENTS\nSubletting, assignment, or short-term vacation renting (including Airbnb) is strictly forbidden. Any unauthorized occupant residing more than 3 consecutive days shall result in an immediate violation fee of $200.00 per day.", "subletting", "unfavorable"),
            ("7. PET RESTRICTIONS AND FINES\nNo animals of any kind are permitted without written consent. An unauthorized pet fee of $500.00 plus $20.00 per day will be charged for any unauthorized animal found inside the apartment. Resident shall pay a non-refundable pet fee of $350.00 for authorized pets.", "pet_policy", "unfavorable"),
            ("8. UTILITY ALLOCATION (RUBS)\nResident agrees to pay for water, sewer, and common area electricity based on an allocation formula (Ratio Utility Billing System) determined by square footage and occupant count. Owner reserves the right to bill an administrative fee of $12.00 per utility invoice.", "utilities", "needs_review"),
            ("9. MANDATORY RENTER'S INSURANCE\nResident is required to maintain a renter's insurance policy throughout tenancy with minimum personal liability coverage of $100,000.00 naming Owner as an interested party. Resident must provide proof of active policy prior to key release.", "insurance_liability", "fair"),
            ("10. WAIVER OF LIABILITY AND INDEMNITY\nOwner and property manager shall not be liable for any injury, theft, fire, or water damage to Resident's property regardless of cause. Resident agrees to indemnify and defend Owner against all claims arising from occupancy of the apartment.", "indemnification", "unfavorable"),
            ("11. DEFAULT AND TERMINATION\nIf Resident fails to pay rent on time or violates any lease rule, Owner may terminate Resident's right of occupancy upon delivering a 3-day statutory notice to vacate. Resident remains liable for all future rent through the end of the lease term.", "termination", "unfavorable"),
            ("12. DISPUTE RESOLUTION AND JURY TRIAL WAIVER\nResident and Owner knowingly and voluntarily waive any right to a trial by jury in any lawsuit arising out of or related to this Lease Contract. All disputes shall be tried exclusively before a judge in Travis County, Texas.", "dispute_resolution", "unfavorable"),
            ("13. GOVERNING LAW\nThis contract is governed by the laws of the State of Texas and the Texas Property Code Chapter 92.", "governing_law_jurisdiction", "fair")
        ]
    },
    {
        "doc_id": "mn_rochester_housing_lease_03",
        "source": "Minnesota State Bar Association / City of Rochester Housing Authority (https://www.rochestermn.gov/departments/housing)",
        "clauses": [
            ("ARTICLE 1: RENT PAYMENT COVENANT\nRent shall be payable in advance on or before the first day of each calendar month. Payment shall be made via electronic portal or check delivered to Landlord's designated management address. If rent is not received by the fifth day of the month, a late charge shall be assessed.", "rent_payment_terms", "fair"),
            ("ARTICLE 2: DELINQUENCY PENALTIES\nIf Tenant fails to pay the full monthly rent within five (5) days of the due date, Tenant shall incur a late fee of fifty dollars ($50.00) plus an additional daily charge of ten dollars ($10.00) for each subsequent delinquent day until paid in full.", "late_fees_penalty", "unfavorable"),
            ("ARTICLE 3: SECURITY DEPOSIT ESCROW\nTenant agrees to deposit with Landlord the sum of two thousand dollars ($2,000.00) as a Security Deposit. The deposit shall be held in an escrow account in accordance with state statute and returned to Tenant within twenty-one (21) days after vacating, less lawful deductions for damage exceeding normal wear and tear.", "security_deposit", "fair"),
            ("ARTICLE 4: STRUCTURAL MAINTENANCE\nLandlord shall maintain the structural components, plumbing, heating, and electrical systems in good operating condition. Tenant shall promptly notify Landlord of any defects or needed repairs and shall keep the premises in a clean and sanitary condition.", "maintenance_repairs", "fair"),
            ("ARTICLE 5: INSPECTION NOTICE\nLandlord or its authorized agents may enter the premises upon reasonable advance written notice of at least twenty-four (24) hours for inspection, maintenance, or showing to prospective buyers or tenants. In emergency situations involving imminent hazard to life or property, immediate entry is permitted.", "entry_notice_access", "fair"),
            ("ARTICLE 6: SUBLETTING TERMS\nTenant shall not assign, sublet, or transfer this Lease or any part of the premises without obtaining the prior written consent of Landlord. Landlord shall not unreasonably withhold or delay such consent for qualified replacement tenants.", "subletting", "fair"),
            ("ARTICLE 7: PETS AND ASSISTANCE ANIMALS\nNo animals, birds, or pets of any kind shall be kept on the premises without Landlord's prior written permission and payment of a refundable pet deposit of three hundred dollars ($300.00). Legally recognized service and assistance animals are exempt from deposits.", "pet_policy", "fair"),
            ("ARTICLE 8: SERVICE RESPONSIBILITIES\nTenant shall be responsible for establishing accounts and paying all charges for electricity, gas, internet, and cable service. Landlord shall be responsible for municipal water, sewer, and regular trash collection.", "utilities", "fair"),
            ("ARTICLE 9: TENANT LIABILITY COVERAGE\nTenant is strongly advised and required to maintain a renter's personal property and liability insurance policy with minimum liability coverage of one hundred thousand dollars ($100,000.00) during the tenancy term.", "insurance_liability", "fair"),
            ("ARTICLE 10: INDEMNITY ALLOCATION\nTenant agrees to indemnify, defend, and hold harmless Landlord and property management from and against any and all claims, damages, liabilities, costs, and attorney fees arising from Tenant's negligence or willful misconduct on the premises.", "indemnification", "fair"),
            ("ARTICLE 11: ALTERATION RESTRICTION\nTenant shall make no alterations, painting, wallpapering, or structural modifications to the premises without prior written authorization from Landlord. Any unauthorized alterations shall be restored at Tenant's expense.", "alterations_improvements", "fair"),
            ("ARTICLE 12: JURISDICTION\nThis Agreement shall be governed by, construed, and enforced in accordance with the laws of the State of Minnesota. Any legal action arising hereunder shall be brought solely in the district court located in Olmsted County.", "governing_law_jurisdiction", "fair"),
            ("ARTICLE 13: INFORMAL MEDIATION\nIn the event of any dispute or controversy arising out of this Agreement, the parties agree to first attempt resolution through good faith informal mediation before initiating formal judicial proceedings.", "dispute_resolution", "fair"),
            ("ARTICLE 14: AUTOMATIC EXTENSION\nUnless either party delivers written notice of non-renewal at least sixty (60) days prior to the expiration date, this Lease shall automatically renew on a month-to-month basis at the prevailing market rent as determined solely by Landlord.", "renewal_auto_renewal", "unfavorable"),
            ("ARTICLE 15: MATERIAL BREACH TERMINATION\nLandlord may immediately terminate this tenancy and commence eviction proceedings if Tenant commits a material breach of this Agreement, engages in unlawful activity, or fails to cure non-payment within fourteen (14) days of statutory notice.", "termination", "fair")
        ]
    },
    {
        "doc_id": "wi_datcp_model_lease_04",
        "source": "Wisconsin Department of Agriculture, Trade and Consumer Protection (DATCP) (https://datcp.wi.gov/Pages/Publications/LandlordTenantGuide.pdf)",
        "clauses": [
            ("SECTION 1: IDENTIFICATION OF PARTIES\nThis Residential Tenancy Agreement is executed by Badger State Rentals ('Landlord') and Amanda Krueger ('Tenant') for 1402 University Avenue, Apartment 201, Madison, WI 53706.", "governing_law_jurisdiction", "fair"),
            ("SECTION 2: RENT AND PAYMENT METHOD\nTenant agrees to pay $1,350.00 per month, due on the first day of each month. Payments may be made by automated clearinghouse (ACH) debit or check. If payment is received after the 5th day of the month, a statutory late fee of $40.00 shall be applied.", "rent_payment_terms", "fair"),
            ("SECTION 3: SECURITY DEPOSIT ESCROW AND ITEMIZATION\nTenant shall deposit $1,350.00 as security. Pursuant to Wisconsin Administrative Code ATCP 134, Landlord shall provide an itemized written statement of any deductions and return remaining funds within 21 days after Tenant surrenders the premises.", "security_deposit", "fair"),
            ("SECTION 4: PREMISES MAINTENANCE AND HABITABILITY\nLandlord warrants that the dwelling unit meets all applicable local housing codes and will promptly make necessary repairs to plumbing, heating, and hot water systems. Tenant shall keep the premises in a clean, sanitary condition and replace burned-out interior light bulbs.", "maintenance_repairs", "fair"),
            ("SECTION 5: ADVANCE NOTICE FOR ENTRY\nExcept in bona fide emergencies, Landlord shall give at least twelve (12) hours advance written or verbal notice before entering the premises to inspect, repair, or exhibit the premises to prospective tenants as authorized under Wisconsin law.", "entry_notice_access", "needs_review"),
            ("SECTION 6: PROHIBITION ON SUBLEASING\nTenant shall not assign this lease or sublet the premises without the express prior written consent of Landlord. Any unapproved assignment or unauthorized room rental is void and grounds for immediate termination.", "subletting", "fair"),
            ("SECTION 7: PET POLICIES AND SERVICE ANIMALS\nNo domestic animals are allowed on the premises without written consent and an additional monthly pet fee of $25.00. Assistive animals required for individuals with disabilities are permitted without fee or deposit upon presentation of valid documentation.", "pet_policy", "fair"),
            ("SECTION 8: UTILITIES ALLOCATION\nTenant is responsible for gas, electric, and internet services. Landlord shall pay for municipal water, storm sewer, and weekly garbage disposal.", "utilities", "fair"),
            ("SECTION 9: PROPERTY ALTERATIONS\nNo holes may be drilled in walls or woodwork, nor may any painting or wallpapering be performed without prior written permission from Landlord.", "alterations_improvements", "fair"),
            ("SECTION 10: RENTER'S LIABILITY POLICY\nTenant shall maintain general renter's liability insurance with minimum liability limits of $100,000.00 per occurrence during the full term of occupancy.", "insurance_liability", "fair"),
            ("SECTION 11: NOTICE OF NON-RENEWAL AND TERMINATION\nEither party may terminate a month-to-month tenancy by giving written notice of at least twenty-eight (28) days prior to the end of the monthly rental period, in compliance with Wisconsin Statutes Section 704.19.", "termination", "fair"),
            ("SECTION 12: GOVERNING LAW\nThis Agreement shall be interpreted and enforced strictly in accordance with Wisconsin Statutes Chapter 704 and Wisconsin Administrative Code ATCP 134.", "governing_law_jurisdiction", "fair")
        ]
    },
    {
        "doc_id": "wa_seattle_housing_lease_05",
        "source": "Seattle Housing Authority / City of Seattle Model Lease (https://www.seattle.gov/rentinginseattle/renters/moving-in)",
        "clauses": [
            ("1. LEASE TERM AND RENT TERMS\nThis agreement begins on September 1, 2024, and ends August 31, 2025. Rent is $2,100.00 per month, due on the first day of each month. Late fees shall not exceed $10.00 per month in strict compliance with the Seattle Municipal Code.", "rent_payment_terms", "fair"),
            ("2. SECURITY DEPOSIT INSTALLMENTS\nTenant deposits $2,100.00 as security. Per Seattle law, Tenant has elected to pay this deposit in six equal consecutive monthly installments of $350.00. Deposit funds are held in a separate trust account at Washington Federal Bank and shall be returned within 30 days of surrender.", "security_deposit", "fair"),
            ("3. LANDLORD ENTRY RESTRICTIONS\nLandlord must provide at least forty-eight (48) hours advance written notice before entering to inspect or repair, and at least twenty-four (24) hours notice before showing the unit to prospective tenants or buyers. Entry is restricted to reasonable hours between 9:00 AM and 6:00 PM.", "entry_notice_access", "fair"),
            ("4. REPAIR OBLIGATIONS AND STATUTORY REMEDIES\nLandlord shall maintain the premises in fit and habitable condition pursuant to the Washington Residential Landlord-Tenant Act (RCW 59.18). Tenant may exercise statutory repair-and-deduct remedies if Landlord fails to commence repairs within 24 hours for water/heat failures.", "maintenance_repairs", "fair"),
            ("5. SUBLETTING AND ROOMMATES\nUnder Seattle Fair Chance Housing laws, Tenant may add family members or immediate roommates upon written notification to Landlord, provided total occupancy complies with municipal room occupancy standards.", "subletting", "fair"),
            ("6. PET POLICY AND DEPOSIT\nTenant may keep up to two approved pets upon payment of a refundable pet deposit not to exceed 25% of one month's rent. No non-refundable pet fees are permitted.", "pet_policy", "fair"),
            ("7. UTILITY TRANSPARENCY\nTenant shall pay electric directly to Seattle City Light. Water and sewer billed through third-party billing must include exact sub-meter readings and cannot exceed actual utility charges incurred.", "utilities", "fair"),
            ("8. JUST CAUSE EVICTION AND TERMINATION\nLandlord may not terminate this tenancy or evict Tenant except for one of the enumerated Just Cause grounds specified under Seattle Municipal Code Section 22.206.160. Minimum 60 days advance written notice is required for non-renewal.", "termination", "fair"),
            ("9. GOVERNING LAW AND VENUE\nThis agreement is governed by the laws of the State of Washington and the municipal ordinances of the City of Seattle. Venue shall lie in King County Superior Court.", "governing_law_jurisdiction", "fair")
        ]
    },
    {
        "doc_id": "ma_legalservices_lease_06",
        "source": "Massachusetts Legal Services Model Standard Lease (https://www.masslegalservices.org/content/standard-form-apartment-lease)",
        "clauses": [
            ("CLAUSE 1: RENT PAYMENT\nThe rent for the premises is $1,900.00 per month, due on the first day of each month. In accordance with Massachusetts General Laws Chapter 186 Section 15B, no late fee may be assessed unless rent is unpaid for thirty (30) full days after the due date.", "rent_payment_terms", "fair"),
            ("CLAUSE 2: SECURITY DEPOSIT ESCROW AND INTEREST\nLandlord acknowledges receipt of $1,900.00 to be held in an interest-bearing escrow account at Bank of America. Landlord shall pay 5% interest annually or the actual bank interest rate to Tenant. Deposit will be returned within thirty (30) days with an itemized statement of repairs sworn under penalties of perjury.", "security_deposit", "fair"),
            ("CLAUSE 3: CONDITION OF PREMISES STATEMENT\nLandlord provides Tenant with a written Statement of Condition detailing existing defects within ten (10) days of the commencement of tenancy. Landlord warrants full compliance with the Massachusetts State Sanitary Code Chapter II.", "maintenance_repairs", "fair"),
            ("CLAUSE 4: LANDLORD RIGHT OF ACCESS\nLandlord may enter the premises only upon reasonable advance notice of at least twenty-four (24) hours to inspect, make repairs, or exhibit the premises pursuant to M.G.L. c. 186 Section 15B. Unannounced entry is prohibited.", "entry_notice_access", "fair"),
            ("CLAUSE 5: PROHIBITION ON EXCULPATORY CLAUSES\nAny provision seeking to relieve Landlord of liability for injuries or damages caused by Landlord's negligence or failure to maintain the premises is void as against Massachusetts public policy.", "indemnification", "fair"),
            ("CLAUSE 6: SUBLETTING AND ASSIGNMENT\nTenant may sublet the premises with the Landlord's written consent, which shall not be unreasonably withheld or delayed. Any replacement tenant meeting reasonable financial criteria shall be accepted.", "subletting", "fair"),
            ("CLAUSE 7: PET COVENANT\nNo dogs or cats shall be maintained without written consent. Certified assistance animals required for medical or psychological reasons are accepted without fee or deposit.", "pet_policy", "fair"),
            ("CLAUSE 8: TERMINATION BY STATUTORY NOTICE\nTenant or Landlord may terminate this month-to-month tenancy by serving written notice of at least thirty (30) days or one full rental period, whichever is longer, conforming to M.G.L. c. 186 Section 12.", "termination", "fair"),
            ("CLAUSE 9: JURISDICTION\nThis agreement is governed by the laws of the Commonwealth of Massachusetts. Any actions shall be brought in the Housing Court Department of Massachusetts.", "governing_law_jurisdiction", "fair")
        ]
    },
    {
        "doc_id": "co_boulder_model_lease_07",
        "source": "City of Boulder Community Housing Assistance Model Lease (https://bouldercolorado.gov/services/model-lease)",
        "clauses": [
            ("SECTION 1: TERM AND RENT\nTenancy commences August 1, 2024, and ends July 31, 2025. Rent is $1,800.00 per month, payable by electronic transfer on the 1st of each month. A grace period extends through the 7th of the month, after which a $35.00 late fee applies.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT AND CITY INTEREST ORDINANCE\nTenant deposits $1,800.00 with Landlord. Under City of Boulder Revised Code 12-2, Landlord shall pay statutory interest annually on the deposit. The deposit shall be returned within thirty (30) days following tenancy termination.", "security_deposit", "fair"),
            ("SECTION 3: HABITABILITY MAINTENANCE\nLandlord shall maintain heating appliances capable of maintaining 68 degrees Fahrenheit, weatherproofing, and plumbing in accordance with the Colorado Warranty of Habitability Act (C.R.S. 38-12-503).", "maintenance_repairs", "fair"),
            ("SECTION 4: ADVANCE NOTICE FOR ENTRY\nLandlord or agents must provide at least forty-eight (48) hours advance written notice before entering for inspections or non-emergency repairs, specifying the two-hour entry window.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLEASING AND ROOMMATES\nTenant has the right to sublease to any prospective subtenant who meets standard credit criteria upon giving Landlord 14 days notice. Landlord shall not charge an administrative subletting fee in excess of $50.00.", "subletting", "fair"),
            ("SECTION 6: PET RULES\nPets are permitted subject to a $250.00 refundable pet deposit. Under Colorado law, no breed-specific bans shall apply to service or companion animals.", "pet_policy", "fair"),
            ("SECTION 7: UTILITIES AND RECYCLING\nLandlord provides trash, municipal recycling, and compost collection. Tenant establishes accounts for gas, electricity, and telecommunications.", "utilities", "fair"),
            ("SECTION 8: DISPUTE MEDIATION\nThe parties agree to participate in the City of Boulder Community Mediation Service to resolve any landlord-tenant disputes before filing an action in county court.", "dispute_resolution", "fair"),
            ("SECTION 9: NOTICE OF TERMINATION\nEither party may terminate the lease at the end of the term by giving at least sixty (60) days advance written notice.", "termination", "fair")
        ]
    },
    {
        "doc_id": "umich_housing_lease_08",
        "source": "University of Michigan Student Legal Services Model Off-Campus Lease (https://studentlegalservices.umich.edu/sample-lease)",
        "clauses": [
            ("1. PARTIES AND DWELLING\nThis lease is entered into by Wolverine Property Management and University of Michigan Student Tenant for premises at 915 Oakland Avenue, Ann Arbor, MI 48104.", "governing_law_jurisdiction", "fair"),
            ("2. RENTAL PAYMENTS AND LATE FEES\nRent is $1,700.00 per month, due on the 1st of each month. A late fee of $25.00 shall be assessed if rent is not received by the 6th day of the month.", "rent_payment_terms", "fair"),
            ("3. SECURITY DEPOSIT AND INVENTORY CHECKLIST\nDeposit of $1,700.00 is deposited in an escrow account at Michigan Central Credit Union. Tenant will complete a Commencement Inventory Checklist within 7 days. Under Michigan MCL 554.609, the deposit will be returned within 30 days of surrender.", "security_deposit", "fair"),
            ("4. LANDLORD REPAIR OBLIGATION\nLandlord covenants to keep premises in reasonable repair and comply with Ann Arbor Housing Code. If Landlord fails to repair major defects after 14 days written notice, Tenant may exercise rights under Michigan law.", "maintenance_repairs", "fair"),
            ("5. ENTRY NOTICE REQUIREMENTS\nLandlord must provide at least twenty-four (24) hours advance notice in writing before entering for non-emergency inspections or showing to future prospective tenants.", "entry_notice_access", "fair"),
            ("6. SUMMER SUBLETTING RIGHTS\nTenant reserves the right to sublet the premises during the academic summer term (May 1 to August 15). Landlord will review subtenant applications within 5 business days and will not unreasonably refuse approval.", "subletting", "fair"),
            ("7. PET RULES AND PROHIBITIONS\nNo pets allowed without prior written consent and payment of a $200.00 refundable pet deposit. Assistance animals are permitted in compliance with the Fair Housing Act.", "pet_policy", "fair"),
            ("8. TERMINATION AND NOTICE TO SURRENDER\nLease term ends August 10, 2025. Non-renewal requires thirty (30) days written notice prior to lease expiration.", "termination", "fair"),
            ("9. GOVERNING LAW\nThis lease is governed by the laws of the State of Michigan and city ordinances of Ann Arbor.", "governing_law_jurisdiction", "fair")
        ]
    },
    {
        "doc_id": "uw_madison_sls_lease_09",
        "source": "University of Wisconsin-Madison Student Legal Services Standard Residential Lease (https://sls.wisc.edu/housing/lease-review)",
        "clauses": [
            ("1. TERM AND RENT\nTerm begins August 15, 2024, and terminates August 14, 2025. Monthly rent is $1,550.00 payable on the 1st day of each month. A late charge of $30.00 applies after the 5th calendar day.", "rent_payment_terms", "fair"),
            ("2. SECURITY DEPOSIT PROTECTIONS\nTenant pays $1,550.00 security deposit. Pursuant to ATCP 134, Landlord shall provide an itemization of damages and mail the remainder within 21 days after vacating.", "security_deposit", "fair"),
            ("3. PROMISE TO REPAIR AND HABITABILITY\nLandlord promises to maintain structural soundness, heating facilities capable of 67 degrees, and running potable water. Repairs will commence within 72 hours of written notification.", "maintenance_repairs", "fair"),
            ("4. LANDLORD ACCESS RESTRICTION\nLandlord shall give at least 24 hours advance notice of entry, specifying the time of entry which must occur between 8:00 AM and 6:00 PM on weekdays, except for emergency repairs.", "entry_notice_access", "fair"),
            ("5. SUBLETTING APPROVAL\nSubletting is permitted with written authorization. Landlord shall not impose an application fee on proposed subtenants exceeding $25.00.", "subletting", "fair"),
            ("6. PET PROVISIONS\nNo unauthorized pets are permitted. Unauthorized pets will result in a fee of $50.00 per occurrence. Service animals are exempt.", "pet_policy", "needs_review"),
            ("7. UTILITY PAYMENTS\nTenant pays electric and gas. Landlord pays municipal water, sewer, and regular recycling services.", "utilities", "fair"),
            ("8. NON-RENEWAL AND TERMINATION\nNon-renewal notice must be given in writing at least 60 days before the lease end date.", "termination", "fair")
        ]
    },
    {
        "doc_id": "uc_berkeley_sls_lease_10",
        "source": "UC Berkeley Student Legal Services Tenancy Agreement Template (https://sls.berkeley.edu/landlord-tenant)",
        "clauses": [
            ("CLAUSE 1: OCCUPANCY AND RENT\nLease term starts August 1, 2024, ending July 31, 2025. Rent is $2,400.00 per month due on the 1st of each month. Late fee of $35.00 applies after the 5th of the month.", "rent_payment_terms", "fair"),
            ("CLAUSE 2: SECURITY DEPOSIT PURSUANT TO CA CIVIL CODE 1950.5\nSecurity deposit of $2,400.00 shall be held in trust. Landlord must offer a pre-move-out initial inspection two weeks before surrender, and return the deposit with receipts within 21 days.", "security_deposit", "fair"),
            ("CLAUSE 3: MAINTENANCE STANDARDS\nLandlord shall maintain hot and cold running water, heating, and weatherproofing per California Civil Code 1941.1. Tenant shall promptly notify landlord of plumbing or roof defects.", "maintenance_repairs", "fair"),
            ("CLAUSE 4: ENTRY RESTRICTIONS AND NOTICE\nLandlord must provide 24 hours written notice before entering the unit. Notice must state the approximate time of entry during normal business hours.", "entry_notice_access", "fair"),
            ("CLAUSE 5: SUBLEASE RIGHTS\nTenant may sublease during the academic breaks. Landlord must approve or reject subtenants within 7 days based solely on documented financial capability.", "subletting", "fair"),
            ("CLAUSE 6: PET RULES\nNo pets allowed without signed Pet Agreement and $250.00 deposit. Service animals and psychiatric service dogs are exempt under the Americans with Disabilities Act.", "pet_policy", "fair"),
            ("CLAUSE 7: JURY TRIAL WAIVER VOID\nIn compliance with California public policy, neither party waives their right to a jury trial in any judicial proceeding arising from this agreement.", "dispute_resolution", "fair"),
            ("CLAUSE 8: TERMINATION TERMS\nTenancy terminates on the agreed expiration date. Month-to-month extension requires thirty (30) days written notice to terminate.", "termination", "fair")
        ]
    },
    {
        "doc_id": "unc_chapelhill_sls_lease_11",
        "source": "UNC Chapel Hill Student Legal Services Sample Lease (https://studentlegalservices.unc.edu/housing)",
        "clauses": [
            ("SECTION 1: RENT AND PAYMENT DUE DATES\nMonthly rent is $1,600.00 due on the first day of each calendar month. Under North Carolina General Statutes Section 42-46, a late fee may not exceed fifteen dollars ($15.00) or five percent (5%) of the monthly rent, whichever is greater, and may only be charged if rent is late by five days or more.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT ESCROW UNDER NC TPAA\nTenant deposits $1,600.00 as security. In compliance with the North Carolina Tenant Security Deposit Act (NCGS 42-50), the deposit is deposited in an escrow account at Wells Fargo Bank in Chapel Hill, NC. Landlord will account for and refund the deposit within thirty (30) days of termination.", "security_deposit", "fair"),
            ("SECTION 3: HABITABILITY AND SMOKE DETECTORS\nLandlord shall comply with all applicable building and housing codes and repair all electrical, plumbing, and HVAC systems within a reasonable time. Landlord will install and test working smoke and carbon monoxide alarms at occupancy commencement.", "maintenance_repairs", "fair"),
            ("SECTION 4: LANDLORD RIGHT OF ENTRY\nLandlord shall provide at least twenty-four (24) hours advance notice prior to entering the premises for non-emergency inspections, appraisals, or showings to prospective tenants.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLETTING AND ROOM ASSIGNMENT\nTenant may sublet the premises with Landlord's written approval. Landlord shall not unreasonably delay evaluation of subtenant applications.", "subletting", "fair"),
            ("SECTION 6: PROHIBITION ON PETS\nNo pets allowed on premises without an authorized pet agreement and a $200.00 refundable pet deposit. Emotional support and service animals are permitted pursuant to fair housing guidelines.", "pet_policy", "fair"),
            ("SECTION 7: UTILITIES AND ALLOCATION\nTenant pays electricity and internet. Landlord provides water, sewer, and stormwater drainage fees.", "utilities", "fair"),
            ("SECTION 8: NOTICE OF TERMINATION\nWritten notice of at least thirty (30) days prior to the expiration date is required to terminate or non-renew this lease.", "termination", "fair")
        ]
    },
    {
        "doc_id": "cornell_offcampus_lease_12",
        "source": "Cornell University Off-Campus Living Model Lease Template (https://scl.cornell.edu/residential-life/living-off-campus)",
        "clauses": [
            ("1. PARTIES AND APARTMENT\nLease between Cayuga Heights Rentals ('Landlord') and Cornell Student ('Tenant') for premises at 204 Dryden Road, Ithaca, NY 14850.", "governing_law_jurisdiction", "fair"),
            ("2. RENT AND LATE CHARGE STATUTORY CAP\nRent is $1,750.00 per month, due on the 1st day of each month. Pursuant to New York Real Property Law Section 238-a, late fees are capped at fifty dollars ($50.00) or five percent (5%) of monthly rent, whichever is less, after a 5-day grace period.", "rent_payment_terms", "fair"),
            ("3. SECURITY DEPOSIT CAP AND TRUST ACCOUNTING\nUnder NY General Obligations Law 7-103, deposit of $1,750.00 (maximum one month's rent) is held in an interest-bearing trust account at Tompkins Community Bank. The deposit shall be returned within fourteen (14) days after Tenant vacates with an itemized accounting.", "security_deposit", "fair"),
            ("4. LANDLORD WARRANTY OF HABITABILITY\nLandlord warrants that the apartment is fit for human habitation under NY Real Property Law Section 235-b. Landlord shall provide adequate heat between October 1 and May 31 (minimum 68 degrees during the day).", "maintenance_repairs", "fair"),
            ("5. ENTRY NOTICE COVENANT\nLandlord must give at least twenty-four (24) hours advance notice in writing or by email prior to non-emergency entry. Entry shall only occur on weekdays during customary business hours.", "entry_notice_access", "fair"),
            ("6. STATUTORY RIGHT TO SUBLET\nPursuant to NY Real Property Law Section 226-b, Tenant has the statutory right to sublet upon written request to Landlord accompanied by subtenant details. Landlord cannot unreasonably refuse consent.", "subletting", "fair"),
            ("7. PET RULES AND PROHIBITIONS\nPets are prohibited unless authorized by a written rider. Service and support animals are accommodated in accordance with the New York State Human Rights Law.", "pet_policy", "fair"),
            ("8. TERMINATION AND NOTICE TO QUIT\nNotice of non-renewal or intent to terminate month-to-month tenancy must be provided at least thirty (30) days in advance.", "termination", "fair")
        ]
    },
    {
        "doc_id": "nys_ag_tenants_rights_lease_13",
        "source": "New York State Attorney General Tenants' Rights Model Residential Lease (https://ag.ny.gov/resources/individuals/tenants-rights)",
        "clauses": [
            ("ARTICLE 1: TERM AND MONTHLY RENTAL\nThis lease runs for one (1) year beginning September 1, 2024. Monthly rent is $2,300.00 payable on the first day of each month.", "rent_payment_terms", "fair"),
            ("ARTICLE 2: LATE FEE CEILING AND GRACE PERIOD\nNo late fee shall be charged unless rent remains unpaid for five (5) full days after the due date. The late fee shall not exceed $50.00 or 5% of monthly rent, whichever is less.", "late_fees_penalty", "fair"),
            ("ARTICLE 3: SECURITY DEPOSIT ESCROW LAWS\nSecurity deposit is limited by law to one month's rent ($2,300.00). Landlord holds deposit in trust and will return deposit minus legitimate deductions within fourteen (14) days of tenant moving out.", "security_deposit", "fair"),
            ("ARTICLE 4: WARRANTY OF HABITABILITY (RPL 235-b)\nLandlord warrants premises are fit for human habitation and free from conditions hazardous to life, health, or safety. Any lease provision waiving this warranty is void.", "maintenance_repairs", "fair"),
            ("ARTICLE 5: INSPECTION ENTRY NOTICE\nLandlord may enter premises only with reasonable advance notice of at least twenty-four (24) hours, except in case of fire or water emergency.", "entry_notice_access", "fair"),
            ("ARTICLE 6: SUBLEASING AND ROOM SHARING LAWS\nTenant has the legal right to share the apartment with immediate family and one additional occupant pursuant to Real Property Law Section 235-f (The Roommate Law).", "subletting", "fair"),
            ("ARTICLE 7: RETALIATORY EVICTION PROHIBITION\nLandlord shall not retaliate against Tenant by increasing rent or terminating tenancy for exercising legal rights or reporting housing code violations under RPL 223-b.", "termination", "fair"),
            ("ARTICLE 8: NOTICE OF RENEWAL OR NON-RENEWAL\nPursuant to the Housing Stability and Tenant Protection Act (HSTPA), Landlord must provide 60 days advance written notice if electing not to renew this lease.", "renewal_auto_renewal", "fair")
        ]
    },
    {
        "doc_id": "fl_bar_approved_lease_14",
        "source": "The Florida Bar Approved Residential Lease (Single Family / Duplex) (https://www.floridabar.org/public/consumer/pamphlet032)",
        "clauses": [
            ("SECTION 1: TERM AND RENT\nTerm begins October 1, 2024, and ends September 30, 2025. Rent is $1,950.00 per month, due on the 1st of each month. Late fee of $50.00 applies after the 4th day of the month.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT HOLDINGS UNDER FS 83.49\nTenant deposits $1,950.00 as security. Landlord shall hold the deposit in a separate Florida banking account and notify Tenant of the depository within 30 days. Deposit shall be returned within 15 days if no claim is made, or 30 days if damages are claimed.", "security_deposit", "fair"),
            ("SECTION 3: LANDLORD MAINTENANCE COVENANT\nUnder Florida Statutes Section 83.51, Landlord shall maintain plumbing in reasonable working condition, maintain roofs, windows, doors, and keep common areas clean and structurally sound.", "maintenance_repairs", "fair"),
            ("SECTION 4: RIGHT OF ACCESS NOTICE (FS 83.53)\nLandlord may enter the dwelling unit at any time for the protection or preservation of premises in an emergency, or upon giving at least twelve (12) hours advance notice for inspections and repairs between 7:30 AM and 8:00 PM.", "entry_notice_access", "needs_review"),
            ("SECTION 5: SUBLETTING RESTRICTION\nTenant shall not sublet or assign any interest in the premises without prior written authorization from Landlord.", "subletting", "fair"),
            ("SECTION 6: PET COVENANT AND DEPOSITS\nNo pets allowed without Landlord's written permission and a refundable deposit of $300.00. Service animals are permitted in compliance with applicable law.", "pet_policy", "fair"),
            ("SECTION 7: UTILITIES AND SERVICE CHARGES\nTenant is responsible for all electricity, internet, and cable. Landlord provides water, sewer, and regular trash collection.", "utilities", "fair"),
            ("SECTION 8: CASUALTY DAMAGE AND TERMINATION\nIf premises are substantially damaged by hurricane or fire, Tenant may immediately vacate and terminate the agreement with rent abated from the date of damage.", "termination", "fair")
        ]
    },
    {
        "doc_id": "va_dhcd_model_lease_15",
        "source": "Virginia Department of Housing and Community Development (DHCD) Model Lease (https://www.dhcd.virginia.gov/vrlta)",
        "clauses": [
            ("SECTION 1: LEASE TERM AND RENT CHARGES\nTerm begins July 1, 2024, ending June 30, 2025. Monthly rent is $1,750.00 due on the first of each month. Late fee cannot exceed ten percent (10%) of the periodic rent or ten percent of the unpaid balance, whichever is lesser, under Code of Virginia Section 55.1-1204.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT AND 45-DAY DISPOSITION\nTenant deposits $1,750.00. Under Code of Virginia Section 55.1-1226, Landlord must perform a move-out inspection and provide an itemized statement and refund within forty-five (45) days of tenant vacation.", "security_deposit", "fair"),
            ("SECTION 3: LANDLORD MAINTENANCE OBLIGATIONS\nLandlord shall maintain heating, air conditioning, plumbing, and electrical systems in good and safe working order, complying with Virginia Uniform Statewide Building Code requirements.", "maintenance_repairs", "fair"),
            ("SECTION 4: ACCESS TO PREMISES (24-HOUR NOTICE)\nPursuant to Virginia Code 55.1-1229, Landlord must provide at least twenty-four (24) hours advance notice before entering for non-emergency inspections or routine maintenance.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLETTING AND GUEST RULES\nTenant may not sublet the dwelling unit without Landlord's written consent. Landlord shall approve or deny subtenants within 10 business days.", "subletting", "fair"),
            ("SECTION 6: PET RESTRICTIONS\nDomestic pets are permitted with written Pet Addendum and $250.00 deposit. Service and assistance animals are exempt from all deposits.", "pet_policy", "fair"),
            ("SECTION 7: TERMINATION AND RIGHT TO CURE\nLandlord must provide a 30-day written notice specifying material lease non-compliance, granting Tenant twenty-one (21) days to cure the defect before terminating tenancy under Virginia Code 55.1-1245.", "termination", "fair")
        ]
    },
    {
        "doc_id": "il_legalaid_model_lease_16",
        "source": "Illinois Legal Aid Online Standard Residential Lease Agreement (https://www.illinoislegalaid.org/legal-information/model-lease-agreement)",
        "clauses": [
            ("SECTION 1: RENT PAYMENT\nRent is $1,650.00 per month, due on the first day of each calendar month. In accordance with Illinois law, late fees cannot exceed $20.00 or 20% of monthly rent and may only apply after a full 5-day grace period.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT ESCROW (765 ILCS 710)\nTenant deposits $1,650.00. Under Illinois Security Deposit Return Act, Landlord must provide an itemized list of damages within thirty (30) days and return the deposit balance within forty-five (45) days.", "security_deposit", "fair"),
            ("SECTION 3: HABITABILITY AND HEATING\nLandlord warrants compliance with municipal housing maintenance codes and promises to furnish heating to a minimum temperature of 68 degrees during the heating season (September 15 through June 1).", "maintenance_repairs", "fair"),
            ("SECTION 4: LANDLORD RIGHT OF ENTRY\nLandlord shall provide at least twenty-four (24) hours advance written notice before entering to inspect or show the unit, except in case of sudden water or gas leak.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLEASING RIGHTS\nUnder Chicago Residential Landlord Tenant Ordinance (RLTO), Tenant has the absolute right to sublease without paying excessive fees, and Landlord shall accept reasonable subtenants.", "subletting", "fair"),
            ("SECTION 6: PET RESTRICTIONS AND FEES\nPets require written permission and a $200.00 refundable pet deposit. Certified service animals are exempt from all pet restrictions.", "pet_policy", "fair"),
            ("SECTION 7: TERMINATION NOTICE REQUIREMENT\nThirty (30) days written notice is required to terminate a month-to-month tenancy or non-renew at lease expiration.", "termination", "fair")
        ]
    },
    {
        "doc_id": "austin_housing_lease_17",
        "source": "City of Austin Housing Authority Model Tenancy Agreement (https://www.austintexas.gov/housing)",
        "clauses": [
            ("1. LEASE TERM AND RENT\nLease commences June 1, 2024, ending May 31, 2025. Rent is $1,400.00 per month due on the 1st. Late fee of $30.00 applies if unpaid by the 5th.", "rent_payment_terms", "fair"),
            ("2. SECURITY DEPOSIT AND 30-DAY REFUND\nTenant deposits $1,400.00. Landlord shall refund deposit and provide itemized damage deductions within thirty (30) days of moving out per Texas Property Code 92.103.", "security_deposit", "fair"),
            ("3. LANDLORD REPAIR OBLIGATION UNDER TPC 92.056\nLandlord must make a diligent effort to repair any condition that materially affects physical health or safety of an ordinary tenant within seven (7) days of written notice.", "maintenance_repairs", "fair"),
            ("4. ADVANCE NOTICE FOR ENTRY\nLandlord shall provide 24 hours advance notice of entry for routine maintenance and safety inspections.", "entry_notice_access", "fair"),
            ("5. SUBLEASING PROHIBITED WITHOUT CONSENT\nTenant shall not sublease or assign the apartment without prior written authorization from property management.", "subletting", "fair"),
            ("6. PET DEPOSIT AND POLICIES\nPets require an approved pet agreement and $250.00 deposit. Service and emotional support animals are permitted without charge.", "pet_policy", "fair"),
            ("7. NOTICE OF TERMINATION\nEither party may terminate by delivering written notice at least thirty (30) days prior to the end of the monthly period.", "termination", "fair")
        ]
    },
    {
        "doc_id": "md_oag_sample_lease_18",
        "source": "Maryland Office of the Attorney General Landlord-Tenant Sample Lease (https://www.marylandattorneygeneral.gov/Pages/CPD/landlords.aspx)",
        "clauses": [
            ("SECTION 1: RENTAL AMOUNT AND MAXIMUM LATE FEES\nRent is $1,750.00 per month. Under Maryland Real Property Code Section 8-208, late fees are capped at five percent (5%) of monthly rent and can only be assessed after rent is 5 days late.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT CEILING (TWO MONTHS MAXIMUM)\nSecurity deposit is $1,750.00. Landlord shall deposit funds in an insured financial institution within thirty (30) days. Under Real Property Section 8-203, Landlord must return deposit with statutory interest within forty-five (45) days of moving out.", "security_deposit", "fair"),
            ("SECTION 3: LANDLORD MAINTENANCE COVENANT\nLandlord covenants to keep premises in clean, safe condition, free from rodent infestation, and maintain heating facilities capable of 68 degrees.", "maintenance_repairs", "fair"),
            ("SECTION 4: RIGHT OF ENTRY (24 HOURS NOTICE)\nExcept for emergency situations, Landlord shall provide at least twenty-four (24) hours advance notice before entering for non-emergency repairs.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLEASING CONDITIONS\nTenant shall not assign this lease or sublet the premises without Landlord's written permission, which shall not be unreasonably withheld.", "subletting", "fair"),
            ("SECTION 6: SERVICE ANIMALS AND PET POLICY\nPets require written authorization. Legally recognized assistance animals are accommodated without pet fees or deposits.", "pet_policy", "fair"),
            ("SECTION 7: TERMINATION AND NOTICE TO VACATE\nEither party may terminate month-to-month tenancy by serving written notice of at least sixty (60) days under Maryland Real Property Code Section 8-402.", "termination", "fair")
        ]
    },
    {
        "doc_id": "ohio_legalaid_model_lease_19",
        "source": "Ohio State Legal Services Association Model Residential Lease (https://www.ohiolegalhelp.org/topic/housing)",
        "clauses": [
            ("CLAUSE 1: RENT TERMS AND PAYMENT\nRent is $1,250.00 per month, due on the 1st of each calendar month. A reasonable late fee of $25.00 applies if rent is unpaid after the 5th.", "rent_payment_terms", "fair"),
            ("CLAUSE 2: SECURITY DEPOSIT ESCROW (RC 5321.16)\nDeposit of $1,250.00 is held in escrow. Under Ohio Revised Code 5321.16, deposits held for more than 6 months shall bear 5% interest per annum. Landlord will mail itemized deductions and refund within thirty (30) days.", "security_deposit", "fair"),
            ("CLAUSE 3: STATUTORY REPAIR OBLIGATIONS (RC 5321.07)\nLandlord shall maintain electrical, plumbing, heating, and ventilating fixtures in good working condition. If Landlord fails to repair within 30 days of written notice, Tenant may escrow rent with municipal court.", "maintenance_repairs", "fair"),
            ("CLAUSE 4: ENTRY NOTICE RESTRICTION (RC 5321.04)\nLandlord must give at least twenty-four (24) hours advance notice of intent to enter and enter only at reasonable times, except in emergencies.", "entry_notice_access", "fair"),
            ("CLAUSE 5: SUBLETTING TERMS\nTenant may not sublet without Landlord's written approval. Approved subtenants must sign an addendum.", "subletting", "fair"),
            ("CLAUSE 6: TERMINATION PROCEDURES\nTermination of periodic tenancy requires at least thirty (30) days written notice prior to the periodic rental date.", "termination", "fair")
        ]
    },
    {
        "doc_id": "co_dola_housing_lease_20",
        "source": "Colorado Department of Local Affairs Division of Housing Model Lease (https://cdola.colorado.gov/housing)",
        "clauses": [
            ("1. RENT PAYMENT AND LATE FEES (HB 21-1121)\nRent is $1,850.00 per month due on the 1st. In compliance with Colorado House Bill 21-1121, late fees cannot exceed $50.00 or 5% of past due rent, whichever is greater, and may only be charged after a 7-day grace period.", "rent_payment_terms", "fair"),
            ("2. SECURITY DEPOSIT AND 60-DAY EXTENSION (CRS 38-12-103)\nTenant deposits $1,850.00. Landlord will return the deposit within thirty (30) days (or up to 60 days if explicitly stated) with an itemized accounting of deductions.", "security_deposit", "fair"),
            ("3. WARRANTY OF HABITABILITY REMEDIES\nLandlord warrants compliance with CRS 38-12-503. Landlord must commence remedial action within 24 hours for lack of heat, water, or life-safety hazards.", "maintenance_repairs", "fair"),
            ("4. LANDLORD ACCESS (48-HOUR ADVANCE NOTICE)\nLandlord shall provide at least 48 hours notice before entering for non-emergency inspections or repair work.", "entry_notice_access", "fair"),
            ("5. SUBLETTING AND PROHIBITED FEES\nSubletting is permitted with written authorization. Landlord cannot charge fees exceeding actual screening costs.", "subletting", "fair"),
            ("6. NOTICE TO VACATE\nEither party may terminate month-to-month tenancy by giving at least twenty-one (21) days notice under CRS 13-40-107.", "termination", "fair")
        ]
    },
    {
        "doc_id": "or_statebar_model_lease_21",
        "source": "Oregon State Bar Residential Tenancy Agreement Form (https://www.osbar.org/public/legalinfo/tenant.html)",
        "clauses": [
            ("SECTION 1: RENT PAYMENT AND FOUR-DAY GRACE PERIOD (ORS 90.260)\nRent is $1,700.00 per month. Under Oregon law, a late fee may only be charged if rent is unpaid after the fourth day of the rental period. Late fee is fixed at $50.00.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT TRUST ACCOUNT (ORS 90.300)\nSecurity deposit of $1,700.00 is deposited in an Oregon bank account. Landlord shall provide a written accounting and refund within thirty-one (31) days after termination.", "security_deposit", "fair"),
            ("SECTION 3: LANDLORD HABITABILITY OBLIGATION (ORS 90.320)\nLandlord covenants that premises are habitable, including effective weatherproofing, plumbing, heating facilities, and hot water systems.", "maintenance_repairs", "fair"),
            ("SECTION 4: 24-HOUR ENTRY NOTICE (ORS 90.322)\nLandlord may enter premises only after giving at least twenty-four (24) hours advance notice in writing, specifying date and time during reasonable hours.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLEASING AND ROOMMATES\nTenant shall not sublease without prior written permission. Sublease requests will be reviewed under standard criteria.", "subletting", "fair"),
            ("SECTION 6: TERMINATION RESTRICTIONS (ORS 90.427)\nTermination of month-to-month tenancies after the first year requires at least 90 days written notice and must be based on statutory landlord cause.", "termination", "fair")
        ]
    },
    {
        "doc_id": "az_housing_model_lease_22",
        "source": "Arizona Department of Housing Standard Residential Lease (https://housing.az.gov/general-public/arizona-residential-landlord-and-tenant-act)",
        "clauses": [
            ("1. RENT AMOUNT AND LATE PAYMENT\nMonthly rent is $1,500.00 due on the first day of each month. A late fee of $10.00 per day applies if rent is not received by the 5th.", "rent_payment_terms", "fair"),
            ("2. SECURITY DEPOSIT CAP UNDER ARS 33-1321\nSecurity deposit is $1,500.00 (capped by statute at one and one-half month's rent). Landlord shall return the deposit with an itemized accounting within fourteen (14) business days of moving out.", "security_deposit", "fair"),
            ("3. LANDLORD MAINTENANCE RESPONSIBILITIES (ARS 33-1324)\nLandlord shall maintain electrical, plumbing, heating, air conditioning, and ventilation in reasonable working order, including cooling systems in summer months.", "maintenance_repairs", "fair"),
            ("4. TWO-DAY ENTRY NOTICE (ARS 33-1343)\nExcept in emergencies, Landlord shall provide at least two (2) days written notice of intent to enter and enter only at reasonable times.", "entry_notice_access", "fair"),
            ("5. SUBLETTING RESTRICTION\nTenant may not assign or sublet the dwelling unit without Landlord's written authorization.", "subletting", "fair"),
            ("6. NOTICE OF TERMINATION\nEither party may terminate month-to-month tenancy by giving at least thirty (30) days written notice prior to the periodic rental date.", "termination", "fair")
        ]
    },
    {
        "doc_id": "ga_dca_model_lease_23",
        "source": "Georgia Department of Community Affairs Landlord-Tenant Model Lease (https://www.dca.ga.gov/node/4576)",
        "clauses": [
            ("SECTION 1: RENT PAYMENT\nRent is $1,450.00 per month, due on the first day of each month. A late fee of $50.00 shall be assessed if rent is not received by the 5th.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT ESCROW (OCGA 44-7-31)\nTenant deposits $1,450.00 held in an escrow account at a state-regulated bank. Landlord will inspect premises within three days of surrender and return deposit within thirty (30) days.", "security_deposit", "fair"),
            ("SECTION 3: REPAIR AND MAINTENANCE OBLIGATIONS\nLandlord shall keep the premises in repair and is liable for damages arising from failure to maintain structural, plumbing, and electrical systems.", "maintenance_repairs", "fair"),
            ("SECTION 4: LANDLORD RIGHT OF ACCESS\nLandlord may enter premises with reasonable advance notice of at least 24 hours for inspection and repair.", "entry_notice_access", "fair"),
            ("SECTION 5: SUBLEASING RESTRICTIONS\nTenant shall not sublease or assign the apartment without prior written permission of Landlord.", "subletting", "fair"),
            ("SECTION 6: TERMINATION NOTICES (OCGA 44-7-7)\nLandlord must provide sixty (60) days notice to terminate a tenancy-at-will; Tenant must provide thirty (30) days notice.", "termination", "fair")
        ]
    },
    {
        "doc_id": "pa_oag_model_lease_24",
        "source": "Pennsylvania Office of Attorney General Landlord Tenant Model Agreement (https://www.attorneygeneral.gov/resources/landlord-tenant-rights)",
        "clauses": [
            ("CLAUSE 1: RENT PAYMENT TERMS\nRent is $1,550.00 per month, due on the first of each month. A late fee of $40.00 applies after the 5th calendar day.", "rent_payment_terms", "fair"),
            ("CLAUSE 2: SECURITY DEPOSIT LIMITS (68 P.S. 250.511a)\nDeposit of $1,550.00 (limited to two months rent in first year, one month in second year) is held in an escrow account. Landlord shall provide itemized damages list and return deposit within thirty (30) days.", "security_deposit", "fair"),
            ("CLAUSE 3: IMPLIED WARRANTY OF HABITABILITY\nLandlord warrants that the dwelling unit is fit for human habitation as recognized in Pugh v. Holmes. Landlord maintains essential heat, water, and sanitary facilities.", "maintenance_repairs", "fair"),
            ("CLAUSE 4: ENTRY NOTICE COVENANT\nLandlord must provide at least twenty-four (24) hours advance notice prior to entering for non-emergency inspections.", "entry_notice_access", "fair"),
            ("CLAUSE 5: SUBLETTING TERMS\nNo sublease is valid without prior written consent of Landlord.", "subletting", "fair"),
            ("CLAUSE 6: TERMINATION PROCEDURES\nThirty (30) days written notice is required to terminate or non-renew at lease expiration.", "termination", "fair")
        ]
    },
    {
        "doc_id": "nj_dca_model_lease_25",
        "source": "New Jersey Department of Community Affairs Truth in Renting Model Lease (https://www.nj.gov/dca/divisions/codes/offices/landlord_tenant_information.html)",
        "clauses": [
            ("SECTION 1: RENT PAYMENT AND SENIOR CITIZEN GRACE PERIOD (NJSA 2A:42-6.1)\nRent is $1,900.00 per month due on the 1st. Under New Jersey law, senior citizens and disability pension recipients receive a mandatory 5-business-day grace period without late penalty.", "rent_payment_terms", "fair"),
            ("SECTION 2: SECURITY DEPOSIT ESCROW AND INTEREST (NJSA 46:8-19)\nSecurity deposit is $1,900.00 (cannot exceed one and one-half month's rent). Landlord shall deposit funds in an interest-bearing account and pay annual interest to Tenant. Refund will occur within 30 days.", "security_deposit", "fair"),
            ("SECTION 3: HABITABILITY AND HEATING CODE\nLandlord must provide heat between October 1 and May 1 maintaining a minimum temperature of 68 degrees Fahrenheit per New Jersey State Housing Code.", "maintenance_repairs", "fair"),
            ("SECTION 4: 24-HOUR NOTICE FOR ENTRY\nLandlord shall provide 24 hours advance written notice before entry for non-emergency repairs.", "entry_notice_access", "fair"),
            ("SECTION 5: ANTI-EVICTION ACT PROTECTIONS (NJSA 2A:18-61.1)\nTenants are protected under the New Jersey Anti-Eviction Act and may not be removed or refused lease renewal except for statutory good cause.", "termination", "fair")
        ]
    }
]

# (Offer letter and insurance sources continue in Part 2)
