I'd use NHANES for the US, with ELSA (England) and CHARLS or LASI (China, India) as the comparison surveys. I confirmed the access routes for NHANES and ELSA today. I couldn't confirm the rest, so those access details come from memory and are marked below.

I also didn't build the interactive shortlist page. This answer is the full deliverable.

## What I assumed you need
- **R1 (must):** Blood pressure measured by a nurse or examiner, not self-reported.
- **R2 (must):** A question on whether a doctor ever told the respondent they have high blood pressure, in the same survey and person.
- **R3 (must):** Nationally representative samples of adults, US first.
- **R4 (nice):** Middle-aged and older samples abroad, with comparable designs.
- **R5 (nice):** Free or fast to get.

## Shortlist
| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | NHANES (US, all adults) | Direct download, no account | US government data, public use | Strong | Site confirmed today; variable details from memory |
| 2 | HRS (US, age 50+) | Free registration, then download | HRS terms of use | Strong | From memory (site returned 403 to my tool) |
| 3 | ELSA (England, age 50+) | Free UK Data Service account, then download | UKDS End User Licence | Strong | Access page read today |
| 4 | CHARLS (China, age 45+) | Registration and application on the CHARLS site | CHARLS terms | Strong | Site exists today; access terms from memory |
| 5 | LASI (India, age 45+) | Application or registration, via IIPS | LASI terms | Strong | From memory; the registry record exists, but I couldn't read the access terms |

## Details

**1. NHANES**
- **What it is:** The US National Health and Nutrition Examination Survey, with a home interview and a mobile exam centre. The exam takes several blood pressure readings from trained examiners.
- **Awareness variable:** The blood pressure questionnaire asks whether a doctor or health professional ever said you had hypertension. I recall the variable as `BPQ020` in the BPQ file, but I haven't confirmed it today.
- **Access:** Download the files from the NHANES site (https://wwwn.cdc.gov/nchs/nhanes/). The site lists a Data User Agreement and a "Limited Access Data" category, which is not what you need. There are no application steps, so you can start today.
- **Coverage:** Cycles from 1999 onward, with the latest listed as 2021–2023 (confirmed on the site). Use the exam sample weights, because the blood pressure readings come from the exam sample.
- **Precedent:** The search returned a record for "Awareness of having hypertension, diabetes and dyslipidaemia among US adults: The 2011–2018 NHANES data" (OpenAIRE). It is useful as a methods precedent.

**2. HRS (Health and Retirement Study)**
- **What it is:** A US panel of adults aged 50 and over. Interviewers measure blood pressure in the physical measures, and I recall this covering half the sample each wave since 2006. The interview asks whether a doctor has ever said you have high blood pressure.
- **Access:** From memory, register free at hrs.isr.umich.edu, accept the terms, and download. This should take days at most.
- **Caveat:** Blood pressure is only measured for part of the sample at each wave, so check the sample design before pooling waves.

**3. ELSA (English Longitudinal Study of Ageing)**
- **What it is:** Respondents aged 50+. From memory, nurse visits take measured blood pressure in alternating waves, and the main interview records doctor-diagnosed hypertension. Check which waves have nurse visits before you plan.
- **Access (confirmed):** The ELSA page says "Researchers can download ELSA data from waves 1-11 including wave 0 (HSE), from the UK Data Service." It also says "End User Licence level data are available to all via UKDS," and non-UK users can request a username. Special Licence and Secure Access data have more restrictions, but you shouldn't need them.
- **Record:** https://doi.org/10.5255/ukda-sn-5050-37 (waves 0–11, 1998–2024).
- **Why it fits:** It is designed to be comparable with HRS.

**4. CHARLS (China Health and Retirement Longitudinal Study)**
- **What it is:** Chinese residents aged 45 and over (confirmed on the site). From memory, interviewers measure blood pressure and the survey asks about a doctor's diagnosis.
- **Access:** From memory, sign up on the CHARLS site and apply for the data. Approval usually takes days to weeks.
- **Caveat:** The site currently shows the banner "This repository is under review for potential modification in compliance with Administration directives." Check that downloads still work before you build around it.
- **Related paper:** "Socioeconomic gradients of cardiovascular risk factors in China and India" uses CHARLS and LASI (https://doi.org/10.1007/s00038-017-0968-3).

**5. LASI (Longitudinal Ageing Study in India)**
- **What it is:** Adults aged 45 and over. From memory, trained field staff measure blood pressure and the survey asks about a doctor's diagnosis. The cohort profile is at https://doi.org/10.1093/ije/dyab266.
- **Access, uncertain:** The DataCite record "Longitudinal Aging Study Asia (LASI)" resolves to a Stanford/Redivis page, and I couldn't read the terms. The IIPS page I fetched had no access text. Treat the access route as unconfirmed and check with IIPS or the Gateway to Global Aging Data (g2aging.org).
- **Try first:** Check whether the LASI team's own data request process is still the route for researchers outside India.

## Known, not confirmed
- **Methods template:** "Unmet needs for hypertension care cascade in older adults and socioeconomic disparities: evidence from five national cohorts" (https://doi.org/10.1186/s12889-026-26341-4). The abstract says the cohorts include the US, UK and China, but it was truncated and I couldn't see the other two. It likely uses the same HRS, ELSA, CHARLS and LASI families.
- **Other candidates from memory:** The Health Survey for England (measured blood pressure, via UKDS) and the Korea National Health and Nutrition Examination Survey. I haven't checked either today.

## Not recommended, and why
- **Self-report-only surveys** such as the US National Health Interview Survey and BRFSS fail your measured blood pressure requirement.
- **Synthetic hypertension datasets** (for example the Hugging Face and Figshare ones from the search) are not real surveys.
- **NHANES paper supplements on Zenodo and Figshare** are derived or reproducibility files. Use the CDC original.

## What I could not find
- I did not confirm variable names or which waves have blood pressure for HRS, CHARLS and LASI. Check each codebook.
- I couldn't read the HRS or LASI access pages, so those steps come from memory.

## Next step
Start with NHANES today, since it needs no account. Register for ELSA at UKDS and for HRS in parallel. Request CHARLS or LASI at the same time, because those approvals take the longest. Choose one definition of awareness up front and apply it in every survey: measured systolic ≥140 or diastolic ≥90, or on blood pressure medication, then the share who report a doctor's diagnosis.

Checked 2026-11-11. Access rules change, so recheck before you commit.