These are the datasets I'd consider, ordered by how well they fit your criteria. I checked each against web sources, and I flag below what I couldn't confirm.

## Primary candidates

### 1. UK Biobank (best fit for your design)
- **Wrist data:** About 103,700 participants wore an Axivity AX3 on the dominant wrist for 7 days at 100 Hz, in 2013–2015. Raw data is in field 90001, with quality-control fields for wear time and calibration.
- **Outcomes:** The cohort has linked hospital records and death registrations, and many published papers use the accelerometer subsample. I didn't open a page describing the linkage itself, so confirm the current follow-up dates in the Data Showcase.
- **Access:**
  - Register (free, reviewed in about 10 working days), then submit an application. Applications are approved for health-related research in the public interest, and your US university is fine.
  - After approval you have 90 days to pay the access fee and sign the Material Transfer Agreement (MTA). UK Biobank's FAQ gives an average of about 15 weeks from submission to data release.
  - The fee is cost-recovery. I found £500 + VAT for students (3 years of access). I couldn't find a current standard fee: the older £1,500 + VAT figure I saw is from 2020 and out of date. Check the current schedule.
  - Analysis takes place on the cloud Research Analysis Platform (run by DNAnexus), which has separate storage and compute charges. New users get £40 of credit.
- **Caveat:** The cohort is healthier and less diverse than the general population. This matters for generalisability but not for comparability with other wrist studies.

### 2. NHANES 2011–2014 (US, nationally representative)
- **Wrist data:** An ActiGraph GT3X+ was worn on the non-dominant wrist for 7 days at 80 Hz. About 12,600 participants across the two waves have accelerometer data, and the data were released in December 2020. Many of them are children, so you'd restrict to adults.
- **Outcomes:** Linkage is to the National Death Index, so you get mortality only, not hospital diagnoses. NCHS's public-use linked mortality files page says follow-up runs through 31 Dec 2022. A search summary said 2019, so check which version you're using.
- **Access:**
  - Accelerometer data and public-use mortality files are free downloads with no application. Minute-level derived data is also on PhysioNet.
  - Restricted-use mortality files (unaltered, including children) are available only through an NCHS Research Data Center with an approved project. You can't combine public-use and restricted-use files inside the RDC.
- **Caveat:** The device and wrist differ from UK Biobank (ActiGraph on the non-dominant wrist, versus Axivity on the dominant wrist). That is a comparability issue if you pool or replicate across the two.

### 3. All of Us (US, with linked EHR)
- **Wrist data:** Fitbit data covers participants who chose to share it. It comes as summary and minute-level tables derived from Fitbit's proprietary algorithms, and raw accelerometry is not provided. That limits comparability with raw-signal wrist studies like UK Biobank and NHANES.
- **Outcomes:** The linked EHR gives diagnoses. Registered Tier Fitbit data is date-shifted.
- **Access:**
  - Your institution must sign a Data Use and Registration Agreement (DURA).
  - You then register, verify your identity, complete Responsible Conduct of Research training, and attest to a code of conduct.
  - There is no project pre-approval, and the data access is free (you may pay for compute and storage).
  - A recent FAQ describes a move to a new Verily-based platform, so check the current onboarding.
- **Caveat:** I'd treat this as a supplementary or sensitivity dataset, because it uses consumer devices with proprietary metrics and has a self-selected wearer subsample. I didn't confirm sample size or Fitbit wear duration. Check the Nature Medicine wearables paper for those.

## Smaller wrist-actigraphy cohorts (older adults)
These are likely under "a few thousand" and have more restricted access, so I'd use them for replication.

- **Study of Osteoporotic Fractures (SOF):** About 3,676 women were eligible for wrist actigraphy at Exam 8 (2002–2003), and a published SOF analysis linked circadian rhythms to mortality. Sleep-visit data are on the National Sleep Research Resource (NSRR), which has a "Request Data Access" option. SOF data are also available through SOF Online and NIA's AgingResearchBiobank. I didn't verify whether the NSRR release includes the raw actigraphy or only summaries.
- **MrOS (men only, N≈2,600):** The Sleepwatch-O is a wrist actigraph. NSRR hosts the polysomnography data but not the actigraphy. Actigraphy requests go to the MrOS sleep study investigators (California Pacific Medical Center Research Institute) or the SOF/MrOS Coordinating Center.
- **Whitehall II (UK):** A paper used wrist accelerometry with mortality follow-up to October 2023. Access is through the UCL data sharing portal. A preprint says the data can't be shared publicly because of ethics constraints, so expect a controlled application. I didn't check the portal's requirements.

## What I couldn't verify
- I couldn't open UK Biobank's own application page (the site returned a 403), so the fee and timeline details come from its FAQ and search summaries.
- I found nothing on the Women's Health Study. The Women's Health Initiative OPACH study used hip-worn devices, so it doesn't meet your wrist requirement.

## Suggested approach
Use UK Biobank as your main analysis, since it is the largest dataset and has hospital and death linkage. Use NHANES for a free US replication, with the caveat that it covers mortality only and uses a different device and wrist. Add SOF or MrOS if you want an older-adult cohort and can wait for controlled access. I can look further into any one of these, such as UK Biobank's current fee schedule or the SOF/MrOS proposal process.

Sources:
- [Wearable accelerometer-derived physical activity and incident disease (npj Digital Medicine)](https://www.nature.com/articles/s41746-022-00676-9)
- [UK Biobank Physical Activity Monitor documentation](https://biobank.ndph.ox.ac.uk/ukb/ukb/docs/PhysicalActivityMonitor.pdf)
- [UK Biobank: Applying and accessing data FAQ](https://community.ukbiobank.ac.uk/hc/en-gb/articles/28002689502237-Applying-to-UK-Biobank-and-accessing-data-FAQ)
- [UK Biobank Access Procedures](https://www.ukbiobank.ac.uk/wp-content/uploads/2026/05/Access-procedures.pdf)
- [How much will it cost me to use the UKB-RAP?](https://community.ukbiobank.ac.uk/hc/en-gb/articles/19968104769309-How-much-will-it-cost-me-to-use-the-UKB-RAP)
- [NHANES 2011–2014: Objective Physical Activity and all-cause mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/)
- [NHANES 2011-2012 Physical Activity Monitor raw data documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAX80_G.htm)
- [PhysioNet minute-level NHANES data](https://physionet.org/content/minute-level-step-count-nhanes/1.0.1/)
- [NCHS public-use linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm)
- [All of Us wearables dataset (Nature Medicine)](https://www.nature.com/articles/s41591-026-04352-3)
- [All of Us Researcher Workbench FAQ](https://support.researchallofus.org/hc/en-us/articles/52861503885460-Frequently-Asked-Questions)
- [How Fitbit data are being made available in All of Us](https://www.researchgate.net/publication/366766944_How_Fitbit_data_are_being_made_available_to_registered_researchers_in_All_of_Us_Research_Program)
- [SOF circadian activity rhythms and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC2938873/)
- [NSRR Study of Osteoporotic Fractures](https://sleepdata.org/datasets/sof)
- [NSRR MrOS Sleep Study](https://sleepdata.org/datasets/mros)
- [NSRR actigraphy forum](https://sleepdata.org/forum/actigraphy)
- [AI-driven sleep staging from actigraphy and heart rate (MrOS actigraphy access)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10191307/)
- [Accelerometer epoch summary measure and mortality in Whitehall II and UK Biobank](https://www.nature.com/articles/s41598-025-30237-5)