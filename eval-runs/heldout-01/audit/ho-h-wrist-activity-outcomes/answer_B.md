Here are the datasets I'd consider, roughly in order of fit. This is from memory, not live-checked, so confirm current fees, wait times and data versions on each program's site before you plan around them.

## Strongest fits

**1. UK Biobank**
- **Device:** Axivity AX3 on the dominant wrist, worn for 7 days. About 100,000 participants wore it in 2013–15, and a repeat-wear subset exists.
- **Outcomes:** Linked hospital inpatient records (HES), death registry, cancer registry, and partial primary care data. Follow-up now runs about 10 years or more.
- **Access:**
  - A US university is eligible. Your institution must be registered, and you apply through the online Access Management System with a short research-question description.
  - You pay a tiered access fee, historically in the low-to-mid thousands of GBP for a multi-year license. Check the current schedule.
  - Analysis must take place in the UK Biobank Research Analysis Platform (DNAnexus cloud), so you can't download individual-level data. You pay cloud compute costs.
  - Approval usually takes a few weeks. The raw accelerometer files and derived metrics are both available.
- **Caveats:** Participants are healthier and older than the general population (healthy-volunteer bias), and mostly of White European ancestry.

**2. NHANES 2011–2014**
- **Device:** ActiGraph GT3X+ on the wrist, worn 24 hours a day for 7 days. Several thousand adults have valid data. This is the only US-representative option here.
- **Outcomes:** Linked National Death Index mortality, with follow-up through 2019 in the public-use files.
- **Access:**
  - The accelerometer data and public-use linked mortality files are free to download with no application.
  - Cause-specific detail, other covariate linkages, and CMS Medicare/Medicaid hospital linkage require a proposal to the NCHS Research Data Center. That means a fee, a secure-site visit or remote access, and a longer timeline.
- **Caveats:** Follow-up is shorter, with fewer deaths. Hospital outcomes require the restricted route.

## Good for sleep and older-adult questions (all wrist actigraphy)

Each of these has a few thousand participants or fewer, so check your power for your outcome.

- **MrOS Sleep Study:** About 3,000 older men, with mortality and fracture follow-up.
- **Study of Osteoporotic Fractures (SOF):** About 3,000 older women, with mortality follow-up.
- **MESA Sleep:** About 2,000 adults with a 7-day Actiwatch, plus cardiovascular event and mortality follow-up.

**Access:** These are mostly distributed through the **National Sleep Research Resource (NSRR)**. You register, sign a data use agreement, and request datasets. It's free, and approval is often quick. Outcomes and event data can sit with the parent studies (MrOS Online, SOF, MESA coordinating center), which may need a separate request or proposal.

## Consumer-tracker option

**All of Us Research Program**
- **Device:** Fitbit wrist trackers, with data from tens of thousands of participants who linked their accounts. The data are consumer-grade and not raw acceleration, so they're less comparable with research-grade wrist accelerometers.
- **Outcomes:** EHR-derived diagnoses and encounters. Death data are more limited.
- **Access:** Free. Your institution signs a data use agreement, and you complete researcher registration, identity verification and ethics training. You work in the cloud Researcher Workbench.

## Worth checking

- **China Kadoorie Biobank:** I believe a resurvey subset wore wrist Axivity devices, with health-insurance and death-registry linkage. Access is by application, but confirm the sample size and international access terms.
- **Our Future Health (UK):** It may be adding wearable data. Check its status.

## Practical advice

- If wrist comparability is the priority, start with **UK Biobank**. It has the best combination of size, wrist-worn research-grade devices, and hospital and death linkage.
- Add **NHANES** as a US-population replication, since the free public files let you start immediately.
- Account for device differences (Axivity vs. ActiGraph vs. Actiwatch). Metrics such as ENMO, MIMS and activity counts aren't directly interchangeable, so plan harmonization early.
- Before applying anywhere, get IRB determination, since this is secondary analysis, and your sponsored-programs office, since several of these require institutional signatures.

I can look up the current fees and application steps for any of these, or help draft the UK Biobank application's research-question summary.