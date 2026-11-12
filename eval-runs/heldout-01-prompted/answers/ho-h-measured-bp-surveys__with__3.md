I'd use NHANES as the US primary, with ELSA, CHARLS and LASI as the comparison surveys. I confirmed each survey's measured-BP component through its official documentation, a published description, or both. I did not confirm every step of every access process, and I note below where that applies.

## US: NHANES (primary)

- **What it is:** a nationally representative US survey of the civilian non-institutionalised population. It is run by CDC/NCHS and fits your design best.
- **Measured BP:** the exam files hold three oscillometric readings per person (e.g. `P_BPXO`, variables `BPXOSY1-3` and `BPXODI1-3`). The 2017–March 2020 file used an Omron HEM-907XL. Older cycles used auscultatory readings in the `BPX` files, which I did not open.
- **Awareness item:** the questionnaire file `BPQ` asks `BPQ020`, "ever told by a doctor or other health professional that you had hypertension". There are follow-ups on medication and age at diagnosis. Borderline or pre-hypertension answers and pregnancy-only hypertension are coded "No".
- **Cycles:** `BPQ_C` is 2003–04, then `BPQ_G`, `H`, `I` and `J` run through 2017–18. `P_BPQ` is the 2017–Mar 2020 pre-pandemic file, and `BPQ_L` is Aug 2021–Aug 2023. `BPQ_L` dropped some medication items and added `BPQ150`, so check the variables if you pool across cycles.
- **Access:** it is free and public, with no registration. You download the SAS transport (`.xpt`) files from the NHANES site. Merge on `SEQN`.
- **Analysis cautions:**
  - Use the exam (MEC) weights when you combine questionnaire and exam data.
  - The 2019–2020 data alone are not nationally representative.
  - Include the survey design variables.
  - It covers adults of all ages, so restrict to ≥45 or ≥50 if you want comparability with the other surveys.

## US longitudinal alternative: Health and Retirement Study (HRS)

- **What it is:** a US panel of adults aged 50 and over. Blood pressure is measured in the enhanced face-to-face interview, every four years, with participant consent.
- **Access:** registration is free. Create an account on the HRS Data Products page and agree to the conditions of use. Biomarker and other sensitive products need a supplemental application: submit the Sensitive Health Data Order Form and wait for approval.
- **Unconfirmed:** I could not tell whether the measured BP is in the public files or only in the sensitive-data tier. The HRS data site returned 403 to me, so check the physical-measures product documentation before you plan around it.
- **How I'd use it:** it is a secondary US source for the older-adult comparison. NHANES alone is probably enough for the US.

## Comparison surveys

**ELSA (England, aged 50+)**
- **Measured BP:** a nurse visit in waves 2, 4, 6 and 8 took the readings, and there is a user guide with a BP section.
- **Caveat:** waves 8 and 9 did a nurse visit on only half the sample. A 2026 paper reports a wave 11 nurse visit, which I did not verify in the catalogue.
- **Awareness item:** ELSA asks about doctor-diagnosed conditions in the main interview, but I did not verify the exact variable name. Check the codebook.
- **Access:** it is UK Data Service study SN 5050 and is free. If your institution is in the UK Access Management Federation, log in through it. Otherwise request a UKDS username. The End User Licence is open to all, and some files need Special Licence or Secure Access. Contact elsadata@natcen.ac.uk or elsa@ucl.ac.uk with questions.

**CHARLS (China, aged 45+)**
- **Measured BP:** it has measured BP, with a baseline in 2011–12 and follow-ups in 2013–14 and 2015.
- **Awareness item:** I did not verify the exact variable. The questionnaire has a doctor-diagnosed hypertension item.
- **Access:** it is free but requires registration. The 2011 baseline is on the Peking University Open Research Data Platform, where you apply to join the user group. Documentation is at charls.pku.edu.cn.
- **Caveat:** a 2020 analysis I found appears to rely on a different BP protocol. Check which waves have the same physical-measurement protocol before pooling.

**LASI (India, aged 45+)**
- **Measured BP:** wave 1 (2017–18) took three Omron HEM-7121 readings per person. It covers about 72,000 people across 35 states and union territories, and Sikkim was collected later. The Gateway to Global Aging harmonised file also includes measured BP.
- **Access:** it is free through IIPS after registration, and the IIPS data catalogue lists it. The access page is iipsindia.ac.in/content/LASI-data. I could not see the contact email, so get it from that page.
- **Published use:** at least one paper already studies undiagnosed hypertension in LASI wave 1, so the design is workable.

If you want a single harmonised route to HRS, ELSA, CHARLS and LASI, the Gateway to Global Aging (g2aging.org) provides harmonised files. I did not check its registration terms or confirm that it covers measured BP for every one of these surveys. Check that before relying on it.

**Practical notes for your analysis**
- Apply the same BP threshold (≥140/90 or on medication) and the same age range across all the surveys.
- Define "unaware" as measured hypertension with a "No" to the doctor-told question. Medication use is a separate indicator of treatment.
- Cycle and wave definitions differ across surveys. Each has its own weights, so run the analyses separately rather than pooling.

Sources:
- [NHANES BPQ_J documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BPQ_J.htm)
- [NHANES P_BPQ documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BPQ.htm)
- [NHANES BPQ_L documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm)
- [NHANES P_BPXO documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_BPXO.htm)
- [HRS sensitive health data](https://hrsdata.isr.umich.edu/data-products/sensitive-health)
- [HRS new user guide, July 2025](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf)
- [ELSA data access](https://www.elsa-project.ac.uk/accessing-elsa-data)
- [UKDS ELSA SN 5050](https://datacatalogue.ukdataservice.ac.uk/studies/study/5050)
- [ELSA nurse visit user guide (waves 2, 4, 6, 8)](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_waves_2-4-6-8_nurse_data_user_guide_v01_0.pdf)
- [CHARLS 2011 baseline, Peking University Open Research Data](https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi%3A10.18170%2FDVN%2FIZU8OF)
- [CHARLS, Maelstrom Research](https://www.maelstrom-research.org/study/charls)
- [LASI cohort profile](https://dx.doi.org/10.1093/ije/dyab266)
- [IIPS data catalogue, LASI](https://www.iipsdata.ac.in/datacatalog_detail/5)
- [LASI wave 1 undiagnosed hypertension paper](https://www.ovid.com/jnls/jfmpc/fulltext/10.4103/jfmpc.jfmpc_1695_24~cardiovascular-risk-assessment-among-undiagnosed)