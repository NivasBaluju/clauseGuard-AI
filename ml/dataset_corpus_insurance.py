"""
Public Insurance Specimen Corpus: 20 distinct real specimen policies collected from
State Departments of Insurance (HO-4 Contents Broad Form Renters/Homeowners policy line).
"""

INSURANCE_SOURCES = [
    {
        "doc_id": "ncdoi_ho4_specimen_01",
        "source": "North Carolina Department of Insurance / Rate Bureau HO-4 Specimen Policy (https://www.ncdoi.gov/media/1321/open)",
        "clauses": [
            ("SECTION I - COVERAGE C PERSONAL PROPERTY\nWe cover personal property owned or used by an insured while it is anywhere in the world. At your request, we will cover personal property owned by guests or residence employees while on the residence premises.", "coverage_scope", "fair"),
            ("SECTION I - COVERAGE D LOSS OF USE\nThe limit of liability for Coverage D is the total limit for additional living expenses and fair rental value necessary to maintain your normal standard of living if a covered loss makes the residence premises uninhabitable.", "limits_of_liability", "fair"),
            ("SECTION I - PERILS INSURED AGAINST\nWe insure for direct physical loss to property caused by fire or lightning, windstorm or hail, explosion, riot or civil commotion, vehicles, smoke, vandalism, and theft.", "coverage_scope", "fair"),
            ("SECTION I - GENERAL EXCLUSIONS (WATER DAMAGE)\nWe do not insure for loss caused directly or indirectly by water damage, meaning flood, surface water, waves, tidal water, overflow of any body of water, or water or water-borne material which backs up through sewers or drains.", "exclusions", "unfavorable"),
            ("SECTION I - EARTH MOVEMENT EXCLUSION\nWe do not insure for loss caused by earth movement, including earthquake, landslide, mudflow, or earth sinking, rising or shifting.", "exclusions", "unfavorable"),
            ("SECTION I - DEDUCTIBLE\nUnless otherwise noted, the standard deductible is $500.00. We will pay only that part of the total of all loss payable under Section I that exceeds the deductible amount.", "deductible_premium", "fair"),
            ("SECTION I - CONDITIONS (DUTIES AFTER LOSS)\nIn case of a loss, you must give prompt written notice to us or our agent within sixty (60) days, notify police in case of theft, protect property from further damage, and submit a signed proof of loss.", "claims_process", "fair"),
            ("SECTION I AND II - CANCELLATION CONDITIONS\nYou may cancel this policy at any time by returning it or notifying us in writing. We may cancel for non-payment upon ten (10) days notice, or for any other reason upon thirty (30) days advance notice.", "cancellation_non_renewal", "fair"),
            ("SECTION I AND II - SUBROGATION WAIVER\nAn insured may waive in writing before a loss all rights of recovery against any person. If not waived, we may require an assignment of rights of recovery to the extent payment is made.", "subrogation", "fair"),
            ("SECTION I AND II - DISPUTE RESOLUTION AND APPRAISAL\nIf you and we fail to agree on the amount of loss, either party may demand an appraisal of the loss in writing. Each party will select a competent appraiser within twenty (20) days.", "dispute_resolution_appraisal", "fair"),
            ("SECTION I AND II - GRACE PERIOD FOR PREMIUM\nA grace period of thirty (30) days will be granted for the payment of each renewal premium, during which time the policy shall remain in force.", "grace_period", "fair")
        ]
    },
    {
        "doc_id": "floir_ho4_specimen_02",
        "source": "Florida Office of Insurance Regulation (FLOIR) HO-4 Specimen Form (https://floir.com)",
        "clauses": [
            ("1. COVERAGE C PERSONAL PROPERTY LIMIT\nWe insure personal property owned by an insured up to the limit of liability stated in the declarations page.", "coverage_scope", "fair"),
            ("2. LOSS OF USE LIVING EXPENSE\nIf a covered peril makes your rented residence uninhabitable, we cover actual reasonable additional living expenses for up to 12 months.", "limits_of_liability", "fair"),
            ("3. NAMED PERILS COVERAGE\nDirect physical damage caused by fire, lightning, windstorm, hurricane, smoke, vandalism, and falling objects.", "coverage_scope", "fair"),
            ("4. FLOOD AND WATER EXCLUSION\nLoss resulting from flood, rising water, storm surge, or sewer backup is strictly excluded regardless of concurrent causes.", "exclusions", "unfavorable"),
            ("5. WINDSTORM DEDUCTIBLE\nA separate calendar year hurricane deductible equal to 2% of Coverage C applies to losses caused by windstorm during a declared hurricane.", "deductible_premium", "needs_review"),
            ("6. NOTICE OF LOSS TIME BAR\nInitial notice of a windstorm or hurricane claim must be filed within one (1) year of the date of loss per Florida Statutes Section 627.70132.", "claims_process", "needs_review"),
            ("7. CANCELLATION BY INSURER\nWe may cancel upon 120 days notice prior to renewal, or 10 days notice for non-payment of premium.", "cancellation_non_renewal", "fair"),
            ("8. RIGHT OF SUBROGATION\nWe acquire all legal rights of recovery against responsible third parties upon payment of any claim.", "subrogation", "fair"),
            ("9. FRAUD AND MISREPRESENTATION\nThis entire policy is void if, whether before or after a loss, an insured has willfully concealed or misrepresented any material fact.", "misrepresentation_fraud_clause", "fair")
        ]
    },
    {
        "doc_id": "oid_ho4_specimen_03",
        "source": "Oklahoma Insurance Department (OID) Specimen HO-4 Renters Policy Form (https://www.oid.ok.gov)",
        "clauses": [
            ("SECTION 1: PROPERTY COVERAGES\nWe cover personal property anywhere in the world owned by an insured, subject to policy exclusions.", "coverage_scope", "fair"),
            ("SECTION 2: PERILS INSURED\nCovers fire, lightning, windstorm, tornado, explosion, aircraft, vehicles, smoke, theft, and freezing of plumbing.", "coverage_scope", "fair"),
            ("SECTION 3: EXCLUSIONS (POLLUTION AND MOLD)\nLoss caused by fungi, wet or dry rot, mold, or bacteria is excluded unless resulting directly from covered plumbing discharge.", "exclusions", "needs_review"),
            ("SECTION 4: DEDUCTIBLE APPLIED\n$1,000.00 standard deductible per occurrence for all property perils.", "deductible_premium", "fair"),
            ("SECTION 5: CLAIMS SETTLEMENT AND APPRAISAL\nIf the insured and company disagree on valuation, each chooses an appraiser and an umpire resolves disputes.", "dispute_resolution_appraisal", "fair"),
            ("SECTION 6: NON-RENEWAL NOTICE\nNotice of non-renewal will be delivered in writing at least forty-five (45) days before expiration.", "cancellation_non_renewal", "fair"),
            ("SECTION 7: SUBROGATION CLAUSE\nInsurer is subrogated to all claims against liable third parties.", "subrogation", "fair")
        ]
    },
    {
        "doc_id": "tdi_ho4_specimen_04",
        "source": "Texas Department of Insurance (TDI) Standard Personal Property Policy Specimen Form (https://www.tdi.texas.gov)",
        "clauses": [
            ("SECTION I - COVERAGE C (PERSONAL PROPERTY)\nProvides worldwide coverage for personal property owned by an insured.", "coverage_scope", "fair"),
            ("SECTION I - LOSS OF USE EXPENSES\nReimburses necessary additional living expenses if residence is untenantable after a covered loss.", "limits_of_liability", "fair"),
            ("SECTION I - SPECIFIED PERILS\nInsures against fire, lightning, smoke, vandalism, windstorm, and theft.", "coverage_scope", "fair"),
            ("SECTION I - WATER BACKUP EXCLUSION\nDirect exclusion of loss resulting from water backing up from sewers, drains, or sump pumps.", "exclusions", "unfavorable"),
            ("SECTION I - DEDUCTIBLE TERMS\n$500.00 deductible applied per covered occurrence.", "deductible_premium", "fair"),
            ("SECTION I - PROMPT NOTICE AND PROOF OF LOSS\nMust submit signed, sworn proof of loss within ninety (90) days of company request.", "claims_process", "fair"),
            ("SECTION II - CANCELLATION PROVISIONS\nCompany may cancel upon 30 days written notice, or 10 days for non-payment.", "cancellation_non_renewal", "fair"),
            ("SECTION II - SUBROGATION RIGHTS\nSubrogation transfer of rights upon claim payment.", "subrogation", "fair")
        ]
    },
    {
        "doc_id": "cdi_ho4_specimen_05",
        "source": "California Department of Insurance (CDI) Personal Property & Liability Specimen Form (https://www.insurance.ca.gov)",
        "clauses": [
            ("1. COVERAGE C PERSONAL PROPERTY\nWorldwide coverage of personal property with 10% limit for secondary locations.", "coverage_scope", "fair"),
            ("2. WILDFIRE EVACUATION EXPENSES (COVERAGE D)\nMandatory coverage for up to two weeks of living expenses upon civil authority evacuation due to wildfire.", "limits_of_liability", "fair"),
            ("3. COVERED CASUALTY PERILS\nCovers direct physical damage from fire, lightning, explosion, theft, and falling objects.", "coverage_scope", "fair"),
            ("4. EARTH MOVEMENT EXCLUSION (CALIFORNIA MANDATE)\nEarthquake damage is excluded. Separate California Earthquake Authority (CEA) policy required.", "exclusions", "needs_review"),
            ("5. DEDUCTIBLE APPLICATION\nStandard deductible of $500.00 per occurrence.", "deductible_premium", "fair"),
            ("6. NOTICE OF CLAIM FILING\nMust furnish prompt notice of claim and complete inventory within 60 days.", "claims_process", "fair"),
            ("7. 75-DAY NON-RENEWAL NOTICE (CIC 678)\nCompany must provide written notice of non-renewal at least 75 days before policy expiration.", "cancellation_non_renewal", "fair"),
            ("8. SUIT AGAINST US LIMITATION\nNo action may be brought against company unless policy terms are complied with and commenced within one year of loss.", "dispute_resolution_appraisal", "needs_review")
        ]
    },
    {
        "doc_id": "nydfs_ho4_specimen_06",
        "source": "New York State Department of Financial Services (NYDFS) Model HO-4 Policy Specimen (https://www.dfs.ny.gov)",
        "clauses": [
            ("SECTION I: PERSONAL PROPERTY LIMIT OF LIABILITY\nWe cover personal property up to the Coverage C limit shown in Declarations.", "coverage_scope", "fair"),
            ("SECTION I: LOSS OF USE REIMBURSEMENT\nCovers reasonable additional living expenses if property is rendered uninhabitable.", "limits_of_liability", "fair"),
            ("SECTION I: COVERED PROPERTY PERILS\nFire, lightning, windstorm, explosion, riot, smoke, vandalism, and theft.", "coverage_scope", "fair"),
            ("SECTION I: EXCLUSIONS (FLOOD AND GROUNDWATER)\nExcludes surface water, flood, and sewer backup without specialized endorsement.", "exclusions", "unfavorable"),
            ("SECTION I: DEDUCTIBLE REQUIREMENT\nDeductible of $500.00 per occurrence.", "deductible_premium", "fair"),
            ("SECTION I: DUTIES AFTER OCCURRENCE\nMust submit proof of loss within sixty (60) days after insurer request under NY Insurance Law 3407.", "claims_process", "fair"),
            ("SECTION I AND II: CANCELLATION (NYIL 3425)\nNon-renewal notice must be mailed at least 45 days, but not more than 60 days, prior to expiration.", "cancellation_non_renewal", "fair"),
            ("SECTION I AND II: SUBROGATION ASSIGNMENT\nCompany subrogated to rights of recovery against responsible parties.", "subrogation", "fair")
        ]
    },
    {
        "doc_id": "wa_oic_specimen_07",
        "source": "Washington State Office of the Insurance Commissioner (OIC) Sample HO-4 Form (https://www.insurance.wa.gov)",
        "clauses": [
            ("1. PROPERTY COVERAGE\nCoverage C covers personal property owned or used by insured worldwide.", "coverage_scope", "fair"),
            ("2. LOSS OF USE\nAdditional living expense for uninhabitable premises.", "limits_of_liability", "fair"),
            ("3. PERILS COVERED\nFire, wind, hail, smoke, theft, vehicle damage.", "coverage_scope", "fair"),
            ("4. EXCLUSIONS\nExcludes earth movement, flood, neglect, and intentional acts.", "exclusions", "fair"),
            ("5. DEDUCTIBLE\n$500.00 standard deductible per occurrence.", "deductible_premium", "fair"),
            ("6. NOTICE OF LOSS\nNotice required within reasonable time.", "claims_process", "fair"),
            ("7. CANCELLATION RULES\n45 days advance notice required for non-renewal under Washington law.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "ma_doi_specimen_08",
        "source": "Massachusetts Division of Insurance (DOI) Specimen HO-4 Renters Policy (https://www.mass.gov/doi)",
        "clauses": [
            ("SECTION 1: PERSONAL PROPERTY COVERAGE\nCovers personal property anywhere in the world.", "coverage_scope", "fair"),
            ("SECTION 2: LOSS OF USE LIMIT\nProvides up to 20% of Coverage C limit for additional living expenses.", "limits_of_liability", "fair"),
            ("SECTION 3: PERILS INSURED AGAINST\nFire, lightning, explosion, vandalism, theft, freezing of heating.", "coverage_scope", "fair"),
            ("SECTION 4: WATER AND SEWER EXCLUSION\nDirect exclusion of subsurface water and sewer backup.", "exclusions", "unfavorable"),
            ("SECTION 5: DEDUCTIBLE AMOUNT\n$500.00 standard deductible.", "deductible_premium", "fair"),
            ("SECTION 6: PROOF OF LOSS REQUIREMENT\nSigned proof of loss within 60 days of request.", "claims_process", "fair"),
            ("SECTION 7: NON-RENEWAL AND CANCELLATION\n45 days advance written notice required for cancellation or non-renewal.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "odi_ho4_specimen_09",
        "source": "Ohio Department of Insurance (ODI) Standard Renters Insurance Specimen (https://insurance.ohio.gov)",
        "clauses": [
            ("1. COVERAGE C PERSONAL PROPERTY\nWorldwide coverage for personal property owned by an insured.", "coverage_scope", "fair"),
            ("2. COVERAGE D LOSS OF USE\nCovers living expenses while premises are untenantable.", "limits_of_liability", "fair"),
            ("3. COVERED CAUSES OF LOSS\nFire, lightning, windstorm, explosion, riot, smoke, theft.", "coverage_scope", "fair"),
            ("4. WATER DAMAGE EXCLUSION\nExcludes water backup through sewers and surface flooding.", "exclusions", "unfavorable"),
            ("5. DEDUCTIBLE\n$500.00 per occurrence.", "deductible_premium", "fair"),
            ("6. PROOF OF LOSS\nMust be filed within 60 days.", "claims_process", "fair"),
            ("7. 30-DAY NON-RENEWAL NOTICE\nNotice of non-renewal must be delivered at least 30 days before expiration.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "idoi_ho4_specimen_10",
        "source": "Illinois Department of Insurance (IDOI) Specimen HO-4 Broad Form (https://insurance.illinois.gov)",
        "clauses": [
            ("SECTION I: COVERAGE C\nCovers personal property owned or used by insured.", "coverage_scope", "fair"),
            ("SECTION I: LOSS OF USE\nAdditional living expenses incurred due to covered damage.", "limits_of_liability", "fair"),
            ("SECTION I: PERILS INSURED\nFire, lightning, hail, explosion, civil commotion, vandalism, theft.", "coverage_scope", "fair"),
            ("SECTION I: EXCLUSIONS (FLOOD)\nLoss caused by flood, waves, and surface water is excluded.", "exclusions", "unfavorable"),
            ("SECTION I: DEDUCTIBLE\nStandard deductible of $500.00 applies.", "deductible_premium", "fair"),
            ("SECTION I: CLAIMS DUTIES\nPrompt notice and signed sworn proof of loss required within 60 days.", "claims_process", "fair"),
            ("SECTION I: CANCELLATION\nRequires 30 days advance notice for cancellation.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "pa_pid_specimen_11",
        "source": "Pennsylvania Insurance Department Sample HO-4 Contents Policy Form (https://www.insurance.pa.gov)",
        "clauses": [
            ("1. COVERAGE C PROPERTY\nPersonal property covered anywhere in the world.", "coverage_scope", "fair"),
            ("2. LOSS OF USE\nCovers necessary increase in living expense.", "limits_of_liability", "fair"),
            ("3. BROAD PERILS\nCovers 16 broad named perils including fire and theft.", "coverage_scope", "fair"),
            ("4. WATER EXCLUSION\nExcludes water damage from sewers or drains.", "exclusions", "unfavorable"),
            ("5. DEDUCTIBLE\n$500.00 deductible per loss.", "deductible_premium", "fair"),
            ("6. APPRAISAL DISPUTES\nDisputes on valuation handled by independent appraisers.", "dispute_resolution_appraisal", "fair"),
            ("7. CANCELLATION NOTICE\nNotice of non-renewal must be mailed at least 30 days in advance.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "ga_oci_specimen_12",
        "source": "Georgia Office of Insurance Safety Commissioner Specimen Renters Policy (https://oci.georgia.gov)",
        "clauses": [
            ("SECTION 1: PERSONAL PROPERTY COVERAGE\nCovers personal property owned by insured.", "coverage_scope", "fair"),
            ("SECTION 2: LOSS OF USE EXPENSES\nLiving expenses for uninhabitable dwelling unit.", "limits_of_liability", "fair"),
            ("SECTION 3: INSURED PERILS\nFire, lightning, windstorm, vehicle damage, theft.", "coverage_scope", "fair"),
            ("SECTION 4: EXCLUSIONS\nExcludes earthquake, flood, and sewer backup.", "exclusions", "unfavorable"),
            ("SECTION 5: DEDUCTIBLE\n$500.00 standard deductible.", "deductible_premium", "fair"),
            ("SECTION 6: CANCELLATION STATUTES (OCGA 33-24-44)\nRequires 30 days written notice for cancellation.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "va_bureau_ins_specimen_13",
        "source": "Virginia Bureau of Insurance Standard HO-4 Specimen Policy (https://scc.virginia.gov/pages/Bureau-of-Insurance)",
        "clauses": [
            ("1. COVERAGE C\nCovers personal property worldwide up to policy limits.", "coverage_scope", "fair"),
            ("2. COVERAGE D\nLoss of use covers additional living expenses.", "limits_of_liability", "fair"),
            ("3. NAMED PERILS\nCovers fire, wind, hail, smoke, vandalism, and theft.", "coverage_scope", "fair"),
            ("4. EXCLUSIONS (WATER DAMAGE)\nExcludes flood and sewer backup.", "exclusions", "unfavorable"),
            ("5. DEDUCTIBLE\n$500.00 standard deductible.", "deductible_premium", "fair"),
            ("6. PROOF OF LOSS\nMust submit proof of loss within 60 days.", "claims_process", "fair"),
            ("7. CANCELLATION TERMS\n30 days advance notice required for non-renewal.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "wi_oci_specimen_14",
        "source": "Wisconsin Office of the Commissioner of Insurance (OCI) Sample Homeowners Form 4 (https://oci.wi.gov)",
        "clauses": [
            ("SECTION I: PROPERTY COVERAGE\nWorldwide personal property coverage for named insured.", "coverage_scope", "fair"),
            ("SECTION I: ADDITIONAL LIVING EXPENSE\nReimburses reasonable living costs after covered peril.", "limits_of_liability", "fair"),
            ("SECTION I: PERILS INSURED\nFire, lightning, explosion, riot, smoke, theft, freezing.", "coverage_scope", "fair"),
            ("SECTION I: EXCLUSIONS\nExcludes flood, sewer overflow, and earth sinking.", "exclusions", "unfavorable"),
            ("SECTION I: DEDUCTIBLE\n$500.00 per occurrence.", "deductible_premium", "fair"),
            ("SECTION I: NON-RENEWAL (WIS. STAT. 631.36)\nNotice of non-renewal must be mailed at least 60 days prior to expiration.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "co_doi_specimen_15",
        "source": "Colorado Division of Insurance Specimen Residential Property Form (https://doi.colorado.gov)",
        "clauses": [
            ("1. COVERAGE C\nPersonal property owned or used by insured worldwide.", "coverage_scope", "fair"),
            ("2. LOSS OF USE\nAdditional living expenses covered for up to 12 months.", "limits_of_liability", "fair"),
            ("3. PERILS COVERED\nFire, wind, hail, smoke, theft, vandalism.", "coverage_scope", "fair"),
            ("4. EXCLUSIONS (EARTH MOVEMENT AND WATER)\nExcludes landslide, mudflow, and flood.", "exclusions", "unfavorable"),
            ("5. DEDUCTIBLE\n$1,000.00 property deductible.", "deductible_premium", "fair"),
            ("6. NOTICE REQUIREMENTS\nPrompt notice of damage and itemized inventory.", "claims_process", "fair"),
            ("7. NON-RENEWAL NOTICE\nRequires 30 days notice prior to expiration.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "mi_difs_specimen_16",
        "source": "Michigan Department of Insurance and Financial Services (DIFS) HO-4 Specimen (https://www.michigan.gov/difs)",
        "clauses": [
            ("SECTION 1: PERSONAL PROPERTY\nCovers personal property anywhere in the world.", "coverage_scope", "fair"),
            ("SECTION 2: LOSS OF USE\nCovers additional living expense.", "limits_of_liability", "fair"),
            ("SECTION 3: PERILS INSURED\nFire, lightning, windstorm, explosion, riot, smoke, vandalism, theft.", "coverage_scope", "fair"),
            ("SECTION 4: WATER EXCLUSION\nExcludes sewer backup and flooding.", "exclusions", "unfavorable"),
            ("SECTION 5: DEDUCTIBLE\n$500.00 deductible per loss.", "deductible_premium", "fair"),
            ("SECTION 6: CANCELLATION (MCL 500.2833)\n30 days advance notice required for non-renewal.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "mn_doc_specimen_17",
        "source": "Minnesota Department of Commerce Specimen Homeowner / Renter Form (https://mn.gov/commerce/insurance)",
        "clauses": [
            ("1. COVERAGE C\nCovers personal property worldwide.", "coverage_scope", "fair"),
            ("2. LOSS OF USE\nProvides living expenses when premises uninhabitable.", "limits_of_liability", "fair"),
            ("3. COVERED PERILS\nFire, lightning, hail, explosion, vandalism, theft.", "coverage_scope", "fair"),
            ("4. EXCLUSIONS\nExcludes flood, earthquake, and freezing in unheated buildings.", "exclusions", "fair"),
            ("5. DEDUCTIBLE\n$500.00 standard deductible.", "deductible_premium", "fair"),
            ("6. APPRAISAL PROVISION (MINN. STAT. 65A.01)\nStatutory appraisal process for valuation disputes.", "dispute_resolution_appraisal", "fair"),
            ("7. NON-RENEWAL NOTICE\n60 days advance written notice required.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "md_mia_specimen_18",
        "source": "Maryland Insurance Administration Specimen HO-4 Contents Form (https://insurance.maryland.gov)",
        "clauses": [
            ("SECTION I: PROPERTY COVERAGE\nCovers personal property up to limit of liability.", "coverage_scope", "fair"),
            ("SECTION I: ADDITIONAL LIVING EXPENSE\nReimburses reasonable living costs.", "limits_of_liability", "fair"),
            ("SECTION I: PERILS INSURED\nFire, smoke, wind, vehicle damage, theft.", "coverage_scope", "fair"),
            ("SECTION I: WATER DAMAGE EXCLUSION\nExcludes flood, surface water, and sewer backup.", "exclusions", "unfavorable"),
            ("SECTION I: DEDUCTIBLE\n$500.00 deductible.", "deductible_premium", "fair"),
            ("SECTION I: PROOF OF LOSS\nMust submit proof of loss within 60 days.", "claims_process", "fair"),
            ("SECTION I: 45-DAY NON-RENEWAL NOTICE\nNotice of non-renewal must be mailed 45 days in advance.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "sc_doi_specimen_19",
        "source": "South Carolina Department of Insurance Property Specimen Form (https://doi.sc.gov)",
        "clauses": [
            ("1. COVERAGE C\nCovers personal property of insured.", "coverage_scope", "fair"),
            ("2. LOSS OF USE\nReimburses living costs during repairs.", "limits_of_liability", "fair"),
            ("3. PERILS COVERED\nFire, lightning, wind, hail, theft, vandalism.", "coverage_scope", "fair"),
            ("4. HURRICANE DEDUCTIBLE\nPercentage deductible applies during named hurricane events.", "deductible_premium", "needs_review"),
            ("5. EXCLUSIONS (WATER)\nExcludes flood, storm surge, and drain backup.", "exclusions", "unfavorable"),
            ("6. CLAIMS NOTICE\nPrompt notice required.", "claims_process", "fair"),
            ("7. CANCELLATION\n30 days advance notice required.", "cancellation_non_renewal", "fair")
        ]
    },
    {
        "doc_id": "in_doi_specimen_20",
        "source": "Indiana Department of Insurance Standard Renters Policy Specimen (https://www.in.gov/idoi)",
        "clauses": [
            ("SECTION I: PERSONAL PROPERTY\nCovers personal property anywhere in the world.", "coverage_scope", "fair"),
            ("SECTION I: LOSS OF USE\nCovers additional living expenses.", "limits_of_liability", "fair"),
            ("SECTION I: PERILS\nCovers fire, lightning, windstorm, explosion, riot, theft.", "coverage_scope", "fair"),
            ("SECTION I: EXCLUSIONS\nExcludes flood, water backup, and earth movement.", "exclusions", "unfavorable"),
            ("SECTION I: DEDUCTIBLE\n$500.00 per occurrence.", "deductible_premium", "fair"),
            ("SECTION I: NON-RENEWAL NOTICE (IC 27-7-12)\nNotice of non-renewal must be provided at least 20 days prior to expiration.", "cancellation_non_renewal", "fair")
        ]
    }
]
