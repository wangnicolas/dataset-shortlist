## Main options

**1. UK Biobank, the largest option**
- **Data:** About 100,000 adults wore an Axivity AX3 on the dominant wrist for 7 days around 2013–2015. You get raw 100 Hz data plus derived summaries (ENMO, activity classes, sleep).
- **Outcomes:** Linked hospital admissions (HES and its Scottish and Welsh equivalents), cancer registry, death registry, and primary care records for part of the cohort. Follow-up now exceeds 10 years.
- **Access:**
  - Register as a researcher on the UK Biobank Access Management System, then submit a project application for health-related research.
  - After approval you sign a Material Transfer Agreement through your university and pay an access fee. It is a few thousand pounds, with discounts for students and some institutions; check the current rate.
  - Analysis now happens almost entirely on the cloud Research Analysis Platform (DNAnexus), not by download. You pay compute and storage costs there, which add up when processing raw accelerometer files.
  - US universities apply routinely. Expect weeks to a couple of months.

**2. NHANES 2011–2014, free and US-representative**
- **Data:** ActiGraph GT3X+ worn on the non-dominant wrist, 24 hours a day for 7 days. There are about 14,000 participants of all ages, roughly 9,000 adults. Public files contain minute-level MIMS summaries plus wear and sleep flags, and raw 80 Hz files have also been released.
- **Outcomes:**
  - The NCHS Public-Use Linked Mortality Files (National Death Index) give vital status and broad cause of death. Current follow-up runs through 2019.
  - The restricted mortality files, plus Medicare (CMS) linkage, are available only through an NCHS/CDC Research Data Center.
- **Access:**
  - The public data and mortality files are free downloads with no application.
  - The restricted data require an RDC proposal and, usually, work in a secure enclave. They allow finer cause of death, exact dates, and claims data that approximate disease incidence.
- **Caution:** NHANES 2003–2006 used hip-worn devices, so only the 2011–2014 cycles fit your wrist requirement.

**3. All of Us Research Program, consumer trackers linked to medical records**
- **Data:** Fitbit data from participants' own devices: steps, heart rate, sleep stages and activity minutes. Recent releases cover tens of thousands of participants, often with months to years of data, linked to EHR diagnoses, procedures, labs and some death data.
- **Access:**
  - Your institution signs a Data Use and Registration Agreement; most large US universities already have.
  - You register with an identity check and complete responsible-conduct training.
  - The Registered Tier is available quickly. The Controlled Tier is usually needed for this kind of work and requires extra training.
  - All analysis happens on the cloud Researcher Workbench. New users get starter credits, then pay compute costs. There is no project-level scientific review, so access is fast, often days.
- **Caveats for comparability:**
  - You get proprietary Fitbit summaries, not raw accelerometry, so they don't map directly onto ENMO or MIMS.
  - Participants are self-selected device owners.
  - Wear patterns vary a lot between people.
  - Outcomes depend on how complete each person's EHR is.

## Smaller cohorts with stronger outcome adjudication

| Cohort | Wrist device and size | Outcomes | Access |
|---|---|---|---|
| **Whitehall II** (UK civil servants) | GENEActiv, non-dominant wrist, 9 days, about 4,000 adults (2012–13) | NHS hospital records, mortality, dementia | Proposal to the Whitehall II team at UCL; reviewed, sometimes with collaboration expected |
| **MrOS Sleep** (older US men) | Wrist actigraph, about 5 days, about 3,000 men | Adjudicated mortality, CVD, fractures | Wrist actigraphy via the National Sleep Research Resource (NSRR, sleepdata.org) under a short DUA; extra follow-up outcomes from the MrOS coordinating center |
| **SOF** (older US women) | Wrist actigraph, about 3 days, about 3,000 women | Mortality, fractures, cognitive decline | NSRR / SOF Online |
| **MESA Sleep** | Actiwatch Spectrum, wrist, 7 days, about 2,000 adults | Adjudicated CVD events, mortality | Actigraphy via NSRR; events via BioLINCC or the MESA coordinating center, which require IRB approval and a DUA |
| **HCHS/SOL Sueño** | Actiwatch, wrist, about 2,000 Hispanic/Latino adults | Ongoing cohort follow-up | NSRR plus the HCHS/SOL coordinating center |
| **Rotterdam Study** | Wrist actigraphy (GENEActiv in later rounds), a few thousand adults | GP records, hospital records, mortality | Collaboration with Erasmus MC, not an open application |
| **China Kadoorie Biobank** | Axivity on the wrist in a recent resurvey subsample of about 20,000 or more | Hospital insurance and death registry linkage | CKB data access portal. Check whether the accelerometer data have been released yet; my information may be out of date |

The MrOS, SOF and MESA devices are sleep-focused actigraphs that record proprietary counts. They work well for sleep and rest-activity rhythms, but are harder to harmonize with raw-data metrics.

## Exclusions (not wrist-worn)

- **Hip:** Women's Health Study, OPACH, Tromsø, NAKO, and NHANES 2003–06.
- **Thigh or back:** HUNT and the 1970 British Cohort Study.
- **Chest:** Fenland.

## Practical suggestions

- **Pairing:** A common design is UK Biobank for discovery and NHANES 2011–14 for US replication. Both are 24-hour wrist protocols with raw data available. They differ in device (Axivity vs ActiGraph), wrist (dominant vs non-dominant) and metric (ENMO vs MIMS). Processing raw data from both with the same pipeline, such as GGIR or the Oxford `stepcount`/`biobankAccelerometerAnalysis` tools, improves comparability.
- **Order of applications:** Start with NHANES public data and NSRR, which take days. Run UK Biobank and All of Us applications in parallel. File an RDC proposal only if you need restricted NHANES mortality or Medicare data.
- **Ethics:** Your university IRB will usually classify secondary analysis of these de-identified data as exempt or not human-subjects research. Some providers, such as NSRR and BioLINCC, still require that determination letter.

Fees, sample counts and follow-up dates change between releases, so check each provider's current access pages before budgeting.