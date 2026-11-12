# Recommended surveys

I haven't checked the live access pages, so confirm wave numbers and procedures on each site before you plan around them.

## 1. US: NHANES (core dataset)
- **Why:** It is the standard source for US hypertension awareness. Trained examiners take several BP readings in the Mobile Examination Center. The questionnaire asks whether a doctor or other health professional ever told the participant they had hypertension (the BPQ file).
- **Coverage:** The sample is nationally representative of all US adults. Continuous NHANES runs from 1999 in 2-year cycles, with a pre-pandemic 2017–March 2020 file and a later 2021–2023 cycle.
- **Caveat:** The BP measurement method changed in recent cycles, from mercury sphygmomanometer to an oscillometric device. Check the documentation before pooling across years.
- **Access:** It's free and needs no application or registration. Download the XPT files from the CDC/NCHS NHANES website. You need the demographics, blood pressure, BP questionnaire and medication files, merged on `SEQN`. Use the MEC exam weights. Linked mortality files and exact geography are restricted and go through the NCHS Research Data Center, which needs a proposal. You won't need those for awareness.

## 2. US, older adults: Health and Retirement Study (HRS)
- **Why:** It covers adults 50 and over. Interviewers take BP in the physical-measures component, and respondents also report whether a doctor ever told them they had high blood pressure. It is longitudinal, so you can study awareness over time.
- **Caveat:** Physical measures cover only a rotating half-sample each wave, from 2006 onward.
- **Access:** It's free. Register on the HRS website (Institute for Social Research, University of Michigan), accept the terms of use, and download the public files. The RAND HRS longitudinal file is a convenient starting point. Sensitive and geographic data need a separate restricted-data application.

## 3. England: English Longitudinal Study of Ageing (ELSA)
- **Why:** It follows adults 50 and over. A nurse visit in alternating waves measures BP, and the main interview asks about doctor-diagnosed hypertension. It is designed to be comparable with HRS.
- **Caveat:** Nurse visits happen only in some waves, so use the nurse-visit datasets and merge them with the main-wave files.
- **Access:** Register with the UK Data Service, accept the End User Licence, and download. This is free for academic users, and you usually get access immediately with institutional login or registration. The Health Survey for England, also on the UK Data Service, is an option if you want all adults rather than just 50 and over.

## 4. China: CHARLS
- **Why:** It is nationally representative of Chinese adults 45 and over. Interviewers measure BP, and respondents are asked whether they have been diagnosed with hypertension. It is a useful contrast with the two high-income settings.
- **Access:** Register on the CHARLS website (Peking University's National School of Development) and agree to the data-use terms. Approval is usually quick for students, and the download is free. Harmonized versions are also available.

## Optional fifth: LASI (India)
It has measured BP and a diagnosis question for adults 45 and over. Access runs through the survey's host institute (IIPS) and its data-request process, which is slower and less certain than the others. Check its current data-access page before committing.

## Harmonization shortcut
The **Gateway to Global Aging Data** (USC) provides harmonized variables across HRS, ELSA, CHARLS, LASI, SHARE and others. It is free with registration. It can save you a lot of recoding, but check which BP variables it includes for each study.

## Analysis points that matter for the thesis
- **Hypertension:** Define it the same way in every survey. The usual definition is mean SBP ≥140 or DBP ≥90 mmHg, or current use of antihypertensive medication. The stricter 130/80 threshold is also common, so state your choice.
- **Awareness:** Among measured hypertensives, awareness is a "yes" to the doctor-told question. Many studies also count those on treatment as aware. Decide this and report it.
- **Readings:** Specify how you average readings. NHANES discards the first reading in some conventions, and the other surveys take fewer readings.
- **Weights and design:** Use the survey weights, strata and PSUs. Nonresponse to the BP exam is non-trivial, so use the exam weights and not the interview weights.
- **Comparability:** Differences in device, number of readings, age range and wording of the diagnosis question will affect cross-country comparisons. Restrict to ages 50 and over for a like-for-like comparison.

If you tell me your preferred hypertension definition and years, I can sketch the variable lists and merge code for each file.