The datasets below are listed from best to weakest fit. This is from my own knowledge, not a live check, so confirm current fees, sample sizes and policies on each portal before you plan around them.

## Best fits

| Dataset | Wrist device and wear | N | Outcomes |
|---|---|---|---|
| **UK Biobank** | Axivity AX3 (raw), 7 days, 2013–15 | about 100,000 | Hospital records, death and cancer registries, and some primary care. Follow-up of 10 or more years. |
| **NHANES 2011–14** | ActiGraph GT3X+ (raw), 7 days, 24 hours a day | about 12,000–14,000 with usable data (adults are a subset) | Mortality through the NDI linkage. Medicare/hospitalization linkage is restricted-use. |
| **China Kadoorie Biobank** | Axivity AX3 on a subsample, 7 days | tens of thousands (check the current figure) | Death registry, disease registries and insurance records |
| **All of Us** | Participants' own Fitbits (consumer device) | tens of thousands | EHR diagnoses. Death data are less complete. |
| **NSRR cohorts (MrOS, SOF, MESA Sleep)** | Wrist actigraphy (Sleepwatch-O and Actiwatch), about 5–7 nights | about 2,000–3,000 each | Mortality, fractures and CVD events, depending on the cohort |

## What access involves

**UK Biobank**
- A US university is eligible.
- You register on the Access Management System, and your institution signs a Material Transfer Agreement.
- You submit an application describing your aims and the data fields you need. Approval usually takes weeks.
- You pay a tiered access fee, which was roughly £9,000 plus VAT for 3 years when I last knew. Check the current tier.
- Analysis happens in their cloud Research Analysis Platform (DNAnexus), so you can't download the data. Budget for compute costs.
- The raw accelerometer files are available. Many people use the derived phenotypes or the Oxford `biobankAccelerometerAnalysis` pipeline.

**NHANES**
- The public data are free, with no application. This includes the 2011–14 raw wrist data and the public-use linked mortality files.
- Public-use mortality is coarser and has fewer covariates. Medicare linkage or detailed cause of death needs an application to the NCHS Research Data Center. That takes months, has fees, and requires working in a secure environment.
- NHANES 2003–06 used hip placement, so it doesn't meet your wrist requirement.
- Follow-up is shorter than in UK Biobank, and most deaths are all-cause.

**China Kadoorie Biobank**
- You submit a proposal to the CKB data access committee. International researchers can apply, and approval takes some weeks to months.
- Because it uses the same Axivity AX3 as UK Biobank, it is a good replication cohort. It also adds a very different population.

**All of Us**
- Access is free through the Researcher Workbench. Your institution needs a Data Use and Registration Agreement, and you need to complete identity verification and the required training to reach controlled-tier data.
- You work in the cloud environment and can't download participant-level data.
- Consumer Fitbit data (steps, heart rate, sleep) are not research-grade accelerometry, so they are not directly comparable with UK Biobank or NHANES. Wear is also self-selected.

**NSRR and the older-adult cohorts**
- NSRR hosts MrOS Sleep, SOF, MESA Sleep and others. You register, accept a data use agreement and request each dataset. Approval is typically quick and free.
- Public NSRR releases may not include all follow-up outcomes. For full event data you may need a separate request to the cohort, for example MrOS through its coordinating center, or MESA through its ancillary-study or BioLINCC route.
- These cohorts are small. The devices produce count-based output rather than raw data, so they are harder to harmonize with raw-data cohorts.

## Smaller or less certain options
- **Whitehall II** had an accelerometer substudy of about 4,000 people. I believe it used a wrist-worn GENEActiv, but verify that. Access is by proposal to UCL.
- **ARIC** has later visits with accelerometry, but I'm not sure of the placement for each visit. Verify before relying on it.
- **Excluded for hip placement:** the Women's Health Study, WHI OPACH, HCHS/SOL and NHANES 2003–06.

## Suggested design
Use UK Biobank as the discovery cohort, since it has the largest sample, the longest follow-up and the richest outcome linkage. Replicate in NHANES 2011–14, which is free and representative of the US, and in CKB, which uses the same device. Add MrOS or SOF if you want older adults or sleep-focused analyses.

Start the UK Biobank application early. Its timeline and fee are the main cost and delay, and you can work with NHANES while you wait.

I can look up current fees and sample sizes on the portals if you'd like. Those are the facts most likely to have changed.