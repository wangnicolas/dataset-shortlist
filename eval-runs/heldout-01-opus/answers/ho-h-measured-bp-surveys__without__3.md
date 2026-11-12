For this, NHANES should be your main dataset. Add HRS if you want an older-US sample. For other countries, the best matches are the HRS "sister studies": ELSA (England), CHARLS (China) and LASI (India). All of them measure blood pressure and ask whether a doctor ever told the person they have high blood pressure, and harmonized versions exist. I wrote this from what I already know and didn't check the websites live, so confirm current releases and access rules before you cite them.

## United States

### 1. NHANES (National Health and Nutrition Examination Survey): main dataset
- **Why:** It's the standard source for US hypertension awareness. It covers the civilian non-institutionalized population of all ages. Blood pressure is measured by trained examiners in Mobile Examination Centers.
- **Key variables:**
  - `BPQ020` asks: "Ever told by a doctor or other health professional that you had high blood pressure?"
  - `BPQ050A` asks whether the person is currently taking blood pressure medication. You need this to separate "treated" from "aware."
  - The exam files are `BPX` (older cycles) and `BPXO` (oscillometric, 2017 onward).
- **Watch out:** The method changed. Older cycles used auscultation with a mercury device. 2017–March 2020 had both methods, and later cycles (e.g., August 2021–August 2023) are oscillometric only. If you pool across this change or look at trends, say so and consider calibration. Use the exam weights (`WTMEC2YR`, or the pre-pandemic combined weights) and the design variables `SDMVSTRA`/`SDMVPSU`.
- **Access:** Free download from the CDC/NCHS NHANES website in SAS XPT format, with no registration. Restricted variables, such as detailed geography, require an application to the NCHS Research Data Center. The R package `nhanesA` or Python `pandas.read_sas` will load the files.

### 2. HRS (Health and Retirement Study): adults aged 50+
- **Why:** Useful as an older-adult US estimate and as the anchor for comparing with other countries.
- **Measurement:** Since 2006, a random half of the sample gets physical measures in a face-to-face interview each wave, so each person is measured every 4 years. Three readings are taken with an Omron monitor by **trained interviewers, not nurses**. Say this in your methods section.
- **Question:** "Has a doctor ever told you that you have high blood pressure or hypertension?"
- **Access:** Free registration at hrsonline.isr.umich.edu. The biomarker and physical-measure files are public. The RAND HRS longitudinal file makes the data much easier to work with. Sensitive or restricted files need a separate application.

## Other countries (middle-aged and older adults)

### 3. ELSA (English Longitudinal Study of Ageing): adults aged 50+, England
- **Measurement:** Blood pressure is measured by a **nurse** during nurse-visit waves: 2, 4, 6, and the 8/9 period. Check the exact years in the documentation.
- **Access:** UK Data Service (study SN 5050). You register, accept the End User Licence, and download for free. The nurse-visit data are in separate files within the study.
- **Alternative:** The Health Survey for England covers all ages, with nurse-measured blood pressure and a doctor-diagnosis question, through the same UK Data Service process. Nurse visits were suspended around COVID, so check which recent years include them.

### 4. CHARLS (China Health and Retirement Longitudinal Study): adults aged 45+
- **Measurement:** Trained interviewers take repeated readings with an Omron device. This was done in 2011, 2013 and 2015, and possibly 2018. The 2020 wave was mostly by phone and has no physical measures, so check the documentation for 2018 onward.
- **Access:** Free registration and a data request at charls.pku.edu.cn.

### 5. LASI (Longitudinal Ageing Study in India): adults aged 45+
- **Measurement:** Wave 1 (2017–19) measured blood pressure and asked about doctor diagnosis. The sample is very large and nationally representative. Awareness of hypertension is known to be low in India, which could give your chapter a striking contrast with the US.
- **Access:** Request through IIPS Mumbai, or through the Gateway to Global Aging Data (below).

### Shortcut: Gateway to Global Aging Data (g2aging.org)
This site provides harmonized files for HRS, ELSA, CHARLS, LASI, MHAS (Mexico) and others, with standardized blood pressure and diagnosis variables. One free registration gets you the harmonized files plus codebooks. You still need permission from each original study to get its raw data. This is the easiest way to make your cross-country comparison methodologically clean.

### Other options
- **KNHANES (Korea):** All ages, nationally representative, modeled on NHANES, with examiner-measured blood pressure. Free download after registering on the KDCA website. This is the closest one-to-one match to NHANES if you want a comparison that isn't limited to older adults.
- **CHMS (Canada):** Good measurement, but microdata are mostly available only through Statistics Canada Research Data Centres.
- **Avoid SHARE** (Europe) for this question. It generally doesn't measure blood pressure.

## Methods points to settle early
- **Hypertension definition:** Use 140/90 or 130/80 (ACC/AHA 2017). Count people on blood pressure medication as hypertensive, whatever their measured value.
- **Readings:** Average the 2nd and 3rd readings, or all valid readings, and keep it the same across surveys.
- **Awareness:** Measure it among people with hypertension, as doctor-diagnosed or on medication, divided by everyone with hypertension (measured or treated).
- **Who measured:** Nurses or examiners in NHANES and ELSA, lay interviewers in HRS, CHARLS and LASI. This can bias the comparison, so mention it as a limitation.

A practical setup would be NHANES as the main analysis, with HRS, ELSA and CHARLS or LASI via g2aging for the 50+ cross-country comparison. If you want help writing the NHANES code (weights, merging the `BPQ` and `BPXO` files, and the awareness estimate in R `survey` or Stata `svy`), I can do that.