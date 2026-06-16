CASES = [
    {
        "id": 1,
        "patient": {
            "name": "Erik Johansson",
            "age": 67,
            "sex": "Male",
            "presenting_complaint": "Persistent cough and 8 kg weight loss over 3 months",
        },
        "history": (
            "Mr. Johansson is a 67-year-old retired carpenter with a 40 pack-year smoking history "
            "(quit 5 years ago). He presents with a 3-month history of worsening dry cough, "
            "progressive dyspnoea on exertion, and unintentional weight loss of 8 kg. He also "
            "reports right-sided chest pain and occasional haemoptysis. No fever or night sweats. "
            "PMH: COPD, hypertension. Medications: salbutamol inhaler, amlodipine 5 mg."
        ),
        "investigations": [
            "CXR: 3.5 cm right upper lobe mass with hilar enlargement",
            "CT chest/abdomen/pelvis: Right upper lobe mass 3.5 x 3.2 cm, ipsilateral mediastinal lymphadenopathy, no distant metastases",
            "PET-CT: FDG-avid right upper lobe mass and right mediastinal nodes (N2 disease)",
            "Bronchoscopy + biopsy: Non-small cell lung cancer, adenocarcinoma",
            "Molecular testing: EGFR exon 19 deletion positive, ALK negative",
            "Brain MRI: No intracranial metastases",
            "PFTs: FEV1 68% predicted",
            "ECOG performance status: 1",
        ],
        "stage": "Stage IIIA (T2aN2M0)",
        "questions": [
            {
                "text": "Based on the staging and molecular profile, what is the most appropriate first-line treatment?",
                "options": [
                    "Concurrent chemoradiotherapy (carboplatin/paclitaxel + RT) followed by durvalumab consolidation",
                    "EGFR-TKI (osimertinib) monotherapy",
                    "Surgical resection (right upper lobectomy) alone",
                    "Palliative chemotherapy (carboplatin/pemetrexed)",
                ],
                "correct": 0,
                "explanation": (
                    "This is Stage IIIA unresectable NSCLC with N2 disease. Despite the EGFR mutation, "
                    "current evidence (PACIFIC trial) supports concurrent chemoradiotherapy followed by "
                    "durvalumab consolidation as standard of care. EGFR-TKIs are first-line for Stage IV "
                    "EGFR-mutant disease but their role in Stage III is not yet established as standard. "
                    "Surgical resection is generally not recommended for N2 disease. Palliative "
                    "chemotherapy is reserved for Stage IV."
                ),
            },
            {
                "text": "The patient asks about his prognosis. Which statement best reflects current evidence?",
                "options": [
                    "Stage IIIA NSCLC has a 5-year survival of approximately 10-15% with chemoRT alone",
                    "Stage IIIA NSCLC is curable in the majority of patients with chemoRT + durvalumab",
                    "With chemoRT + durvalumab, 5-year progression-free survival is approximately 33%",
                    "EGFR mutation status has no prognostic relevance in Stage IIIA disease",
                ],
                "correct": 2,
                "explanation": (
                    "The PACIFIC trial demonstrated that durvalumab consolidation after chemoRT improved "
                    "5-year PFS to approximately 33% and 5-year OS to 43%. While this is a significant "
                    "improvement over historical data, Stage IIIA NSCLC is not curable in the majority. "
                    "The 10-15% figure reflects older data without immunotherapy. The prognostic role of "
                    "EGFR mutation in Stage III remains under active investigation."
                ),
            },
            {
                "text": "Before initiating treatment, which step is most important?",
                "options": [
                    "Repeat CT scan in 6 weeks to confirm disease stability",
                    "Multidisciplinary team (MDT) discussion",
                    "Bone scan to exclude occult bone metastases",
                    "Endoscopic ultrasound (EUS) for mediastinal restaging",
                ],
                "correct": 1,
                "explanation": (
                    "MDT discussion is mandatory before treatment initiation for all lung cancer cases. "
                    "It ensures coordinated input from thoracic surgery, radiation oncology, medical "
                    "oncology, radiology, and pathology. EUS/EBUS would have been appropriate earlier "
                    "if PET findings were ambiguous, but diagnosis and stage are already confirmed. "
                    "A bone scan is largely superseded by PET-CT. Delaying treatment for repeat CT "
                    "is not clinically indicated here."
                ),
            },
        ],
    },
    {
        "id": 2,
        "patient": {
            "name": "Margaret Chen",
            "age": 52,
            "sex": "Female",
            "presenting_complaint": "Bone pain and shortness of breath for 3 months",
        },
        "history": (
            "Ms. Chen is a 52-year-old postmenopausal retired teacher with a history of stage II "
            "HER2-positive, hormone receptor-positive invasive ductal carcinoma diagnosed 4 years ago. "
            "She completed adjuvant chemotherapy (AC-T), locoregional radiotherapy, and 1 year of "
            "trastuzumab. She has been on letrozole 2.5 mg for 3 years as maintenance endocrine therapy. "
            "She now presents with 3 months of progressive lower back pain, dyspnoea on exertion, "
            "fatigue, and 8 lb weight loss despite NSAIDs. Non-smoker, occasional alcohol use. "
            "PMH: Hypertension, type 2 diabetes. Medications: lisinopril 10 mg, metformin 1000 mg BD, "
            "atorvastatin 20 mg, letrozole 2.5 mg. Allergies: none known."
        ),
        "investigations": [
            "CT chest/abdomen/pelvis: Multiple pulmonary nodules (largest 1.2 cm), 2–3 hepatic lesions (0.8–1.5 cm)",
            "Bone scan: Increased uptake at L4–L5, right femoral head, and sternum — consistent with metastases",
            "MRI lumbar spine: L4–L5 metastatic lesion with mild cord compression, no myelopathy",
            "Labs: Hb 11.8 g/dL, ALP 145 (elevated), CEA 8.5 ng/mL (elevated), CA 15-3 68 U/mL (elevated)",
            "Pathology (primary tumour): ER 80%, PR 65%, HER2 3+ by IHC",
            "ECOG performance status: 1",
        ],
        "stage": "Stage IV (metastatic) HER2-positive, HR-positive breast cancer",
        "questions": [
            {
                "text": "What is the most appropriate first-line systemic treatment for this patient?",
                "options": [
                    "Trastuzumab + pertuzumab + docetaxel",
                    "Continue letrozole monotherapy",
                    "Fulvestrant + palbociclib",
                    "Paclitaxel monotherapy",
                ],
                "correct": 0,
                "explanation": (
                    "For HER2-positive metastatic breast cancer, dual HER2 blockade (trastuzumab + pertuzumab) "
                    "combined with a taxane is the gold standard first-line regimen (CLEOPATRA trial). "
                    "Continuing letrozole is inappropriate — she has progressed on it, indicating endocrine resistance. "
                    "Fulvestrant + palbociclib targets HR+ HER2-negative disease. Paclitaxel alone omits essential "
                    "HER2-directed therapy."
                ),
            },
            {
                "text": "Before starting trastuzumab + pertuzumab, which baseline assessment is mandatory?",
                "options": [
                    "DEXA scan for osteoporosis",
                    "Echocardiogram (LVEF assessment)",
                    "Hepatic biopsy to confirm metastases",
                    "Bone marrow biopsy",
                ],
                "correct": 1,
                "explanation": (
                    "Both trastuzumab and pertuzumab carry a risk of cardiotoxicity and reduced LVEF. "
                    "A baseline echocardiogram (or MUGA scan) is mandatory before starting HER2-directed therapy, "
                    "with repeat monitoring throughout treatment. DEXA is not urgent. Hepatic biopsy is not "
                    "indicated — CT and clinical context are sufficient to confirm metastatic recurrence. "
                    "Bone marrow biopsy has no role here."
                ),
            },
            {
                "text": "Given her hormone receptor positivity, what role does endocrine therapy play going forward?",
                "options": [
                    "Discontinue all endocrine therapy; HER2-directed treatment replaces it",
                    "Continue letrozole unchanged alongside chemotherapy",
                    "Switch to fulvestrant and continue alongside HER2-directed therapy",
                    "Add a CDK4/6 inhibitor to letrozole without starting chemotherapy",
                ],
                "correct": 2,
                "explanation": (
                    "In HR+ HER2+ metastatic breast cancer, endocrine therapy is maintained alongside "
                    "HER2-directed treatment for additive benefit. However, because Ms. Chen has progressed "
                    "on letrozole, switching to fulvestrant (an ER antagonist without cross-resistance to AIs) "
                    "is preferred over continuing the same agent. CDK4/6 inhibitors are standard in HR+ HER2-negative "
                    "disease but are not routinely combined with HER2-directed chemotherapy. Dropping endocrine "
                    "therapy altogether forfeits its additive benefit in a dual-positive tumour."
                ),
            },
        ],
    },
]