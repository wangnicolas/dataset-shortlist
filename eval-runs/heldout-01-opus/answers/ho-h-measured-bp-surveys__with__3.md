For the US, use **NHANES**. For the other countries, use **ELSA (England)** plus **CHARLS (China)** or **LASI (India)**. ELSA uses nurses, CHARLS and LASI use trained staff. These three non-US surveys and the **HRS** (the US Health and Retirement Study, adults 50+) are harmonised with each other. A 2023 JAHA paper ([doi:10.1161/jaha.123.030765](https://doi.org/10.1161/jaha.123.030765)) already compared measured-BP hypertension across HRS, ELSA, CHARLS and LASI, so you have a methods precedent to cite.

I checked access on 12 Nov 2026. Where something comes from memory, I say so.

## Shortlist

| # | Survey | Who measures BP | How you get it | Time | Checked |
|---|---|---|---|---|---|
| 1 | **NHANES** (US, all ages) | Certified examiners in a mobile exam centre | Free download, no login | minutes | today |
| 2 | **HRS** (US, 50+) | Trained interviewers in the home, not nurses | Free registration | minutes | HRS documentation, via search |
| 3 | **ELSA** (England, 50+) | Nurse visit | Free UK Data Service account | minutes–days | today |
| 4 | **CHARLS** (China, 45+) | Trained staff, 3 readings | Free registration and request | days | CHARLS documentation, via search |
| 5 | **LASI** (India, 45+) | Trained field staff | Request form with ID, reviewed in 24–48 h | days | today |
| 6 | **KNHANES** (Korea, all ages) | Examiners, NHANES-style | Free registration | days | papers' data statements |
| 7 | TILDA (Ireland, 50+) | Nurse health assessment | Application, non-commercial users only | weeks | today |
| 8 | CHMS (Canada) | Mobile clinic | Research Data Centre only | months | today |

## How to get each one

**1. NHANES.** Go to https://wwwn.cdc.gov/nchs/nhanes/ and download the public files for each cycle you want. For Aug 2021–Aug 2023 these are `DEMO_L`, `BPXO_L` and `BPQ_L`; merge them on `SEQN`.
- **BP:** three Omron readings taken by certified examiners after 5 minutes of seated rest, in the file `BPXO_L` (confirmed today).
- **Awareness:** `BPQ020`, "ever told by a doctor or other health professional that you had hypertension". `BPQ150` asks about current medication.
- **Weights:** use the exam (MEC) weights and the design variables (`SDMVPSU`, `SDMVSTRA`).
- **Caveat:** NHANES stopped mercury (auscultatory) measurements after 2017–18. If you pool cycles across that change, you need to handle the device switch.
- **Use:** the "Awareness of having hypertension, diabetes and dyslipidaemia among US adults: NHANES 2011–2018" paper measures exactly your outcome.

**2. HRS.** Register for free at hrsdata.isr.umich.edu. Public data "only require you to register, log in, and access." Download the core health section (C) and physical measures section (I) for each wave, plus the tracker file for the weights. A cleaned, harmonised version is also on g2aging.org.
- **Who is measured:** since 2006 a random half of respondents gets the enhanced face-to-face interview each wave. That means each person is measured every 4 years.
- **Weights:** use the physical-measures weights.
- **2020 wave:** COVID disrupted the 2020 measurements, so skip it.
- **Caveat:** interviewers take the readings, not nurses. Say so in your methods.

**3. ELSA.** The ELSA site says "End User Licence level data are available to all via UKDS" (confirmed today). Log in through your institution (UK Access Management Federation) or request a username if you're outside the UK. Then download the ELSA series, including the nurse files.
- **Nurse visits:** only every other wave (2, 4, 6, 8/9, from memory). COVID affected later waves.
- **Wave 0:** this is the Health Survey for England, which also has nurse-measured BP for all ages.

**4. CHARLS.** The documentation says the data are "freely available to all bona fide researchers." You register at charls.pku.edu.cn/en and submit a request. The site timed out from here, so check the current form yourself.
- **Waves:** use 2011–2018. The 2020 wave apparently had no physical exam, but I couldn't confirm that.
- **Use:** there is a CHARLS paper on hypertension awareness ([PMC6480849](https://pmc.ncbi.nlm.nih.gov/articles/PMC6480849/)).

**5. LASI.** Fill in the request form at https://www.iipsindia.ac.in/content/lasi-data and attach "a valid identity proof." Access is "only granted for legitimate academic research purposes", and IIPS reviews requests "within 24 to 48 hours" (all confirmed today). With about 73,000 respondents it gives a high-undiagnosed contrast to the US and England.

**6. KNHANES.** Register on knhanes.kdca.go.kr, accept the data use policy and download the raw files. The registration pages are mostly in Korean, and I couldn't confirm that foreign researchers can sign up.

## Not recommended
- **NHIS and BRFSS:** self-reported hypertension only, so they fail your main requirement.
- **SHARE:** as far as I recall, no BP measurement in the main survey.
- **MHAS (Mexico):** BP was measured only in a subsample, from memory, and I couldn't confirm the site.
- **TILDA and CHMS:** they fit the measurement requirement, but access is slower. TILDA needs an application and is for non-commercial users only. CHMS can only be used inside a Canadian Research Data Centre.

## Two things for your methods
- **Who did the measuring differs:** examiners (NHANES), nurses (ELSA) and trained interviewers or field staff (HRS, CHARLS, LASI). Say this in your methods.
- **A single visit overestimates hypertension:** every survey here measures BP on one occasion, not over repeated visits. The usual approach is to define hypertension as a measured BP of 140/90 or higher, or currently taking BP medication. Then estimate unawareness as the share of those people who were never told they have it.

## Next step
Start with NHANES 2017–2020 or 2021–2023 today. Register for ELSA and either CHARLS or LASI this week, since both are free or quick. The Harmonized HRS, ELSA, CHARLS and LASI files on g2aging.org save a lot of variable matching.

## What I couldn't check
The HRS site blocked automated access and the CHARLS site timed out, so their details come from their documentation. The registry searches were mostly noise; the useful candidates came from known studies and the literature.

Sources: [HRS New User Guide 2025](https://hrs.isr.umich.edu/sites/default/files/new-user-guide/HRS-New-User-Guide-July-2025.pdf), [HRS 2006 Biomarker documentation](https://hrsonline.isr.umich.edu/modules/meta/bio2006/desc/biomkr06dd.pdf), [CHARLS baseline user guide](https://charls.charlsdata.com/Public/ashelf/public/uploads/document/2011-charls-wave1/application/CHARLS_nationalbaseline_users_guide.pdf), [Harmonized CHARLS](https://charls.charlsdata.com/Public/ashelf/public/uploads/document/harmonized_charls/application/Harmonized_CHARLS_D.pdf), [CHARLS awareness paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6480849/), [KNHANES profile](https://pmc.ncbi.nlm.nih.gov/articles/PMC4017741/), [KNHANES death-linkage paper](https://www.e-epih.org/journal/view.php?number=1269), [NHANES BPXO_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPXO_L.htm), [NHANES BPQ_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm), [ELSA access](https://www.elsa-project.ac.uk/accessing-elsa-data), [LASI data](https://www.iipsindia.ac.in/content/lasi-data), [TILDA access](https://tilda.tcd.ie/data/accessing-data/)

The full shortlist is in an interactive page you can filter and export an access plan from: `/private/tmp/e-Ltg1Tb/home/cwd/dataset-shortlist.html`