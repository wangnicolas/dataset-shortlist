I searched for each survey and confirmed that the files or access pages exist. Search results are summaries, so a few details are marked "check" below. I did not open the HRS, ELSA or CHARLS data files themselves.

## Recommended surveys

| Survey | Measured BP | "Ever told" question | Access |
|---|---|---|---|
| **NHANES (US)** | Yes, in the exam (MEC) files | Yes, `BPQ020` in the BPQ file | Free, no registration |
| **HRS (US, age 50+)** | Yes, in the physical measures part of the interview | Core interview question (check the variable name) | Free, registration required |
| **ELSA (England, age 50+)** | Yes, in the nurse visit | Yes, in the main interview | Free, registration and licence |
| **CHARLS (China, age 45+)** | Yes, 3 readings per person | Yes, in the health module | Free, registration and approval |
| **LASI (India, age 45+)** | Yes, 3 readings per person | Yes, in the health module | Free, request to IIPS |

### NHANES (primary US source)
- **Awareness:** `BPQ020` asks whether a doctor or other health professional ever said the person had hypertension. It is in the BPQ questionnaire file, separate from the BP exam files. Related items cover medication use and age when first told.
- **Access:** The files are public SAS transport (.xpt) files with an .htm codebook per cycle, at `wwwn.cdc.gov/Nchs/Data/Nhanes/Public/<start year>/DataFiles/`. Examples are `BPQ_I.xpt` for 2015–16 and `P_BPQ.xpt` for 2017–March 2020. You download them directly and merge the BPQ file with the BP exam file on `SEQN`.
- **Weights:** Use the exam (MEC) weights when you combine questionnaire and exam data.
- **Cycle changes:** The 2021–23 BPQ file dropped several items, including `BPQ040A` and `BPQ050A`, and the medication question is now `BPQ150`.
- **Check:** I believe the 2021–23 cycle changed the BP device. Confirm that in the exam documentation before pooling cycles.

### HRS (older US adults)
- **Measured BP:** BP is taken in the enhanced face-to-face interview, which happens every four years for participants who consent to physical measures.
- **Access:** Public data needs a free account on the HRS site. Sensitive health data such as biomarkers needs a separate Sensitive Health Data order form.
- **Check:** The search results did not say whether the BP physical-measures files are public or sensitive. Look at the data descriptions for each wave, or the [new-user guide](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf). Also confirm the "doctor ever told you" variable name in the codebook.

### ELSA (England)
- **Measured BP:** The nurse visit happens every four years. Health visit data are archived for waves 2, 4, 6 and 8, plus a wave 0 file based on the Health Survey for England. A recent paper used wave 11 nurse data, so later waves may now be archived. Check the catalogue.
- **Half-sample waves:** The wave 8 and 9 nurse visits covered only half the sample.
- **Access:** Register with the UK Data Service and accept the End User Licence, then download study SN 5050. The ELSA project's [access page](https://www.elsa-project.ac.uk/accessing-elsa-data) lists the contacts. Use the "User Guide to the Nurse Visit Datasets" for the BP variables.
- **Merging:** You merge the nurse files with the main interview files, which hold the diagnosis question.

### CHARLS (China)
- **Measured BP:** Staff took three readings 45 seconds apart on the left arm with an Omron HEM-7200. It was measured in 2011, 2013 and 2015.
- **Access:** Register and sign the agreement at charls.pku.edu.cn/en. Approval took about 3 days in the older guide, and the data are free. Check the site for the current process.
- **Shortcut:** The Harmonized CHARLS file (codebook at g2aging.org) has a Physical Measures section with BP. Downloading it requires registration for both CHARLS data access and the forum.

### LASI (India)
- **Measured BP:** Wave 1 (2017–18) took three readings five minutes apart and averaged the last two. One paper notes BP was measured on a single occasion and some participants have no BP reading.
- **Access:** Request the data through the IIPS data catalogue at iipsdata.ac.in, where it is listed as free with a request column. Another source gives [iipsindia.ac.in/content/LASI-data](https://www.iipsindia.ac.in/content/LASI-data). A harmonized version is on the Gateway to Global Aging Data (g2aging.org).
- **Not what you need:** LASI-DAD (lasi-dad.org) is a separate cognition and dementia sub-study.

## Recommendation
Use **NHANES** as the main analysis, because it covers all adults and has the longest run of cycles. Add **ELSA** as the comparison, since its access process is simple and its nurse-measured BP is well documented. Use **HRS** if you want a US cohort of the same age range as ELSA. Add **CHARLS** or **LASI** if you want a middle-income comparison.

Whichever you pick, define "hypertension" the same way in each survey. A common definition is mean BP of at least 140/90 mmHg or taking antihypertensive medication. Your awareness measure is then the share of those people who report being told they have hypertension. Note that the BP devices, number of readings and which readings are averaged differ across these surveys.

Sources:
- [NHANES BPQ file listing and codebooks (CDC)](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm)
- [NHANES BPQ question-testing report (CDC Q-Bank)](https://wwwn.cdc.gov/qbank/report/NHANESBPQQuestionnaire.pdf)
- [ELSA nurse visit user guide, waves 2, 4, 6, 8](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/5050_waves_2-4-6-8_nurse_data_user_guide_v01_0.pdf)
- [ELSA in the CESSDA data catalogue](https://datacatalogue.cessda.eu/detail/99f93be30fe9ab3a1f8c339e754676dd9b70339a819883f60a531ea77063451d?lang=en)
- [HRS new user guide, July 2025](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf)
- [HRS sensitive health data](https://hrsdata.isr.umich.edu/data-products/sensitive-health)
- [CHARLS national baseline user guide](https://charls.charlsdata.com/Public/ashelf/public/uploads/document/2011-charls-wave1/application/CHARLS_nationalbaseline_users_guide.pdf)
- [Harmonized CHARLS documentation](https://charls.charlsdata.com/Public/ashelf/public/uploads/document/harmonized_charls/application/Harmonized_CHARLS_D.pdf)
- [LASI hypertension awareness paper (Springer)](https://link.springer.com/article/10.1186/s41043-023-00404-3)
- [IIPS data catalogue, LASI](https://www.iipsdata.ac.in/datacatalog_detail/5)