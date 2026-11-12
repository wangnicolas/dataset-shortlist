You can do this with NHANES for the US and ELSA plus one of CHARLS or LASI for other countries. I checked these through search results and one verified CDC page. I did not build the interactive shortlist page. Only one record (the NHANES questionnaire page) passed the verification tool. The UK Data Service, HRS and Michigan biomarker-network pages block automated checks, so I couldn't read their access terms directly. Where I say "from memory", I haven't confirmed it.

## What I assumed you need
- **R1 (must):** A measured blood pressure (BP) by an examiner or nurse.
- **R2 (must):** A "has a doctor ever told you that you have high BP" question in the same respondents.
- **R3 (must):** A nationally representative sample with survey weights.
- **R4:** US first, plus one or two comparable countries.
- **R5:** Middle-aged and older adults are fine.
- **R6:** Free microdata that you can get without a long wait.

## Shortlist
| # | Dataset | Access | Fit | Checked |
|---|---|---|---|---|
| 1 | NHANES (US, all ages, 1999 to 2023) | Open download, no registration (from memory) | Strong | Questionnaire item confirmed today; access from memory |
| 2 | HRS (US, age 50+) | Free registration. Possibly an extra "sensitive data" step. | Strong | Search results only |
| 3 | ELSA (England, age 50+) | Free UK Data Service registration, End User Licence | Strong | Search results only |
| 4 | CHARLS (China, age 45+) | Free registration | Strong | Search results, plus the Gateway to Global Aging page |
| 5 | LASI (India, age 45+) | Open download from several hosts | Strong | Search results only |
| 6 | KNHANES (Korea, all ages) | Free registration, Korean-language site | Strong | Search results only |
| 7 | MHAS (Mexico, age 50+) | Free registration, BP only from 2012 | Partial | Search results only |
| 8 | TILDA (Ireland, age 50+) | Application and fees | Strong, but slow | Search results only |

## Details

**1. NHANES (US).**
- **What it has:** Examiners measure BP in the mobile exam centre, and the household interview asks `BPQ020` ("ever told you had high blood pressure"). The interviewer codes pregnancy-only and "borderline" answers as No. `BPQ030` asks whether you were told on two or more visits.
- **Confirmed today:** The CDC [BPQ documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm) loaded, and `BPQ020` was described in the questionnaire PDFs.
- **From memory:**
  - The exam files are `BPX*`.
  - Download is open with no registration and no application, so you can start today.
  - The data are US public domain.
- **Method notes:**
  - Use the exam (MEC) weights when you merge exam and questionnaire files.
  - The 2021–2023 cycle dropped several follow-up items, so check the questions you need cycle by cycle.

**2. HRS (US, age 50+).**
- **What it has:** A longitudinal panel with measured BP in the physical-measures component from 2006. I recall that the diagnosis question is "Has a doctor ever told you that you have high blood pressure or hypertension?" (from memory).
- **Access:** Search results say registration is free. The dried-blood-spot and venous-blood biomarkers are "sensitive" data, which need an order form and a use agreement. One paper used BP from the public physical-measures files, so BP may not need the sensitive step. Confirm this on the [HRS sensitive data page](https://hrsdata.isr.umich.edu/data-products/sensitive-health) and in the [New User Guide](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf).
- **Method note:** BP was measured in a rotating half-sample each wave (from memory).

**3. ELSA (England).**
- **Why it's the best comparator for the US:** Nurse visits measure BP at Waves 2, 4, 6 and 8, plus a half-sample at Wave 9. Wave 0 came from the Health Survey for England.
- **Access:** The data are on the UK Data Service as [SN 5050](https://datacatalogue.ukdataservice.ac.uk/studies/study/5050). The catalogue lists them as "safeguarded", so you register and accept the End User Licence. That takes days.
- **Check yourself:** The catalogue page needs a browser, so I couldn't confirm the record. Also check which nurse waves are in the current edition.
- **Docs:** The [nurse visit user guide](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_waves_2-4-6-8_nurse_data_user_guide_v01_0.pdf).
- **Contacts:** ELSAdata@natcen.ac.uk or elsa@ucl.ac.uk.

**4. CHARLS (China).**
- **What it has:** BP was measured three times at Waves 1 to 3 (2011, 2013, 2015), and there is a 2020 wave. The interview has a doctor-diagnosis question (from memory).
- **Access:** Free, with registration on the CHARLS site (charls.pku.edu.cn). The [Gateway to Global Aging page](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d) says harmonized files can be downloaded by any registered user.
- **Check yourself:** Which waves include BP and the diagnosis question.

**5. LASI (India).**
- **What it has:** Wave 1 (2017–18) has measured BP, taken three times at five-minute intervals. The sample is age 45+.
- **Access:** Wave 1 microdata and documentation are public via IIPS, data.gov.in, lasi-india.org and the Gateway to Global Aging. The Gateway's harmonized file includes the measured BP.
- **Check yourself:** The licence terms were not read.
- **Prior use:** Two LASI hypertension awareness papers are listed under evidence of use below.

**6. KNHANES (Korea).**
- **What it has:** An examination survey like NHANES. Published papers define awareness as a prior diagnosis by medical personnel.
- **Access:** Download from [knhanes.kdca.go.kr](https://knhanes.kdca.go.kr) after a login. Raw data come out each December for the previous year's survey. Documentation is largely Korean.

**7. MHAS (Mexico).**
- **What it has:** BP was first measured in 2012, in a subsample, and again in 2018. Use the biomarker weight (`factora_12` for 2012).
- **Access:** Free registration at [mhasweb.org](https://www.mhasweb.org/DataProducts/Home.aspx).

**8. TILDA (Ireland).**
- **What it has:** A health-assessment BP measurement at Waves 1 and 3 only.
- **Access:** ICPSR has withdrawn it, so older guides pointing there are out of date. You apply to TILDA directly (tilda@tcd.ie, [tilda.tcd.ie](https://tilda.tcd.ie/)), and fees apply. Plan for weeks.

## Evidence of use
These are the papers the search returned:
- [Cardiovascular Risk Factor Prevalence and Control by Education Strata in Older Adults in 3 Countries](https://doi.org/10.1001/jamanetworkopen.2026.25410) (2026). It compares the US, England and South Korea in adults 50+, so it is close to your design. I only read the abstract, so check which surveys it used.
- [LASI awareness, treatment and control, middle-aged and older](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8726460/).
- [Sex-specific LASI hypertension analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10464490/).
- [KNHANES hypertension awareness trends](https://pmc.ncbi.nlm.nih.gov/articles/PMC6662850/).

## Known, not confirmed
- **Health Survey for England** (nurse-measured BP plus a doctor-diagnosis question, from memory). I didn't search for it, and it is probably the other UK option.
- **SAGE (WHO)** and **Canadian Health Measures Survey** (both from memory). I didn't search for either.
- **SHARE** does not measure BP, as far as I recall. Confirm before ruling it in or out.

## Not recommended
- **Anything self-report only.** The registry hits were mostly paper supplements, small clinic studies and synthetic data. None is nationally representative.

## What I could not find
- **Terms I couldn't read:** Licence terms for ELSA, CHARLS, LASI and KNHANES, and the exact HRS sensitive-data rule for BP.
- **Registries:** The registry tool only searched DataCite, Hugging Face, OpenAIRE, PhysioNet and Zenodo. These surveys sit in their own archives, so I found them by web search.
- **Variables:** I didn't check variable names, so confirm them in each codebook.

## Next step
1. Download the NHANES `BPX` and `BPQ` files today and build your awareness cascade there.
2. Register with UKDS for ELSA.
3. Register with CHARLS or download LASI.
4. Confirm the HRS BP file tier before you plan around it.

Access details were checked on 2026-11-12, and these rules change, so re-check each one before you rely on it.