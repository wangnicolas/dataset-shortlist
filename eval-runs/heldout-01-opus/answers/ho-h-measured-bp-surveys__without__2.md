For your question the core requirement is a measured-BP-plus-diagnosis survey. NHANES is the obvious US choice. For international comparison, the HRS "sister studies" (ELSA, CHARLS, LASI) and Korea's KNHANES work best. I wrote this from memory and didn't check the websites this session, so confirm wave years and access steps against current documentation before citing them.

## United States

### 1. NHANES (National Health and Nutrition Examination Survey): use this as your primary source
- **Why it fits:** It is the standard source for US hypertension awareness estimates. It is nationally representative of the civilian non-institutionalized population. Trained examiners measure BP in a mobile examination center (MEC), using up to three readings. Older cycles used a manual cuff. Since 2017–2018 an automated oscillometric protocol is used (files `BPXO_*`; earlier files are `BPX_*`).
- **Key variables:**
  - `BPQ020`: "Ever told by a doctor or other health professional that you had hypertension/high blood pressure?"
  - `BPQ040A`/`BPQ050A`: told to take, and now taking, BP medication. You need these to define hypertension as measured high BP *or* on medication.
- **Access:** Free public-use files (SAS XPT format), no registration. Download from the CDC/NCHS NHANES site (wwwn.cdc.gov/nchs/nhanes). In R, the `nhanesA` package fetches files directly.
- **What you must do:**
  - Merge the demographics (DEMO), BP exam (BPX/BPXO) and BP questionnaire (BPQ) files on `SEQN`.
  - Use the **MEC exam weights** (`WTMEC2YR`, or the special weights for the 2017–March 2020 pre-pandemic file) with `SDMVPSU`/`SDMVSTRA` in a survey-design analysis (R `survey`, Stata `svy`).
  - Follow the NCHS analytic guidelines when combining cycles.
- **Watch out for:**
  - The switch from manual to oscillometric measurement. NCHS ran a crossover comparison in 2017–2018, which you should cite if you look at trends.
  - COVID disrupted collection. There is a 2017–March 2020 pre-pandemic file and then a separate August 2021–August 2023 cycle.

### 2. HRS (Health and Retirement Study), ages 50+: optional
- Interviewers measure BP during in-home "enhanced face-to-face" interviews, with each random half of the sample measured every other wave since 2006. HRS also asks whether a doctor ever told the respondent they have high BP.
- Access is free after registering on the HRS website (University of Michigan). The physical measures are in the public core files. Blood biomarkers carry extra restrictions, but you don't need them.
- Use it only if you need longitudinal data or exact comparability with the international aging studies below. Note that interviewers take the readings, not nurses, so mention that if you're strict about who measures.

## International comparisons

**Option A: Harmonized aging studies (best for comparability with HRS, or with NHANES restricted to ages 50+)**
- **ELSA (English Longitudinal Study of Ageing, 50+):** A nurse visit with BP measurement took place roughly every other wave (2, 4, 6 and 8/9), and the survey has a doctor-diagnosis question. Access is through the **UK Data Service**: register, accept the End User Licence, and it's free for academic use. The nurse-visit data sit in separate files and have their own weights.
- **CHARLS (China, 45+):** Trained staff measure BP with Omron devices (2011, 2013 and 2015 are the main waves with physical measures; check later waves). It asks about doctor-diagnosed hypertension. Free after registering on the CHARLS site at Peking University.
- **LASI (India, 45+, Wave 1 2017–19):** Measured BP plus a diagnosis question, with a very large sample. You apply through IIPS / the LASI data portal.
- **Tip:** The **Gateway to Global Aging Data** (g2aging.org) offers harmonized versions of HRS, ELSA, CHARLS and LASI with consistent variable definitions. That saves a lot of recoding and gives you a citable harmonization source.

**Option B: An NHANES clone**
- **KNHANES (Korea):** Modeled directly on NHANES. Trained examiners measure BP, there is a doctor-diagnosis question, it covers all ages, and it runs annually. Download it free after registering on the KDCA KNHANES website. Some documentation is Korean-only.
- **CHMS (Canadian Health Measures Survey)** is also comparable, but microdata access requires a Statistics Canada Research Data Centre application, which is slow for a thesis.

**Avoid:** SHARE (Europe) for this question. Except for limited sub-studies, it doesn't measure BP, so you'd be back to self-report.

## My recommendation
Use **NHANES** as the core. Add **ELSA** plus either **CHARLS** or **LASI** through the Gateway harmonized files. If you want a high-income, all-ages comparator with the same design, use **KNHANES** instead. Restrict every sample to the same age band (e.g., 50+) for the comparison.

## Methods points examiners will ask about
1. **Definition:**
   - Hypertension = mean SBP ≥140 or DBP ≥90 (or ≥130/80 under the 2017 ACC/AHA definition), **or** current antihypertensive use.
   - Unaware = has hypertension but answered "no" to the doctor-told question.
   - Report results under both thresholds.
2. **Readings:** Most studies average the 2nd and 3rd readings and drop the first. Apply the same rule across all surveys.
3. **Single-visit bias:** Clinical diagnosis needs repeated visits, but these surveys measure once. That overstates prevalence and therefore "unawareness." Acknowledge it as a limitation.
4. **Device and protocol differences** across surveys (manual vs. oscillometric, examiner type) limit direct comparisons. Describe them in a table.