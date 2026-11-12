Here are the datasets that fit your criteria, in the order I'd consider them. This is from memory without live checks, so confirm fees, sample sizes and follow-up dates on each program's site before you plan around them.

## Best fits

| Dataset | Wrist device and protocol | Approx. N | Outcomes |
|---|---|---|---|
| **UK Biobank** | Axivity AX3, 7 days, 24 h/day, 2013–15 | ~100,000 | Hospital records (HES), death and cancer registries, partial primary care |
| **NHANES 2011–2014** | ActiGraph GT3X+, 7 days, with raw data released | ~7–8k adults with valid wear | Mortality only through the public-use linked file (to end of 2019) |
| **All of Us** | Participants' own Fitbits, often months to years of data | Tens of thousands | EHR diagnoses. Mortality is incomplete. |
| **MESA Sleep, MrOS Sleep, SOF** | Wrist actigraphy (Actiwatch or SleepWatch), 5–7 days | ~2,000, ~2,900 (older men), ~3,000 (older women) | Adjudicated CVD events and mortality, with long follow-up |

Other cohorts with wrist accelerometry include China Kadoorie Biobank, Whitehall II, and the Rotterdam Study. They are usually collaboration-based and harder for outside groups to get into, so I'd treat them as second-tier unless you already have a contact.

## What access involves

**UK Biobank**
- Your institution registers, and you submit an application through the UKB Access Management System. It asks for a scientific rationale and the data fields you need, including the accelerometer fields.
- Approval typically takes weeks. There is a tiered access fee, in the low thousands to about £9k plus VAT. Check the current schedule, since US universities are eligible but lower tiers may not apply to you.
- Data are accessed only inside the UKB Research Analysis Platform (DNAnexus), where you pay for compute and storage. Raw `.cwa` files are very large. Most people use the derived summary fields or the open-source `biobankAccelerometerAnalysis` pipeline.

**NHANES**
- The public-use accelerometer data and the NCHS linked mortality files are free downloads with no application.
- Restricted-use linkages, such as Medicare claims for hospitalizations, require a proposal to the NCHS Research Data Center. It is slower, and you work in a secure environment.
- This is the most directly comparable US population sample, but it only gives you mortality unless you go through the RDC.

**All of Us**
- You register your institution, sign a data use agreement, complete the program's training, and verify your identity. Access is free through the cloud-based Researcher Workbench.
- Fitbit data are in the Registered Tier. Check whether your analysis needs Controlled Tier data.
- Fitbit data are consumer-grade and not comparable to Axivity or ActiGraph counts. Coverage of outcomes depends on EHR linkage, so deaths and events outside the health system can be missed.

**NSRR (MESA, MrOS, SOF sleep data)**
- Create an account on sleepdata.org and sign a data use agreement. Actigraphy and many covariates are available quickly.
- Linked events and mortality sometimes sit outside NSRR. You may also need BioLINCC, or an ancillary-study proposal to the MESA or MrOS coordinating center.
- These cohorts are small by "a few thousand" standards. They are best as replication cohorts or for sleep-specific questions.

## Things that affect comparability
- **Devices differ.** Axivity gives ENMO-type metrics, ActiGraph gives counts or MIMS, and Actiwatch gives its own counts. Plan to harmonize, or to analyze each cohort separately and meta-analyze.
- **UK Biobank is not representative.** It is mostly white, healthier than average, and 40–69 years old at baseline. Pairing it with NHANES gives you a more representative US check.
- **Reverse causation.** Standard practice is to exclude the first 1–2 years of follow-up and adjust for baseline illness.

My suggestion is UK Biobank as the discovery dataset, NHANES for a US mortality replication, and MESA or MrOS for sleep-focused work in older adults. I can draft a UKB application rationale or a field list for any of these if that would help.