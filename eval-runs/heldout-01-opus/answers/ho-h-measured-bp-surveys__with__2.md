I'd use **NHANES** as the US source. For the other countries, **ELSA (England)** and either **CHARLS (China)** or **LASI (India)** are the strongest options. All four put measured blood pressure and a "doctor ever told you" question on the same people. HRS, ELSA, CHARLS and LASI are also sister studies, and ready-made cross-country versions of their variables are on the Gateway to Global Aging Data (g2aging.org). That makes the international comparison much easier.

I checked these on 12 Nov 2026. "Today" in the Checked column means I confirmed it from the official page or the study's own documents. "From memory" means I didn't. Access rules change, so re-check before you submit an ethics application.

## What I assumed you need
- **R1 (must):** a nationally representative sample. Adults of all ages, or 45+/50+, is fine.
- **R2 (must):** blood pressure measured by a nurse, examiner or trained field staff.
- **R3 (must):** a "has a doctor ever told you that you have high blood pressure" question, asked of the same people.
- **R4 (nice to have):** you can get the data within weeks on a student's standing.

## Shortlist
| # | Survey | Access | Who measured BP | Checked |
|---|---|---|---|---|
| 1 | **NHANES** (US, all ages) | Direct download, no account | Health technicians at mobile exam centres | today |
| 2 | **HRS** (US, 50+) | Free registration | Trained interviewers, not nurses | today, from HRS documents |
| 3 | **ELSA** (England, 50+) | Free UK Data Service account and End User Licence, ~days | Nurses (waves 2, 4, 6, 8, 9) | today |
| 4 | **CHARLS** (China, 45+) | Registration plus online agreement, approved in ~3 working days | Trained staff, 3 Omron readings | today, from the CHARLS FAQ |
| 5 | **LASI** (India, 45+, ~72,000 people) | Request form plus short proposal (~weeks), or through g2aging.org | Trained staff | today |
| 6 | **KNHANES** (Korea, all ages) | Registration and data request | Examiners | partly |
| 7 | **TILDA** (Ireland, 50+) | Public file through ISSDA (Irish Social Science Data Archive); fuller data by application, possibly with fees | Nurses | today |
| 8 | **Canadian Health Measures Survey** (CHMS) | Only inside Statistics Canada Research Data Centres, ~months | Mobile clinic staff | access rules from memory |

## Details
**1. NHANES** ([wwwn.cdc.gov/nchs/nhanes](https://wwwn.cdc.gov/nchs/nhanes/))
- **Variables:** BP readings are in the BPX/BPXO files (automated cuff from 2017 onward). The awareness question is BPQ020. I confirmed its wording today: "ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?" Related items are BPQ030 (told on 2+ visits) and BPQ150 (taking prescribed BP medication).
- **Steps:**
  - Download the DEMO, BPXO and BPQ files for a cycle and merge them on SEQN.
  - Use the exam weights plus the design variables SDMVSTRA and SDMVPSU.
- **Watch out for:**
  - The 2021–2023 cycle used a new sample design, so read the analysis guidelines before pooling it with earlier cycles.
  - The switch from manual to automated BP measurement affects trend analyses.
- **Example paper:** Egan et al., JAMA 2010 ([doi](https://doi.org/10.1001/jama.2010.650)), uses the standard awareness definition.

**2. HRS** ([New User Guide](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf), [physical-measures documentation DR-011](https://hrsonline.isr.umich.edu/sitedocs/userg/dr-011.pdf))
- **Variables:** BP was measured with an Omron HEM-780 during the in-person interview from 2006 onward. Each half of the sample is measured every 4 years.
- **Access:** BP is in the public core files and needs only registration. The blood biomarkers need an extra sensitive-data agreement.
- **Weights:** use the physical-measures weights (KPMWGTR for 2006, NPMWGTR for 2012).
- **Watch out for:** interviewers took the readings, not nurses. If your examiners must be nurses, say this in your methods.

**3. ELSA** ([how to access the data](https://www.elsa-project.ac.uk/accessing-elsa-data), [nurse visit user guide](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_elsa_waves_2-4-6-8-9_nurse_data_user_guide.pdf))
- **Access:** the ELSA site says: "End User Licence level data are available to all via UKDS."
- **Steps:**
  - Register with the UK Data Service. Use your institution's login (UKAMF) if your institution is a member, otherwise request a username.
  - Download study SN 5050, which includes the nurse files, and use the nurse weights.

**4. CHARLS** ([FAQ](https://charls.pku.edu.cn/en/Faq/Frequently_Asked_Questions.htm))
- **Variables:** the question is "Have you ever been diagnosed with hypertension by a doctor?" BP is measured as three Omron HEM-7200 readings.
- **Steps:**
  - Register at charls.pku.edu.cn and sign the online data-use agreement.
  - Activate your account by email, then apply for each dataset. The FAQ says approval takes about 3 working days.
  - Use the official site only, not the unofficial copies that circulate online.
- **Example papers:** [BMJ Open 2016](https://doi.org/10.1136/bmjopen-2015-009836) compares self-reported and measured hypertension. [BMC Public Health](https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-019-6753-x) looks at awareness from 2011 to 2015.

**5. LASI** ([request form](https://iipsindia.ac.in/sites/default/files/LASI_DataRequestForm_0.pdf), [cohort profile](https://doi.org/10.1093/ije/dyab266))
- **Variables:** the question is "Has any health professional ever told you that you have hypertension or high blood pressure?"
- **Steps:** email the form, a 500-word description of your topic and a study proposal to datacenter@iipsindia.ac.in. Alternatively, register on g2aging.org for the harmonised version.
- **Example paper:** [PMC8425529](https://pmc.ncbi.nlm.nih.gov/articles/PMC8425529) covers awareness, treatment and control in India.

**6–8.**
- **KNHANES:** the closest copy of NHANES's design. Literature found in a web search today says the raw data need registration and a request. KNHANES's English page returned a 404 today, and the site is mostly in Korean. I couldn't tell whether researchers outside Korea can register.
- **TILDA:** the site says the data are "only available for access by non-commercial entities." The fuller health data go through the VISTA remote secure environment or on-site desks, and fees may apply. I haven't checked which BP variables are in the public ISSDA file.
- **CHMS:** realistic only if you have a Canadian affiliation.

## Known, not confirmed
- **Health Survey for England:** nurse-measured BP, distributed through the UK Data Service. Its site blocked my automated check. ELSA already includes an HSE baseline ("wave 0").
- **Indonesia Family Life Survey (IFLS):** measured BP, free registration through RAND, from memory. RAND's site blocked the check.
- **WHO SAGE** (six low- and middle-income countries, measured BP): the catalogue page resolves, but I didn't read its access terms.
- **MHAS (Mexico):** measured BP in a subsample only (from memory). I didn't confirm it.

## Not recommended, and why
- **NHIS and BRFSS:** self-reported hypertension only.
- **SHARE:** no measured BP in its core waves (from memory).
- **UK Biobank:** a volunteer cohort, not nationally representative, and fee-based.

## What I could not find
The general dataset registries returned nothing relevant. Every candidate came from my own knowledge, the literature and web searches, which is normal for national surveys.

## Next step
Start downloading NHANES today. At the same time, register with the UK Data Service for ELSA and with CHARLS, which should take a few days. If you'd like India instead of, or as well as, China, send the LASI request now, because it takes the longest. Before you analyse anything, fix one definition of "unaware" across all surveys: measured BP ≥140/90 (or ≥130/80), or on BP medication, but not reporting a diagnosis. Also note how many readings each survey averages, because that differs between them.

The interactive comparison page is at `/private/tmp/e-jq5eMJ/home/cwd/dataset-shortlist.html`.