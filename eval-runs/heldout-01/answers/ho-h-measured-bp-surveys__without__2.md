I'd use NHANES as the core US source, with HRS as a second US option. For comparison countries, I'd use ELSA (England) and CHARLS (China). I'm working from memory here, so confirm wave years and variable names against each survey's current documentation before you commit.

## Awareness definition (all surveys)
- **Hypertension:** mean measured BP at or above your threshold (140/90, or 130/80 under the 2017 ACC/AHA guideline), or currently taking antihypertensive medication.
- **Aware:** among those people, a "yes" to the doctor-told question.
- **Unaware:** the measured-hypertensive people who answer "no".
- **Medication:** keep it in the definition, so treated people with controlled BP count as hypertensive.

## US

**1. NHANES (CDC/NCHS), the best fit**
- **Design:** nationally representative, all ages. You can restrict to adults 40+ or 18+.
- **Blood pressure:** examiners take multiple readings in the Mobile Exam Center. Average readings 2–3 (or all valid ones), and check how each cycle handled the first reading.
- **Awareness question:** BPQ020, "Ever told by a doctor or health professional you had hypertension?" BPQ040A/BPQ050A cover medication.
- **Access:** free and public-use, with no application. Download the Demographics, Blood Pressure (BPX/BPXO), and Blood Pressure & Cholesterol questionnaire (BPQ) files from the NCHS NHANES site and merge on SEQN.
- **Pitfalls:**
  - Use the MEC exam weights, plus the strata and PSU design variables.
  - Pool cycles for precision, and divide weights appropriately.
  - The 2019–2020 cycle was cut short by COVID, so check how NCHS handles it (the pre-pandemic file and the August 2021–August 2023 cycle are separate).
  - Variable names and the BP device changed across cycles (auscultatory to oscillometric), so check the documentation.

**2. HRS (Health and Retirement Study), for adults 50+**
- **Blood pressure:** measured by interviewers during the physical measures. Since 2006 this has covered a rotating half-sample each wave, so you need to pool waves.
- **Awareness question:** the "has a doctor ever told you that you have high blood pressure" item.
- **Access:** free registration at hrs.isr.umich.edu, then download the public files. The RAND HRS longitudinal file is easier to work with than the raw files.
- **Pitfall:** use the biomarker or physical-measures weights, not the main-interview weights.

## International

**3. ELSA (English Longitudinal Study of Ageing), ages 50+**
- **Blood pressure:** a nurse visit measures BP, and it's offered in alternating waves.
- **Awareness question:** doctor-diagnosed hypertension, asked in the main interview.
- **Access:** register with the UK Data Service and accept the End User Licence. It's free for academic use and usually approved quickly. Use the nurse-visit weights.

**4. CHARLS (China Health and Retirement Longitudinal Study), ages 45+**
- **Blood pressure:** measured by trained interviewers with an Omron monitor, in the 2011, 2013, 2015 and 2018 waves (check which waves include the physical exam you need).
- **Awareness question:** "Have you been diagnosed with hypertension by a doctor?"
- **Access:** register at charls.pku.edu.cn, agree to the data-use terms, and download. It's free and usually quick.
- **Pitfall:** use the biomarker weights.

## Alternatives
- **LASI (India, 45+):** a good fit with measured BP and a diagnosis question, but access runs through an application to IIPS or the data distributor.
- **Other options:** MHAS (Mexico), TILDA (Ireland), Health Survey for England (all ages, nurse-measured), and KNHANES (Korea). Check each for BP measurement and the diagnosis question.
- **Not suitable:** SHARE doesn't measure BP, so skip it despite the name recognition.

## Cross-country comparability
The Gateway to Global Aging Data (g2aging.org) provides harmonized files for HRS, ELSA, CHARLS and others. It can save recoding time, but check whether the harmonized files include the measured BP variables, because some only carry the self-reported items. Also note that the surveys differ in BP device, number of readings, and age range, so say so in your limitations section.

If you tell me your age range and which hypertension threshold you're using, I can draft the variable list and merge steps for NHANES and HRS.