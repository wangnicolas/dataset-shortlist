**Use NHANES as your US source, and add KNHANES (South Korea) and the Health Survey for England as comparators.** All three measure blood pressure in a standardized exam and ask the "ever told by a doctor" question. This is from memory, not checked against the current sites, so confirm variable names and the latest release in each codebook.

| Survey | Population | BP measurement | Diagnosis question | Access |
|---|---|---|---|---|
| **NHANES** (US, CDC/NCHS) | All ages, 2-year cycles | Exam in a mobile centre, three readings; mercury auscultatory through 2017–18, oscillometric from 2017–2020 | `BPQ020`: ever told by a doctor or health professional you had high blood pressure | Direct download from the CDC NHANES site, no registration |
| **KNHANES** (South Korea, KDCA) | All ages, annual | Health exam by trained staff, three readings | Physician-diagnosed hypertension item, plus treatment items | Free download after registering on the KNHANES site; English documentation available |
| **Health Survey for England** | Adults in private households, annual | Nurse visit, three oscillometric readings | Doctor-diagnosed high blood pressure item | UK Data Service: register, add to a project, accept the End User Licence; free |

If you want an ageing-cohort comparison instead, these three are designed as sister studies:

- **HRS (US, age 51+)**: blood pressure is measured by interviewers since 2006, on a rotating half of the sample each wave. Access is by free registration on the HRS site.
- **ELSA (England, 50+)**: blood pressure is measured in the nurse-visit waves only (2, 4, 6, and 8/9). Access is through the UK Data Service, as for HSE.
- **CHARLS (China, 45+)**: blood pressure was measured in 2011, 2013 and 2015. Access is by free registration and a short application on the CHARLS site.

The Gateway to Global Aging Data offers harmonized versions of all three, which saves recoding. SHARE (Europe) will not work, because its hypertension data are self-reported.

**NHANES details**
- **Files:** for each cycle, merge the demographics (`DEMO`), blood pressure questionnaire (`BPQ`) and exam files (`BPX`, or `BPXO` for oscillometric) on `SEQN`.
- **Weights:** use the exam weights (`WTMEC2YR`), not the interview weights, with `SDMVSTRA` and `SDMVPSU` for the design.
- **Cycles:** the 2019–March 2020 data were combined with 2017–18 into a "pre-pandemic" file with its own weight. The newest cycle is August 2021–August 2023.
- **Protocol change:** the switch from mercury to oscillometric devices affects trend comparisons. NCHS published a bridging study using 2017–18, when both methods were run.

**Things to settle in your methods**
- **Definition:** the usual one is mean measured blood pressure ≥140/90 (or ≥130/80) or current antihypertensive medication, with "unaware" meaning a "no" to the ever-told question. Use the same threshold and the same number of readings averaged across surveys.
- **Single-visit bias:** all of these surveys measure on one occasion, which overstates true hypertension and so overstates unawareness. This is a standard limitation to state.
- **Mode differences:** HSE nurse visits happen at home, while NHANES and KNHANES use exam centres. Nurse-visit subsamples also have their own weights.
- **Pandemic gaps:** HSE 2020 was cancelled and 2021 had reduced nurse coverage, so 2019 is the cleanest recent HSE year.