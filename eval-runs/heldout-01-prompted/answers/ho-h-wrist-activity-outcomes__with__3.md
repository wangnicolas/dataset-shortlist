I searched for each dataset below and confirmed it exists. I could only read the access pages for NHANES and the UK Biobank fee summaries (via search results). I couldn't open the UK Biobank application page (it returned a 403) or the NSRR MrOS page (certificate error), so check those two yourself.

## Best fits

**1. UK Biobank (UKB)**
- **What it is:** From 2013 to 2015, about 103,700 participants wore an Axivity AX3 on the dominant wrist for up to 7 days, and about 96,600 have valid data. Outcomes come from linked hospital and death records.
- **Access:** Apply through the UKB Research Analysis Platform (RAP). Per the fee summaries, the cost is £3,000 for Tier 1 for 3 years, or £6,000 for Tier 2. Whole-genome and imaging data need Tier 3 at £9,000. International researchers pay the same rates. The average time from application to data release is about 15 weeks. After approval you have 90 days to pay and sign the Material Transfer Agreement. RAP compute and storage cost extra, and each account starts with £40 of credit.
- **Caveat:** The search results say new applications are currently paused while the RAP is changed, with reopening expected in late 2026. Check the status first. If you already have access through a collaborator, that may be quicker.

**2. NHANES 2011–2014 with linked mortality (public)**
- **What it is:** Participants aged 3 and over wore an ActiGraph GT3X+ on the non-dominant wrist for 9 days, sampled at 80 Hz. There are about 7 full days of usable data, and the raw and minute-level data (MIMS units) were released in 2020. The sample is nationally representative of the US.
- **Access:** The accelerometer data are free to download from CDC. The public-use linked mortality files are also free and give vital status, follow-up time and cause of death. Some follow-up times and causes are synthetically altered to protect privacy.
- **Limits:** You get mortality only, not hospital records. The CDC page I read lists the public files as covering NHANES 1999–2018, with a 2022 update on the page. The page didn't say which follow-up end date applies to which file, so check that. For unaltered data you need an NCHS Research Data Center application, and you can't combine public and restricted files in the RDC.
- **Comparability:** The device is wrist-worn but a different brand and placement side from UKB, so harmonise metrics carefully.

**3. All of Us Research Program**
- **What it is:** Participants who shared Fitbit data total about 59,000. About 25,900 to 36,600 of them also have linked EHR data, depending on the data release.
- **Access:** Register as a researcher, complete the Responsible Conduct of Research training, and for individual-level data complete the extra Controlled Tier steps. Your institution must have a data use agreement. All analysis runs inside the cloud Researcher Workbench, and the Data Browser shows only aggregate data.
- **Caveats:** This is consumer-device data collected over years, not a fixed one-week protocol. The sources I found don't say that all Fitbit data are wrist-worn, so check the device types. It also reflects self-selected users, and the outcomes are EHR diagnoses rather than registry-grade death records.

## Smaller cohorts (a few thousand people, older adults)

| Cohort | Wrist device and sample | Outcome | Access |
|---|---|---|---|
| **Whitehall II** accelerometer sub-study | About 3,991 participants; wrist-worn | Mortality to 2021 | UCL data-sharing portal; application required, and data can't be shared publicly |
| **MrOS Sleep Study** | 3,135 older men; wrist SleepWatch-O, 3–5 days | Mortality, CVD, falls, fractures | NSRR doesn't host the actigraphy, so the search results say to request it from the MrOS investigators |
| **Study of Osteoporotic Fractures (SOF)** | About 3,000 older women; wrist actigraphy | Mortality, fractures | NSRR "Request Data Access" or NIA AgingResearchBiobank (I couldn't confirm which hosts the actigraphy) |
| **Rotterdam Study** | About 1,700 participants; actigraphy | Mortality | Request through the Rotterdam data management team (datamanagement.ergo@erasmusmc.nl) |

I did not confirm the Rotterdam device placement, so check it. WHI OPACH is hip-worn, so it doesn't meet your wrist requirement. The Women's Health Study turned up nothing in my search, so I can't recommend it.

## Suggested order
1. Start with NHANES, since it needs no application and lets you build your pipeline.
2. Pursue UKB once applications reopen. It has the scale, the hospital and death linkage, and the most comparable wrist-worn literature.
3. Use Whitehall II or MrOS as replication cohorts, or All of Us if you want EHR outcomes.

Sources:
- [UK Biobank accelerometer study (Doherty et al., PLoS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0169649)
- [UK Biobank accelerometer documentation](https://biobank.ndph.ox.ac.uk/ukb/ukb/docs/PhysicalActivityMonitor.pdf)
- [UK Biobank apply for access](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/)
- [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)
- [UK Biobank access FAQ](https://community.ukbiobank.ac.uk/hc/en-gb/articles/28002689502237-Applying-to-UK-Biobank-and-accessing-data-FAQ)
- [NCHS public-use linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm)
- [NHANES wrist accelerometry and mortality (PMC11402588)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/)
- [NHANES step-count comparison (arXiv)](https://arxiv.org/pdf/2410.11040)
- [All of Us Fitbit resources](https://support.researchallofus.org/hc/en-us/articles/20281023493908-Overview-and-resources-to-aid-using-Fitbit-data-available-on-All-of-Us-Researcher-Workbench)
- [All of Us Fitbit Data Browser](https://databrowser.researchallofus.org/fitbit)
- [All of Us wearables dataset (Nature Medicine)](https://www.nature.com/articles/s41591-026-04352-3)
- [Whitehall II and UK Biobank (Scientific Reports)](https://www.nature.com/articles/s41598-025-30237-5)
- [Whitehall II mortality model (eClinicalMedicine)](https://www.thelancet.com/journals/eclinm/article/PIIS2589-5370(22)00502-8/fulltext)
- [MrOS rest/activity rhythms and mortality (PubMed)](https://pubmed.ncbi.nlm.nih.gov/20370475)
- [MrOS actigraphy access (PLoS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0285703)
- [NSRR MrOS](https://sleepdata.org/datasets/mros)
- [NSRR SOF](https://sleepdata.org/datasets/sof)
- [SOF actigraphy and mortality (ResearchGate)](https://www.researchgate.net/publication/269415396_Fragmentation_and_Stability_of_Circadian_Activity_Rhythms_Predict_Mortality)