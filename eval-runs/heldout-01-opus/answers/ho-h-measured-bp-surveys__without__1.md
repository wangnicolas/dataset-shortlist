For the US, use **NHANES**. For the comparison countries, I'd use **ELSA** (England) and either **CHARLS** (China) or **KNHANES** (South Korea). All four measure blood pressure as part of an exam and also ask whether a doctor ever told the respondent they have high blood pressure, so you can count people who meet the measured or medication definition but say they were never told.

## 1. NHANES (United States): your main survey

- **Why:** It's a nationally representative sample of all ages. Blood pressure is measured at a mobile exam centre (MEC), and CDC uses it for its own official figures on hypertension awareness. CDC Data Brief 511 reports these for Aug 2021–Aug 2023 (prevalence 47.7%), so you can check your numbers against it.
- **Files for the latest cycle (2021–2023, suffix `_L`):**
  - `BPXO_L`: three oscillometric readings (`BPXOSY1–3`, `BPXODI1–3`).
  - `BPQ_L`: the questionnaire with "ever told you had high blood pressure" and BP medication use.
  - `DEMO_L`: demographics, plus the survey design variables (`SDMVSTRA`, `SDMVPSU`) and the exam weight (`WTMEC2YR`).
- **Access:** None needed. The public XPT files download freely from the CDC NHANES site, with no registration.
- **Things to watch:**
  - From 2021 NHANES switched from auscultatory readings (`BPX` files in older cycles) to oscillometric ones. If you pool or trend across cycles, the protocol change matters.
  - Use the MEC exam weights, not the interview weights, and account for the survey design (stratum and PSU).
  - The 2017–March 2020 "pre-pandemic" file is the previous usable cycle.

## 2. ELSA (England, ages 50+): best match for older adults

- **Why:** It's a nationally representative sample of people aged 50 and over. A study nurse measures blood pressure at a home visit, following the Health Survey for England protocol. The core interview asks about doctor-diagnosed high blood pressure, and the nurse visit also records prescribed medications.
- **Which waves:** Nurse visits took place in waves 2, 4, 6, 8 and 9. In wave 9 (2018/19) only half the sample got a visit. Use the nurse-visit weights.
- **Access:**
  1. Register with the UK Data Service (study SN 5050).
  2. Accept the End User Licence, which is free for academic use.
  3. Download.

  I think the main nurse files are in the End User Licence release, but I couldn't confirm that. Check the access level on the SN 5050 catalogue page. Some variables are under Special Licence, which takes a short extra application.
- **Contact:** ELSAdata@natcen.ac.uk.

## 3. A third survey: choose one

- **CHARLS (China, ages 45+):** It's nationally representative. Trained field staff take three Omron readings rather than nurses, and you get the doctor-diagnosis question and medication use. It's widely used for studies of hypertension awareness. **Access:** register free on the CHARLS website (charls.pku.edu.cn), state how you'll use the data, and download once approved, usually within days.
- **KNHANES (South Korea, all ages):** It's built on the NHANES model, so it's the closest match in design: standardized measurement by trained examiners, plus a diagnosis question. **Access:** register free on the KDCA KNHANES site and submit a short data request. The documentation is partly in English.
- **Also possible:** LASI (India, 45+) has the same type of design as CHARLS. You request it through IIPS or the Gateway to Global Aging. HRS, the US sister study to ELSA, has had physical measures including BP, taken by interviewers in half the sample each wave since 2006, but NHANES is the stronger US source.

**Practical tip:** ELSA, CHARLS, LASI and HRS are harmonized by the **Gateway to Global Aging Data** (g2aging.org). It publishes consistent variable definitions across studies, which makes cross-country comparisons much easier to defend in a thesis.

**Methods points to settle early:**
- Pick one threshold, 140/90 or ACC/AHA 130/80, and apply it everywhere. Report the other one as a sensitivity analysis.
- Define "hypertensive" as measured high BP *or* taking BP medication.
- Average the readings the same way in every survey (e.g., the mean of the 2nd and 3rd).
- Note the measurement differences: nurse versus trained interviewer, and oscillometric versus auscultatory.

Sources:
- [NHANES 2021–2023 Examination Data](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Examination&Cycle=2021-2023)
- [NHANES 2021–2023 Questionnaire Data](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Questionnaire&Cycle=2021-2023)
- [NCHS Data Brief 511](https://www.cdc.gov/nchs/products/databriefs/db511.htm)
- [ELSA Wave 4 Nurse Dataset User Guide](https://ifs.org.uk/sites/default/files/output_url_files/wave_4_nurse_dataset.pdf)
- [ELSA Wave 9 Technical Report (UKDS SN 5050)](https://doc.ukdataservice.ac.uk/doc/5050/mrdoc/pdf/5050_elsa_w9_technical_report_v3.pdf)
- [UKDS ELSA update](https://ukdataservice.ac.uk/app/uploads/pacchiotti.pdf)
- [ELSA on Atlas of Longitudinal Datasets](https://atlaslongitudinaldatasets.ac.uk/datasets/elsa)