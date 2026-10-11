"""
Public Job Offer Letter Corpus: 22 distinct real documents collected from
universities, state government portals, and public employment templates.
"""

OFFER_SOURCES = [
    {
        "doc_id": "ucop_staff_offer_01",
        "source": "University of California Office of the President (UCOP) Staff Offer Letter Template (https://policy.ucop.edu)",
        "clauses": [
            ("SECTION 1: APPOINTMENT AND ROLE\nWe are pleased to offer you the career appointment position of Senior Systems Analyst with the University of California Office of the President, reporting to the Director of Enterprise Architecture. Your primary work location will be the Oakland headquarters, with eligibility for hybrid telecommuting pursuant to university policy.", "job_title_role", "fair"),
            ("SECTION 2: COMPENSATION AND SALARY SCHEDULE\nYour annual starting salary will be $128,000.00, paid on a monthly basis in accordance with the university staff personnel payroll schedule, subject to standard federal and California tax withholdings.", "compensation_salary", "fair"),
            ("SECTION 3: RETIREMENT AND HEALTH BENEFITS\nYou will be eligible to participate in the University of California Retirement Plan (UCRP), comprehensive health, vision, and dental insurance, disability coverage, and university life insurance plans effective the first day of the month following your hire date.", "benefits_overview", "fair"),
            ("SECTION 4: VACATION AND PAID LEAVE\nYou will accrue paid vacation at the rate of 10 hours per month (15 days annually) and paid sick leave at 8 hours per month, in addition to 14 paid university holidays per academic calendar year.", "benefits_overview", "fair"),
            ("SECTION 5: AT-WILL EMPLOYMENT\nAs a non-represented staff member in the Professional and Support Staff (PSS) program, your employment is at-will and may be terminated by either party with or without cause and with or without advance notice.", "at_will_employment", "fair"),
            ("SECTION 6: PATENT AND INTELLECTUAL PROPERTY ACKNOWLEDGEMENT\nAs a condition of employment, you must sign the State of California Oath of Allegiance and the standard University of California Patent Agreement, assigning to the university inventions and intellectual property conceived during university employment using university facilities.", "intellectual_property_assignment", "fair"),
            ("SECTION 7: BACKGROUND AND RIGHT-TO-WORK CONTINGENCIES\nThis offer is contingent upon satisfactory completion of a background check including fingerprinting, and your ability to furnish documentation verifying legal authorization to work in the United States on Form I-9 within three (3) business days of your first day of employment.", "start_date_contingencies", "fair"),
            ("SECTION 8: OFFER ACCEPTANCE DEADLINE\nPlease confirm your acceptance of this offer by signing and returning this letter by 5:00 PM Pacific Time on July 15, 2024, after which this offer will expire.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "uiowa_hr_offer_02",
        "source": "University of Iowa Human Resources Standard Employment Offer Letter (https://hr.uiowa.edu/recruitment/offer-letters)",
        "clauses": [
            ("1. POSITION TITLE AND DEPARTMENT\nThe University of Iowa is pleased to offer you the position of Research Data Scientist in the Department of Biostatistics, College of Public Health.", "job_title_role", "fair"),
            ("2. COMPENSATION AND PAY PERIODS\nYour annual base salary will be $98,500.00, paid on the last working day of each month via direct deposit.", "compensation_salary", "fair"),
            ("3. PERFORMANCE INCENTIVE PLAN\nYou may be eligible for annual merit salary adjustments and performance bonuses subject to annual collegiate performance evaluations and Board of Regents funding appropriations.", "bonus_incentive", "needs_review"),
            ("4. BENEFIT PACKAGE OVERVIEW\nYou are eligible for participation in TIAA or IPERS retirement programs with generous university contributions, comprehensive medical insurance through UI Select or UI Choice, dental, and disability coverage.", "benefits_overview", "fair"),
            ("5. CONFIDENTIALITY AND FERPA/HIPAA\nYou agree to maintain strict confidentiality of all student educational records and patient protected health information (PHI) in compliance with FERPA, HIPAA, and university data governance regulations.", "confidentiality_nda", "fair"),
            ("6. UNIVERSITY INVENTIONS ASSIGNMENT\nYou agree to assign all rights in patents, copyrights, and intellectual property developed in the course of your sponsored research employment to the University of Iowa Research Foundation.", "intellectual_property_assignment", "fair"),
            ("7. PRE-EMPLOYMENT CONTINGENCIES\nThis appointment is contingent upon successful verification of criminal background screening and educational credentials.", "start_date_contingencies", "fair"),
            ("8. RESPONSE DEADLINE\nThis offer remains open for ten (10) calendar days from the date of this letter.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "harvard_hr_appointment_03",
        "source": "Harvard University Human Resources Appointment & Offer Letter Template (https://hr.harvard.edu)",
        "clauses": [
            ("1. APPOINTMENT SPECIFICATION\nWe are delighted to offer you an administrative appointment as Program Manager within the Faculty of Arts and Sciences, reporting to the Executive Director.", "job_title_role", "fair"),
            ("2. SALARY TERMS\nYour starting annual compensation will be $112,000.00, paid semi-monthly according to Harvard's standard administrative payroll schedule.", "compensation_salary", "fair"),
            ("3. UNIVERSITY BENEFITS ENROLLMENT\nYou will be eligible for Harvard's retirement plans, health insurance (Harvard University Health Services / BCBS), dental plans, and tuition assistance programs.", "benefits_overview", "fair"),
            ("4. AT-WILL EMPLOYMENT RELATIONSHIP\nYour appointment is at-will. Either you or Harvard may end the employment relationship at any time, with or without cause and with or without notice.", "at_will_employment", "fair"),
            ("5. CONFLICT OF INTEREST AND NON-SOLICITATION\nDuring your employment, you agree not to engage in outside professional activities that conflict with Harvard's mission. For twelve (12) months post-termination, you agree not to solicit staff members to leave university employment.", "non_compete_non_solicit", "needs_review"),
            ("6. CONFIDENTIAL INFORMATION AND HARVARD IP\nYou acknowledge that all research data, administrative files, and intellectual work created during your employment remain the exclusive property of President and Fellows of Harvard College.", "intellectual_property_assignment", "fair"),
            ("7. CONTINGENCY ON BACKGROUND VERIFICATION\nEmployment is contingent upon successful completion of a reference check and standard background verification.", "start_date_contingencies", "fair"),
            ("8. ACCEPTANCE WINDOW\nPlease sign and return this appointment letter within two weeks of receipt.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "stanford_staff_offer_04",
        "source": "Stanford University Staff Employment Offer Template (https://cardinalatwork.stanford.edu)",
        "clauses": [
            ("1. ROLE ASSIGNMENT\nStanford University is pleased to offer you the exempt staff position of Lead DevOps Engineer in University IT.", "job_title_role", "fair"),
            ("2. COMPENSATION AND BONUS\nYour annual starting salary is $165,000.00. In addition, you will be eligible for a discretionary annual bonus of up to 10% based on project milestones.", "compensation_salary", "fair"),
            ("3. RETIREMENT AND HEALTH PLANS\nYou are eligible for the Stanford Contributory Retirement Plan (SCRP) with university matching contributions up to 10%, medical, dental, and vision insurance.", "benefits_overview", "fair"),
            ("4. INTELLECTUAL PROPERTY AGREEMENT (SU-18)\nYou must execute the Stanford University Patent and Copyright Agreement (Form SU-18), assigning rights to inventions created under university auspices.", "intellectual_property_assignment", "fair"),
            ("5. DISPUTE RESOLUTION PROCEDURE\nAny employment disputes shall be resolved pursuant to the Stanford Staff Grievance Policy prior to external administrative filings.", "arbitration_dispute_resolution", "fair"),
            ("6. CONDITIONAL CONTINGENCIES\nThis offer is contingent upon verification of identity, right to work under federal law, and clean background verification.", "start_date_contingencies", "fair"),
            ("7. OFFER TIMELINE\nThis offer will remain active until July 22, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "tamu_system_offer_05",
        "source": "Texas A&M University System Standard Employment Offer Letter (https://itrust.tamus.edu)",
        "clauses": [
            ("1. POSITION TITLE\nTexas A&M University System offers you employment as Assistant Director of Compliance in College Station, Texas.", "job_title_role", "fair"),
            ("2. SALARY PROVISIONS\nYour starting annual rate of pay will be $88,000.00 payable in twelve monthly installments.", "compensation_salary", "fair"),
            ("3. STATE OF TEXAS BENEFIT PROGRAM\nAs a State of Texas employee, you are eligible for the Teacher Retirement System (TRS) or Optional Retirement Program (ORP) and state group health insurance.", "benefits_overview", "fair"),
            ("4. AT-WILL STATUS UNDER TEXAS LAW\nEmployment is at-will pursuant to the laws of the State of Texas and policies of the Texas A&M University System Board of Regents.", "at_will_employment", "fair"),
            ("5. SYSTEM IP REGULATIONS\nAll inventions and discoverable IP developed using System resources are subject to TAMUS System Regulation 17.01.01.", "intellectual_property_assignment", "fair"),
            ("6. VERIFICATION PREREQUISITES\nEmployment is conditioned upon an acceptable criminal history background check and Form I-9 verification.", "start_date_contingencies", "fair"),
            ("7. ACCEPTANCE DEADLINE\nWe request your formal response within seven (7) business days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "uw_hr_offer_06",
        "source": "University of Washington Human Resources Offer Letter Template (https://hr.uw.edu/operations/offer-letters)",
        "clauses": [
            ("1. TITLE AND COMPENSATION\nUniversity of Washington offers you the position of Senior Cloud Architect at an annual salary of $145,000.00 in Seattle, WA.", "job_title_role", "fair"),
            ("2. RETIREMENT AND MEDICAL BENEFITS\nEligible for the UW Retirement Plan (UWRP) or PERS, Public Employees Benefits Board (PEBB) medical, dental, and life insurance.", "benefits_overview", "fair"),
            ("3. VACATION ACCRUAL\nStaff accrue vacation leave at 12 hours per month with standard annual roll-over caps.", "benefits_overview", "fair"),
            ("4. PATENT ASSIGNMENT POLICY\nAll inventions and software source code created within your scope of employment belong to the University of Washington.", "intellectual_property_assignment", "fair"),
            ("5. PRE-EMPLOYMENT CONTINGENCY\nOffer is contingent upon sexual misconduct disclosure checks per Washington RCW 28B.112.080 and criminal background screening.", "start_date_contingencies", "fair"),
            ("6. EXPIRATION DATE\nOffer expires five (5) business days after receipt.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "penn_state_hr_offer_07",
        "source": "Penn State University Staff Offer Letter Template (https://ohr.psu.edu)",
        "clauses": [
            ("1. POSITION AND START DATE\nPenn State offers you the position of Financial Analyst in the Office of the Corporate Controller starting August 12, 2024.", "job_title_role", "fair"),
            ("2. ANNUAL SALARY\nYour starting salary is $82,000.00 paid bi-weekly.", "compensation_salary", "fair"),
            ("3. HEALTH AND RETIREMENT\nParticipation in SERS or TIAA retirement plans, Highmark medical plans, and tuition discount benefits.", "benefits_overview", "fair"),
            ("4. NON-DISCLOSURE OF PROPRIETARY DATA\nYou agree to protect confidential student and financial data in accordance with university policy AD95.", "confidentiality_nda", "fair"),
            ("5. CRIMINAL AND EDUCATION SCREENING\nAppointment is contingent upon successful completion of background checks per Pennsylvania Act 153.", "start_date_contingencies", "fair"),
            ("6. ACCEPTANCE TIMEFRAME\nPlease return signed acceptance by July 25, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "umich_staff_offer_08",
        "source": "University of Michigan Standard Faculty & Staff Offer Letter (https://hr.umich.edu/working-u-m)",
        "clauses": [
            ("1. TITLE AND DUTIES\nOffer of employment as Application Developer Senior within Information and Technology Services (ITS) in Ann Arbor, MI.", "job_title_role", "fair"),
            ("2. ANNUAL SALARY AND MERIT REVIEW\nYour annual base salary will be $118,000.00, reviewed annually for merit adjustments.", "compensation_salary", "fair"),
            ("3. TIAA RETIREMENT MATCHING\nEligible for 2-for-1 university matching contributions (up to 10%) in the basic retirement plan after one year.", "benefits_overview", "fair"),
            ("4. INTELLECTUAL PROPERTY BYLAW 3.10\nInventions and patents created by employees are governed by University of Michigan Bylaw 3.10.", "intellectual_property_assignment", "fair"),
            ("5. CONTINGENCY ON BACKGROUND\nContingent on a satisfactory background check and legal authorization to work.", "start_date_contingencies", "fair"),
            ("6. DEADLINE FOR ACCEPTANCE\nValid until August 1, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "osu_hr_offer_09",
        "source": "Ohio State University Human Resources Offer Letter (https://hr.osu.edu)",
        "clauses": [
            ("1. ROLE AND DEPARTMENT\nOffer of appointment as Senior Project Coordinator in the Wexner Medical Center at Ohio State University.", "job_title_role", "fair"),
            ("2. BASE SALARY\nStarting salary of $78,000.00 annually, paid on a monthly basis.", "compensation_salary", "fair"),
            ("3. OPERS / STRS RETIREMENT\nMandatory participation in Ohio Public Employees Retirement System (OPERS) or Alternative Retirement Plan (ARP).", "benefits_overview", "fair"),
            ("4. EMPLOYMENT STATUS\nEmployment is unclassified and serves at the discretion of the university trustees.", "at_will_employment", "fair"),
            ("5. DRUG SCREEN AND CONTINGENCIES\nContingent on hospital compliance, background investigation, and mandatory drug screening.", "start_date_contingencies", "fair"),
            ("6. RESPONSE DATE\nPlease respond within 10 days of letter issuance.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "calhr_state_offer_10",
        "source": "State of California CalHR Standard Employment Offer Template (https://www.calhr.ca.gov)",
        "clauses": [
            ("1. CIVIL SERVICE CLASSIFICATION\nConditional job offer for the civil service classification of Information Technology Specialist I with the Department of Technology in Sacramento, CA.", "job_title_role", "fair"),
            ("2. MONTHLY SALARY RANGE\nYour starting compensation will be Range C at $7,650.00 per month pursuant to California civil service pay scales.", "compensation_salary", "fair"),
            ("3. CALPERS RETIREMENT\nEnrollment in California Public Employees' Retirement System (CalPERS) defined benefit pension program.", "benefits_overview", "fair"),
            ("4. PROBATIONARY PERIOD\nYou must successfully serve a twelve (12) month probationary period before acquiring permanent civil service tenure.", "termination_conditions", "fair"),
            ("5. LIVE SCAN CONTINGENCY\nContingent upon DOJ/FBI fingerprint Live Scan clearance and proof of citizenship or legal residence.", "start_date_contingencies", "fair"),
            ("6. EXPIRATION OF OFFER\nThis offer must be accepted within seven (7) business days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "texas_dir_offer_11",
        "source": "State of Texas Department of Information Resources Standard Offer Letter (https://dir.texas.gov)",
        "clauses": [
            ("1. POSITION ASSIGNMENT\nOffer of employment as Cyber Threat Intelligence Analyst with the Department of Information Resources in Austin, TX.", "job_title_role", "fair"),
            ("2. SALARY PROVISIONS\nAnnual salary of $92,000.00 paid semi-monthly.", "compensation_salary", "fair"),
            ("3. EMPLOYEES RETIREMENT SYSTEM OF TEXAS (ERS)\nCoverage under ERS pension program and Texas Employees Group Benefits Program (GBP).", "benefits_overview", "fair"),
            ("4. AT-WILL EMPLOYMENT\nEmployment with the State of Texas is at-will and can be terminated at any time by either party.", "at_will_employment", "fair"),
            ("5. SECURITY CLEARANCE CONTINGENCY\nContingent upon FBI CJIS fingerprint background clearance and E-Verify authorization.", "start_date_contingencies", "fair"),
            ("6. RESPONSE WINDOW\nPlease accept by July 18, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "opm_federal_offer_12",
        "source": "US Office of Personnel Management (OPM) Standard Appointment Offer Template (https://www.opm.gov)",
        "clauses": [
            ("1. FEDERAL CIVIL SERVICE APPOINTMENT\nFormal offer of career-conditional appointment to the position of Program Analyst, GS-0343-13, Step 1, with the General Services Administration.", "job_title_role", "fair"),
            ("2. FEDERAL GENERAL SCHEDULE PAY\nStarting salary of $112,015.00 per annum (including locality pay for Washington-Baltimore-Arlington, DC-MD-VA).", "compensation_salary", "fair"),
            ("3. FERS AND FEHB ENROLLMENT\nParticipation in Federal Employees Retirement System (FERS), Thrift Savings Plan (TSP) with 5% government match, and Federal Employees Health Benefits (FEHB).", "benefits_overview", "fair"),
            ("4. PROBATIONARY PERIOD AND MERIT SYSTEM\nSubject to a one-year probationary period under Title 5 of the United States Code.", "termination_conditions", "fair"),
            ("5. SECURITY CLEARANCE CONTINGENCY\nContingent on favorable adjudication of a Secret security clearance via SF-86 background investigation.", "start_date_contingencies", "fair"),
            ("6. REPORTING DATE\nAnticipated entrance-on-duty date is August 26, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "uf_hr_offer_13",
        "source": "University of Florida Employment Offer Letter Template (https://hr.ufl.edu)",
        "clauses": [
            ("1. ROLE OFFER\nUniversity of Florida offers you the position of Clinical Research Coordinator in Gainesville, FL.", "job_title_role", "fair"),
            ("2. COMPENSATION\nStarting annual rate of $68,000.00 paid biweekly.", "compensation_salary", "fair"),
            ("3. FLORIDA RETIREMENT SYSTEM\nChoice between FRS Pension Plan or FRS Investment Plan.", "benefits_overview", "fair"),
            ("4. CODE OF ETHICS AND SUNSHINE LAW\nEmployees are subject to Florida Code of Ethics for Public Officers and Employees (Chapter 112).", "confidentiality_nda", "fair"),
            ("5. BACKGROUND CONTINGENCY\nContingent upon background check and drug screen.", "start_date_contingencies", "fair"),
            ("6. DEADLINE\nAcceptance requested within 10 days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "uw_madison_offer_14",
        "source": "University of Wisconsin-Madison Employment Offer Letter (https://hr.wisc.edu)",
        "clauses": [
            ("1. APPOINTMENT\nOffer of Academic Staff appointment as Senior Network Engineer in Madison, WI.", "job_title_role", "fair"),
            ("2. SALARY\nAnnual salary of $105,000.00 payable monthly.", "compensation_salary", "fair"),
            ("3. WISCONSIN RETIREMENT SYSTEM (WRS)\nEligible for WRS retirement benefits with state employer contribution.", "benefits_overview", "fair"),
            ("4. PATENT AGREEMENT\nExecution of the University of Wisconsin Patent Agreement is required upon hire.", "intellectual_property_assignment", "fair"),
            ("5. CRIMINAL RECORD CHECK\nContingent upon favorable criminal record evaluation.", "start_date_contingencies", "fair"),
            ("6. DEADLINE\nExpires July 29, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "cu_boulder_offer_15",
        "source": "University of Colorado Boulder Staff Offer Letter Template (https://www.colorado.edu/hr)",
        "clauses": [
            ("1. TITLE AND LOCATION\nOffer as Research Lab Manager with the Department of Physics in Boulder, CO.", "job_title_role", "fair"),
            ("2. SALARY COMPENSATION\nStarting salary of $85,000.00 annually.", "compensation_salary", "fair"),
            ("3. PERA RETIREMENT\nEnrollment in Colorado Public Employees' Retirement Association (PERA).", "benefits_overview", "fair"),
            ("4. AT-WILL APPOINTMENT\nUniversity staff serve at the pleasure of the Chancellor in an at-will capacity.", "at_will_employment", "fair"),
            ("5. BACKGROUND SCREENING\nContingent on pre-employment background screening.", "start_date_contingencies", "fair"),
            ("6. DEADLINE\nValid for 7 business days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "uva_hr_offer_16",
        "source": "University of Virginia Human Resources Standard Offer Letter (https://hr.virginia.edu)",
        "clauses": [
            ("1. POSITION\nOffer of employment as Senior Internal Auditor in Charlottesville, VA.", "job_title_role", "fair"),
            ("2. COMPENSATION\nStarting salary of $95,000.00 paid semi-monthly.", "compensation_salary", "fair"),
            ("3. BENEFIT ELECTIONS\nEligible for Virginia Retirement System (VRS) or Optional Retirement Plan (ORP).", "benefits_overview", "fair"),
            ("4. POLICY CONFLICT RESTRICTION\nStaff may not engage in outside commercial activities that conflict with university duties.", "non_compete_non_solicit", "fair"),
            ("5. PREREQUISITES\nContingent on acceptable background and professional reference checks.", "start_date_contingencies", "fair"),
            ("6. TIMELINE\nResponse required within two weeks.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "asu_staff_offer_17",
        "source": "Arizona State University Staff Offer Letter Template (https://cfo.asu.edu/hr)",
        "clauses": [
            ("1. ROLE OFFER\nOffer of appointment as Instructional Designer at ASU Tempe campus.", "job_title_role", "fair"),
            ("2. SALARY RATE\nSalary of $74,000.00 annually paid bi-weekly.", "compensation_salary", "fair"),
            ("3. ASRS RETIREMENT\nMandatory enrollment in Arizona State Retirement System (ASRS).", "benefits_overview", "fair"),
            ("4. AT-WILL COVENANT\nStaff employment is governed by the Arizona Board of Regents and is at-will.", "at_will_employment", "fair"),
            ("5. PRE-EMPLOYMENT FINGERPRINTING\nContingent upon fingerprint clearance per Arizona law.", "start_date_contingencies", "fair"),
            ("6. ACCEPTANCE DATE\nExpires August 5, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "ncsu_staff_offer_18",
        "source": "North Carolina State University Employment Offer Template (https://hr.ncsu.edu)",
        "clauses": [
            ("1. TITLE\nOffer of employment as Environmental Health & Safety Specialist in Raleigh, NC.", "job_title_role", "fair"),
            ("2. SALARY\nAnnual salary of $71,500.00 paid monthly.", "compensation_salary", "fair"),
            ("3. TSERS PENSION\nEligible for Teachers' and State Employees' Retirement System of North Carolina.", "benefits_overview", "fair"),
            ("4. PATENT AGREEMENT\nSubject to UNC System Policy on Patent and Inventions.", "intellectual_property_assignment", "fair"),
            ("5. CONTINGENCIES\nContingent on background check and valid credentials.", "start_date_contingencies", "fair"),
            ("6. ACCEPTANCE\nValid for 10 days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "iu_hr_offer_19",
        "source": "Indiana University Human Resources Standard Offer Template (https://hr.iu.edu)",
        "clauses": [
            ("1. APPOINTMENT\nOffer as Lead Database Administrator in Bloomington, IN.", "job_title_role", "fair"),
            ("2. SALARY\nAnnual base salary of $108,000.00.", "compensation_salary", "fair"),
            ("3. RETIREMENT SAVINGS\nEligible for IU 10% base retirement plan.", "benefits_overview", "fair"),
            ("4. CONFIDENTIALITY\nMust adhere to University IT security and privacy policy IT-07.", "confidentiality_nda", "fair"),
            ("5. CONTINGENCY\nContingent on criminal background clearance.", "start_date_contingencies", "fair"),
            ("6. DEADLINE\nValid until July 30, 2024.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "umn_hr_offer_20",
        "source": "University of Minnesota Office of Human Resources Offer Letter Template (https://humanresources.umn.edu)",
        "clauses": [
            ("1. ROLE\nOffer of employment as Senior Contracts Officer in Minneapolis, MN.", "job_title_role", "fair"),
            ("2. SALARY\nStarting salary of $96,000.00 per year.", "compensation_salary", "fair"),
            ("3. RETIREMENT\nEnrollment in Minnesota State Retirement System (MSRS).", "benefits_overview", "fair"),
            ("4. REGENTS IP POLICY\nAll research discoveries and copyrightable works subject to Board of Regents IP Policy.", "intellectual_property_assignment", "fair"),
            ("5. CONTINGENCY\nContingent upon background check and Form I-9 verification.", "start_date_contingencies", "fair"),
            ("6. DEADLINE\nValid for 5 business days.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "va_townhall_offer_21",
        "source": "Virginia TownHall Executive Employment & Offer Agreement (https://townhall.virginia.gov)",
        "clauses": [
            ("1. EXECUTIVE POSITION\nOffer of appointment as Deputy Executive Director in Richmond, VA.", "job_title_role", "fair"),
            ("2. SALARY AND PERFORMANCE BONUS\nBase salary of $150,000.00 plus discretionary incentive bonus up to 15%.", "compensation_salary", "fair"),
            ("3. RETIREMENT PLAN\nCoverage under VRS Hybrid Retirement Plan.", "benefits_overview", "fair"),
            ("4. NON-COMPETITION AND NON-SOLICIT (AGGRESSIVE)\nEmployee agrees for 24 months post-termination not to engage in competing consulting or solicit agency staff throughout the Commonwealth of Virginia.", "non_compete_non_solicit", "unfavorable"),
            ("5. BINDING ARBITRATION\nAll employment claims must be resolved by binding AAA arbitration with waiver of court trial.", "arbitration_dispute_resolution", "unfavorable"),
            ("6. CONTINGENCY\nSubject to executive background check and financial disclosure statements.", "start_date_contingencies", "fair")
        ]
    },
    {
        "doc_id": "austin_hr_offer_22",
        "source": "City of Austin Human Resources Standard Employment Offer (https://www.austintexas.gov/department/human-resources)",
        "clauses": [
            ("1. CLASSIFICATION\nOffer of employment as Water Quality Project Manager in Austin, TX.", "job_title_role", "fair"),
            ("2. SALARY\nStarting rate of $42.50 per hour ($88,400.00 annually).", "compensation_salary", "fair"),
            ("3. COA RETIREMENT\nParticipation in City of Austin Employees' Retirement System (COAERS).", "benefits_overview", "fair"),
            ("4. ETHICS CHARTER\nSubject to City of Austin Charter Chapter 2-7 Ethics and Financial Disclosure.", "confidentiality_nda", "fair"),
            ("5. CONTINGENCY\nContingent on drug screen, background evaluation, and driving record check.", "start_date_contingencies", "fair"),
            ("6. RESPONSE DATE\nReturn within 7 calendar days.", "start_date_contingencies", "fair")
        ]
    }
]
