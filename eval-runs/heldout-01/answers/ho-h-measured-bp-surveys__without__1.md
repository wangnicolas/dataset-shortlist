I'd use NHANES as the main US source and HRS as a second US source for older adults. For comparison countries I'd use ELSA (England) and CHARLS (China), with LASI (India) as an optional third. I'm working from memory, so confirm wave and cycle details in each study's documentation before you finalize your design.

## US

**NHANES (CDC/NCHS)**
- **Blood pressure:** Trained examiners take several seated readings in the Mobile Examination Center. Most analysts average the readings after dropping the first.
- **Awareness item:** BPQ020, "Ever told by a doctor or health professional that you had hypertension?"
- **Coverage:** Nationally representative of non-institutionalized US adults of all ages, in two-year cycles from 1999 on.
- **Access:** The public-use files are free. Download them from the NCHS NHANES site with no application or registration. You need the Demographics, Blood Pressure (BPX/BPXO), Blood Pressure Questionnaire (BPQ) and Medication files, merged on SEQN.
- **Restricted data:** Geography and linked mortality or Medicare files go through the NCHS Research Data Center, which means a proposal and a fee. You probably don't need these.
- **Weights:** Use the MEC exam weights, not the interview weights. Divide by the number of cycles when you pool them.

**Health and Retirement Study (HRS, University of Michigan)**
- **Blood pressure:** Interviewers measure it in the physical-measures component. Since 2006 this has covered a rotating half-sample at each wave.
- **Awareness item:** "Has a doctor ever told you that you have high blood pressure or hypertension?" This is asked at every wave.
- **Coverage:** Adults aged 50 and over, with a longitudinal design.
- **Access:** Free registration at hrs.isr.umich.edu, then download. Some sensitive files, such as geographic identifiers, need a separate restricted-data application.
- **Weights:** Use the biomarker or physical-measures weights, not the main respondent weights.

## Other countries

| Survey | Population | BP measured by | Awareness item | Access |
|---|---|---|---|---|
| **ELSA** (England) | 50+ | Nurse visit, in selected waves only (check which) | Doctor-diagnosed hypertension | Free through the UK Data Service. Register, accept the End User Licence and apply for the nurse-visit dataset. Academic users can log in through their institution. |
| **CHARLS** (China) | 45+ | Interviewer, in 2011 and later waves | Doctor-diagnosed hypertension | Free. Register and apply at charls.pku.edu.cn. |
| **LASI** (India) | 45+ | Interviewer | Diagnosed hypertension | Apply through the IIPS/LASI data portal. Check the current terms. |

The Health Survey for England (all ages, nurse-measured) is an alternative to ELSA if you want younger adults too. Gateway to Global Aging offers harmonized versions of HRS, ELSA, CHARLS and LASI with comparable variable names. That saves a lot of recoding for a cross-country chapter.

## Design points

- **Definition:** Measured hypertension is usually mean SBP ≥140 or DBP ≥90, or currently taking antihypertensive medication. Awareness is the share of those people who report a diagnosis. Decide up front whether you use 140/90 or the 2017 ACC/AHA 130/80 threshold, and report both as a sensitivity check.
- **Protocol differences:** Devices, number of readings, rest periods and which readings get averaged differ across surveys. Document this, because it affects comparability.
- **Single-visit bias:** A single-occasion measurement can overstate prevalence, so awareness can look lower than it is.
- **Survey design:** Use survey weights and design variables (strata and PSU) in every analysis.

I can draft the exact variable lists and merge code for NHANES and HRS if that would help.