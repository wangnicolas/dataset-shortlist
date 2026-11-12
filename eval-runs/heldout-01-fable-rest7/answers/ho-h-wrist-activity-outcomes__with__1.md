There are ten datasets worth considering, but only one (NHANES 2011–2014) is downloadable today, and the obvious first choice, UK Biobank, is reported closed to new applications right now. All facts below were checked on 12 November 2026 unless marked "from memory".

## What I assumed you need

- **R1 (must):** device worn on the wrist for several days to a week or longer, in daily life.
- **R2 (must):** at least a few thousand adults.
- **R3 (must):** follow-up outcomes after the wear period, death at minimum.
- **R4 (nice):** disease outcomes from hospital records or diagnoses, not only death.
- **R5 (nice):** raw or high-resolution acceleration, since that is what makes wrist studies comparable. This is my assumption.
- **R6 (must):** obtainable by a US university researcher; applications and waiting are acceptable.

## Shortlist

| # | Dataset | Access | Licence / terms | Size (wrist data) | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES 2011–2014 + NCHS linked mortality | Direct download, minutes | US federal public-use data | 14,693 people, about 8,600 adults | Partial: death only | Today |
| 2 | All of Us (Fitbit + health records) | Institutional agreement; days if your university has one, otherwise weeks | Data Use and Registration Agreement; analysis only in the cloud Workbench | 68,000+ with Fitbit data | Strong, but consumer tracker | Today |
| 3 | UK Biobank accelerometer study | Application, fee, secure platform; new applications reported closed, so months | Material transfer agreement | 103,617 | Strong | Status from search results; official pages blocked |
| 4 | MrOS Sleep Study (older men) | Free account plus data use agreement, days | Data use agreement | about 3,050 | Partial: about 5 nights, old device | Today |
| 5 | Study of Osteoporotic Fractures (older women) | Free account plus data use agreement, days | Data use agreement | about 3,000 | Partial: about 4 nights | Today |
| 6 | Whitehall II (UK) | Application via Dementias Platform UK plus study committee, months | Data access agreement | 4,204 | Strong | Search summaries; page blocked |
| 7 | Northern Finland Birth Cohort 1966 | Collaboration request with University of Oulu, months | Study agreement | 5,481 | Partial: no raw data | Today |
| 8 | MESA Sleep (US) | Two applications (sleep data, then events), weeks | Data use agreements; commercial use tiered | 2,237 | Partial: linkage unconfirmed | Events page today; sleep-data page blocked |
| 9 | China Kadoorie Biobank resurvey | Application to access committee; timing unknown | Data access agreement | 21,897 | Partial: release unconfirmed | Paper today; access page blocked |
| 10 | CoLaus\|PsyCoLaus (Switzerland) | Proposal to study data centre, months | Data transfer agreement | about 2,600–2,700 | Partial | Today, from papers |

## Details

**1. NHANES 2011–2014 wrist accelerometry + public-use linked mortality** ([accelerometer file](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm), [mortality files](https://www.cdc.gov/nchs/linked-data/mortality-files/))
- **Contents:** ActiGraph GT3X+ on the non-dominant wrist for 9 calendar days, in a US-representative sample, with minute, hour and day summaries. Raw 80 Hz files are also public (from memory).
- **Outcomes:** death only. Public-use mortality follow-up ends 31 December 2019, and cause of death may be perturbed for some records.
- **Access:** download both file sets and merge on the participant ID. Follow-up through 2022 and unaltered cause of death need a proposal to the NCHS Research Data Center (fee, weeks to months).
- **Extra:** derived minute-level step counts are on [PhysioNet](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/) under CC0.
- **Limits:** death counts are modest (one paper reports 582 deaths among 3,032 adults aged 50+).
- **Used by:** [activity as the strongest mortality predictor](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/); [diurnal activity and sleep patterns vs mortality](https://link.springer.com/article/10.1186/s12966-024-01673-9).

**2. All of Us Research Program** ([register](https://www.researchallofus.org/register/))
- **Contents:** Fitbit steps, heart rate and sleep, often over months or years, linked to health record diagnoses. Version 8 had 59,018 Fitbit participants, 36,614 of them with health records; version 9 has more than 68,000.
- **Access:** the page states "Only researchers whose institutions have signed a DURA may access the Researcher Workbench." Check the registered institutions list, then create an account, verify your identity, complete the training and sign the code of conduct.
- **Tiers:** the Registered Tier includes Fitbit and health record data with shifted dates. Cause of death needs the Controlled Tier.
- **Limits:** no raw acceleration; mostly participants' own devices, so a self-selected group; deaths come from health records and staff reports, and I found no National Death Index linkage. Data cannot leave the Workbench, and compute is billed.
- **Used by:** [step counts and chronic disease risk](https://www.nature.com/articles/s41591-022-02012-w); [the wearables dataset description](https://www.nature.com/articles/s41591-026-04352-3).

**3. UK Biobank** ([accelerometer category](https://biobank.ndph.ox.ac.uk/showcase/label.cgi?id=1008), [apply](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/))
- **Contents:** Axivity AX3 on the wrist for 7 days (2013–2015) in 103,617 adults, linked to hospital, cancer and death records. This is the dataset other wrist studies compare against.
- **Current status:** search results quoting UK Biobank's own pages say all researcher access was shut on 23 April 2026 after exported data were found for sale. New applications remain closed, with a "late 2026" target and no confirmed date. I could not open the official pages myself.
- **Access when open:** free registration, project application (about 10 working days' review), institutional agreement, then analysis on its Research Analysis Platform with downloads blocked.
- **Fee:** £3,000 plus VAT for three years at the lowest tier, according to a third-party summary rather than UK Biobank's fees page.
- **Limits:** very heavily used, so simple activity–outcome questions are mostly published.
- **Used by:** [methods paper](https://doi.org/10.1371/journal.pone.0169649); [sleep regularity and mortality](https://doi.org/10.1093/sleep/zsad253); [activity and 697 incident diseases](https://doi.org/10.1038/s41746-022-00676-9).

**4 and 5. MrOS and SOF** ([MrOS Online](https://mrosonline.ucsf.edu/), [SOF Online](https://sofonline.ucsf.edu/))
- **Contents:** SleepWatch-O actigraph on the non-dominant wrist in about 3,050 men (mean age 76, 5.2 nights) and about 3,000 women (mean age 84, 4.1 nights).
- **Outcomes:** mortality (mean follow-up 12.1 and 5.4 years), plus adjudicated fractures and cardiovascular events (from memory).
- **Access:** both sites state "You must have an account and accept the terms of a Data Use Agreement before you can download or explore clinical data."
- **Limits:** old device with count-based output, short recordings and elderly single-sex cohorts.
- **Used by:** [rest-activity rhythms and mortality in MrOS](https://pubmed.ncbi.nlm.nih.gov/20370475); [sleep duration phenotypes and mortality in both](https://pmc.ncbi.nlm.nih.gov/articles/PMC13698916).

**6. Whitehall II** ([data sharing page](https://www.ucl.ac.uk/brain-sciences/psychiatry/research/mental-health-older-people/projects/whitehall-ii/data-sharing))
- **Contents:** GENEActiv on the non-dominant wrist for nine days in 2012–2013, 4,204 readable files, raw data at 85.7 Hz.
- **Outcomes:** mortality follow-up to August 2024 and incident dementia in published work.
- **Access:** apply through the Dementias Platform UK portal; its staff triage the request, then the Whitehall II data sharing committee reviews it.
- **To confirm:** whether raw files are released, and whether non-UK applicants are eligible.
- **Used by:** [sleep duration and dementia](https://www.nature.com/articles/s41467-021-22354-2); [walking cadence and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC13695056).

**7. Northern Finland Birth Cohort 1966** ([programme page](https://www.oulu.fi/en/university/faculties-and-units/faculty-medicine/northern-finland-birth-cohorts-and-arctic-biobank))
- **Contents:** Polar Active on the non-dominant wrist for 14 days at age 46, 5,481 valid recordings.
- **Outcomes:** national hospital and death registers, with follow-up to the end of 2023.
- **Access:** data "can be requested for research collaboration projects with University of Oulu", so you need a local collaborator and a material request.
- **Limits:** single birth year, and the device gives activity levels, not raw acceleration.
- **Used by:** [sleep timing irregularity and cardiac events](https://link.springer.com/article/10.1186/s12872-026-05762-4).

**8. MESA Sleep** ([sleep data](https://sleepdata.org/datasets/mesa), [events data](https://biolincc.nhlbi.nih.gov/studies/mesa/))
- **Contents:** Actiwatch Spectrum on the wrist for 7 days in 2,237 multi-ethnic US adults, as 30-second counts.
- **Outcomes:** held separately; the NHLBI repository offers "events data updated through calendar year 2020".
- **Access:** a data access agreement with the National Sleep Research Resource, plus a separate request to the NHLBI repository.
- **To confirm before applying:** whether the two releases share a participant identifier. Ask the MESA Coordinating Center.

**9. China Kadoorie Biobank** ([paper](https://doi.org/10.1186/s12966-023-01537-8))
- **Contents:** the same Axivity device and 7-day protocol as UK Biobank, in 21,897 adults in 2020–2021.
- **Access:** the paper says "Data are available upon reasonable request" and points to the biobank's data access page, which I could not open.
- **Limits:** whether the accelerometer data are released to outside researchers is unconfirmed, and follow-up since wear is short.

**10. CoLaus|PsyCoLaus** ([study site](https://www.colaus-psycolaus.ch/))
- **Contents:** GENEActiv on the right wrist for 14 days in about 2,600–2,700 adults, with a repeat measurement in 2018–2021.
- **Outcomes:** adjudicated cardiovascular events; I found no accelerometry–mortality paper.
- **Access:** e-mail a proposal to research.colaus@chuv.ch; the data are not posted publicly.
- **Used by:** [activity patterns and cardiovascular events](https://pmc.ncbi.nlm.nih.gov/articles/PMC11497381/).

## Known, not confirmed

- **UK Biobank status and fees:** from search summaries of its pages; the pages refused my tools. Check the apply page and researcher Community site.
- **Whitehall II and Dementias Platform UK steps:** both sites blocked automated reading; details are from search summaries and memory.
- **Sleep-data repository pages (MESA, MrOS, SOF):** my tools could not verify sleepdata.org's certificate; open it in a browser.
- **Seniors-ENRICA-2 (Spain), PREDIMED-Plus and MIPACT (Michigan, Apple Watch with health records):** recalled as possible fits; I found no access information.

## Not recommended, and why

- **Rush Memory and Aging Project:** wrist-worn with dementia and death outcomes, but analytic samples are about 700–1,000. The request site was unreachable today.
- **Rotterdam Study:** about 2,000 with mostly older wrist actigraphs; no release, only requests to the study management team.
- **NHANES 2003–2006, Tromsø7, German National Cohort:** hip-worn. Women's Health Study, WHI OPACH and REGARDS are also hip-worn (from memory).
- **HUNT4:** thigh and lower-back sensors.
- **BLSA, HANDLS, FinHealth 2017:** wrist-worn but under 1,000 participants each.

## What I could not find

- No openly downloadable dataset combines wrist accelerometry with hospital or diagnosis follow-up.
- Registry searches (OpenAIRE, Zenodo, DataCite, PhysioNet, Hugging Face) returned almost only small device-validation datasets; the cohorts above came from memory, the literature and project sites.

## Next step

1. Start on NHANES now to build your processing pipeline and mortality models.
2. Check whether your university is on the All of Us registered institutions list; if so, you can have diagnosis-linked data within days.
3. Watch for UK Biobank to reopen, and meanwhile send the Whitehall II application, the closest raw-data wrist cohort with long follow-up.
4. Before using any restricted dataset, check its agreement on third-party services, including online AI tools.

The interactive shortlist, with filters and an exportable access plan, is at `/private/tmp/e-PVHKEC/home/cwd/dataset-shortlist.html`.

Sources:
- [UK Biobank: apply for access](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/)
- [UK Biobank Community FAQ: applying and accessing data](https://community.ukbiobank.ac.uk/hc/en-gb/articles/28002689502237-Applying-to-UK-Biobank-and-accessing-data-FAQ)
- [Research Professional News: UK Biobank set to reopen after data breach](https://www.researchprofessionalnews.com/rr-news-uk-charities-and-societies-2026-10-uk-biobank-set-to-reopen-to-researchers-after-data-breach/)
- [PublicTechnology: UK Biobank security review](https://www.publictechnology.net/2026/07/13/health-and-social-care/uk-biobank-commissions-200k-security-review-after-major-data-incident/)
- [All of Us: Curated Data Repository version 9](https://support.researchallofus.org/hc/en-us/articles/50653909888788-Our-Largest-Genomic-Dataset-Curated-Data-Repository-version-9)
- [All of Us: death data collection](https://support.researchallofus.org/hc/en-us/articles/10237876482196-How-to-find-participant-death-reports)
- [NCHS linked mortality files](https://www.cdc.gov/nchs/linked-data/mortality-files/)
- [MESA actigraphy introduction (sleepdata.org)](https://sleepdata.org/datasets/mesa/pages/actigraphy-introduction.md)
- [China Kadoorie Biobank accelerometer paper](https://ijbnpa.biomedcentral.com/articles/10.1186/s12966-023-01537-8)
- [NFBC1966 Polar Active dose-response paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6322295/)
- [Rush Memory and Aging Project overview](https://pmc.ncbi.nlm.nih.gov/articles/PMC3439198)
- [Rotterdam Study actigraphy and dementia](https://alz-journals.onlinelibrary.wiley.com/doi/10.1002/alz.12122)
- [HUNT4 data resource profile](https://pmc.ncbi.nlm.nih.gov/articles/PMC13457080/)
- [Wrist accelerometer review, Epidemiologic Reviews](https://academic.oup.com/epirev/article/43/1/65/6313190)