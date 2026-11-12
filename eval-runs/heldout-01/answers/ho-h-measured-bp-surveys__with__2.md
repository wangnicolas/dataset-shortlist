For your chapter I'd use NHANES as the main US source. Add ELSA (England) and either LASI (India) or CHARLS (China) as comparators. Only part of this is confirmed against official pages today (12 Nov 2026), and I've marked which.

I didn't build the interactive shortlist page. The registry search returned almost only paper supplements, and the real sources live on agency sites.

## What I assumed you need
- **R1:** Nationally representative adults.
- **R2:** BP measured by an examiner or interviewer, not self-reported.
- **R3:** A "ever told by a doctor you have high blood pressure" item, plus a BP medication item, so you can classify aware and unaware among the measured-hypertensive.
- **R4:** Middle-aged and older samples are fine abroad.
- **R5:** Free or academic access is fine.

## Shortlist
| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | **NHANES** (US, CDC/NCHS) | Direct download, no account (from memory) | US government data, public use, with a data user agreement | Meets R1–R3. Examiner-measured BP in the mobile exam centre, plus the BP questionnaire. | Page confirmed today; variables from memory |
| 2 | **ELSA** (England, 50+) | Free UKDS account, download at End User Licence level | UKDS End User Licence | Nurse-visit waves have measured BP, and the interview asks about doctor-diagnosed hypertension. | Access confirmed today; contents from memory |
| 3 | **HRS** (US, 50+) | Free registration for public files. Biomarker and sensitive health files need a supplemental order form. | HRS terms and conditions | Interviewer-measured BP in the physical measures, plus the doctor-told item. | Access from search today; contents from memory |
| 4 | **LASI** (India, 45+, 2017–18) | Request form to IIPS | Confidential-data conditions | Measured BP and doctor-diagnosis items. Published awareness analyses exist. | Access from search today |
| 5 | **CHARLS** (China, 45+) | Free account on the project site (from memory) | Project terms | Measured BP plus a doctor-diagnosis item. | Site showed a login and register page today; the rest is from memory |

## Details

**NHANES** is the home page (https://wwwn.cdc.gov/nchs/nhanes/), and it lists a Data User Agreement and ethics approval documentation.
- **Steps:** Open the cycle you want and download the examination BP file, the BP and cholesterol questionnaire file and the demographics file. Merge them on the participant ID (SEQN).
- **Variable:** The doctor-told item is, from memory, `BPQ020`, which asks if a doctor or other health professional ever told the person they had hypertension. Check the code in the cycle's codebook.
- **Method point:** The most recent cycles switched from a mercury sphygmomanometer to an oscillometric device. From memory, that affects comparability across years. I couldn't confirm the file names today. My one guessed URL returned a 404, so I'm not giving you a link.
- **Complex survey:** Use the MEC exam weights and the strata and PSU variables.

**ELSA** (https://www.elsa-project.ac.uk/accessing-elsa-data)
- The page says: "Researchers can download ELSA data from waves 1-11 including wave 0 (HSE), from the UK Data Service."
- It also says: "Note that End User Licence level data are available to all via UKDS."
- UK institutions log in with their institutional account. Everyone else requests a username.
- From memory, only some waves have nurse visits, so check which waves carry BP before you design the analysis.

**HRS** (https://hrs.isr.umich.edu/data-products)
- My fetch of this page was refused (HTTP 403), so I used a web search.
- Public data are free to registered users. Biomarker and sensitive health data need an extra step, via the Sensitive Health Data Order Form (https://hrsdata.isr.umich.edu/data-products/sensitive-health).
- It is unclear whether the measured BP values sit in the public core files or only in the biomarker files. Check the new-user guide (https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf) before planning around it.
- From memory, physical measures were taken on a rotating half-sample from 2006.

**LASI**
- Wave 1 data and documentation are reported to be available through the IIPS site, data.gov.in and the Gateway to Global Aging.
- The request form is at https://iipsindia.ac.in/sites/default/files/LASI_DataRequestForm_0.pdf. A PLOS Medicine paper says data go to researchers who meet the criteria for confidential data. This is second-hand, and my direct fetch of an IIPS page returned a 404.
- Per a secondary paper, three BP readings were taken and the last two averaged. BP is missing for about 9% of participants.
- A close methods precedent is the PLOS Medicine paper on [hypertension awareness, treatment and control in India](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.1003740).

**CHARLS** (https://charls.charlsdata.com/)
- The data page lists the 2011 baseline through the 2021–23 follow-up, plus Harmonized CHARLS.
- The page is drawn by JavaScript, so I couldn't read the terms. From memory, it needs a free account and an application describing your use, and it's usually fast.

## Known, not confirmed
- **KNHANES (Korea):** From memory, a free download after registering with KDCA. I didn't check it.
- **Health Survey for England:** From memory, a nurse-measured BP survey via UKDS, with a self-report item on doctor-diagnosed hypertension.

## Not recommended
- **SHARE:** From memory, it has no routine BP measurement, so you can't classify unaware hypertension.
- **Add Health, L.A.FANS and the Zenodo, figshare and Hugging Face hits:** These are not representative adult surveys or are derivative files. Re-analysis files are not the source.

## What I could not find
- I couldn't confirm the exact NHANES file names for each cycle.
- I couldn't read the CHARLS or HRS terms pages directly.
- I didn't run the paper lookup for each dataset.

## Next step
1. Start with NHANES, since you need no approval.
2. Register for ELSA at UKDS and for HRS the same day.
3. Submit the LASI or CHARLS request early, since those are the slow ones.
4. Define "aware" before merging. The standard definition is among people with measured SBP ≥140 or DBP ≥90 or on BP medication, the share who report a doctor told them. Check that each survey's measurement protocol matches.

Sources:
- [NHANES](https://wwwn.cdc.gov/nchs/nhanes/)
- [ELSA data access](https://www.elsa-project.ac.uk/accessing-elsa-data)
- [HRS data products](https://hrs.isr.umich.edu/data-products)
- [HRS sensitive health data](https://hrsdata.isr.umich.edu/data-products/sensitive-health)
- [LASI data request form](https://iipsindia.ac.in/sites/default/files/LASI_DataRequestForm_0.pdf)
- [CHARLS](https://charls.charlsdata.com/)