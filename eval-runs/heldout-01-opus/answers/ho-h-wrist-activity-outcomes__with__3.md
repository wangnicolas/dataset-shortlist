I found eight datasets worth considering. The one most wrist studies compare against, **UK Biobank, is not taking new applications right now**. **NHANES 2011–2014 is the one you can start on today**, and **All of Us** is likely the fastest route to records-linked data for a US university.

## What I assumed you need
- **Must have:** a wrist-worn device; several days or more of everyday wear; a few thousand adults or more; linked outcomes (hospital records, diagnoses or deaths).
- **Nice to have:** raw or minute-level signal, so you can process it the same way as other wrist studies.
- **Assumed:** non-US cohorts are fine, and waiting weeks to months for approval is acceptable.

## Shortlist (checked 12 Nov 2026)
| # | Dataset | Access | Wrist device / size | Outcomes | Checked |
|---|---|---|---|---|---|
| 1 | NHANES 2011–14 + Linked Mortality Files | Direct download; minutes | ActiGraph GT3X+, 9 days, ~12,600–14,700 | Deaths only (to 2019 public; to 2022 restricted) | today |
| 2 | UK Biobank accelerometer sub-study | Application + fee; **new applications paused** | Axivity AX3, 7 days, ~100k | Hospital records, deaths, cancer | today (web search) |
| 3 | All of Us (Fitbit + health records) | Institutional agreement + training; days | Fitbit, often months, 12.8k in 2022 (more now) | Health-record diagnoses | today |
| 4 | Whitehall II (GENEActiv) | Application via Dementias Platform UK; weeks | GENEActiv, 9 days, 4,204 | Deaths; hospital records from memory | today (web search) |
| 5 | China Kadoorie Biobank, 3rd resurvey | Application; months; release status unclear | Axivity AX3, 7 days, ~20,400 | Hospital insurance and death registries (from memory); short follow-up | today (web search) |
| 6 | MrOS (older men) | Free registration + online agreement; days | Wrist actigraph, ~5 nights, 3,135 | Reviewed deaths and heart events, ~15 yrs | today (web search) |
| 7 | MESA Sleep | Agreement + ethics approval (IRB); weeks | Actiwatch, 7 days, 2,237 | Heart events via a separate request | today (web search) |
| 8 | Rush Memory and Aging Project | Data request; weeks | Actical, up to 10 days, repeated, ~1,000+ | Deaths, dementia, autopsy | today (web search) |

"Today" means I confirmed the page with the checking tool. "Today (web search)" means the site blocked automated checks (UK Biobank, UCL, CKB, UCSF, sleepdata.org and Rush all did), so those facts come from web search results today, not from the site itself.

## Details and access steps
**1. NHANES 2011–2014.** Participants wore an ActiGraph on the non-dominant wrist for 9 days, and minute-level files (in MIMS units) are released.
- **Access:** download the activity files for the 2011–12 and 2013–14 cycles, then the public mortality files from the [CDC linked-data page](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm). No application.
- **Limits:** the public files end follow-up on 31 Dec 2019, and CDC alters follow-up time or cause of death for a few records to protect privacy. Follow-up to 2022 is only available as restricted files through an NCHS Research Data Center, which takes months.
- **Outcomes:** deaths only, no hospital records.
- **Example paper:** [PMC11402588](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/).

**2. UK Biobank.** Still the best match on paper: about 100k adults, raw 100 Hz signal, and linked hospital, cancer and death records.
- **Status:** its FAQ (updated 22 Oct 2026) says "We are not currently accepting applications for new research projects", with reopening planned for late 2026. This follows a [data leak in 2026](https://www.the-scientist.com/uk-biobank-to-restore-access-months-after-massive-data-leak-75197).
- **Fees when it reopens:** Tier 1 is £3,000 for 3 years (£500 for students, who must apply with their supervisor). See the [fees page](https://www.ukbiobank.ac.uk/use-our-data/fees/).
- **Where you analyse:** only on its cloud platform (UKB-RAP), with compute billed separately. Some new linked health data is being held back until government data providers sign off.
- **Plan for now:** register on its application system and prepare your proposal.
- **Example paper:** [10.1371/journal.pmed.1005213](https://doi.org/10.1371/journal.pmed.1005213).

**3. All of Us.**
- **Access:** your university must have signed a Data Use and Registration Agreement (most large US universities have). You then register on the [Researcher Workbench](https://www.researchallofus.org/data-tools/workbench/), verify your identity and complete training. The Controlled Tier, which has real event dates, needs an amended agreement and extra training.
- **Rules:** you work only in their cloud workbench and may not link records to outside data.
- **Caveat for comparability:** this is consumer-tracker output (steps, heart rate, sleep stages), not raw acceleration. People who already own a Fitbit are also not a random sample.
- **Recent papers:** many on sleep, activity and disease.

**4. Whitehall II.** About 4,200 participants wore a GENEActiv on the non-dominant wrist for 9 days in 2012–13.
- **Access:** apply through the [DPUK portal](https://portal.dementiasplatform.uk/data/cohort-data-availability/). You choose variables, the Whitehall committee reviews the request, you sign an access agreement and you analyse in a secure remote environment.
- **To ask:** whether the raw device files are available (whitehall2@ucl.ac.uk).

**5. China Kadoorie Biobank.** The same device as UK Biobank, worn by about 20,000 adults in 2020–21 ([Chen et al. 2023](https://link.springer.com/article/10.1186/s12966-023-01537-8)).
- **Status:** I could not confirm whether the accelerometer data has been released to researchers through the CKB Data Access System yet.
- **Limit:** follow-up is still short.

**6. MrOS.** Free registration and an online data-use agreement on MrOS Online. It has actigraphy from the sleep visit (n=3,135) and mortality with more than half of participants deceased. See this [mortality paper](https://academic.oup.com/sleep/article/45/4/zsac015/6509372). The sister study of older women, SOF (about 3,000), is requested through SOF Online, and its access terms are not confirmed.

**7. MESA Sleep.** Raw actigraphy is on the National Sleep Research Resource (NSRR), which needs a data-use agreement and ethics approval (IRB). Heart events must be requested separately from BioLINCC or the MESA Coordinating Center.

**8. Rush Memory and Aging Project.** Request through the Rush Alzheimer's Disease Center (RADC) Research Resource Sharing Hub. It is smaller than your target, but people wore the device repeatedly over years.

## Known, not confirmed
- The device MrOS used (from memory: SleepWatch-O, a wrist actigraph), and whether raw epochs are available.
- Whitehall II's hospital-record linkage (from memory).
- Two smaller US cohorts I did not check: the Baltimore Longitudinal Study of Aging (wrist ActiGraph/GENEActiv, roughly 1,000 people, application at blsa.nih.gov) and the Study of Osteoporotic Fractures (SOF).

## Not recommended
These wore the device on the hip or thigh, which fails your wrist requirement:
- NHANES 2003–06, the Women's Health Study and the WHI OPACH study (hip)
- HUNT4 (thigh and lower back)
- REGARDS, Tromsø 7 and the German National Cohort (hip, from memory)
- 1970 British Cohort Study (thigh)

These are wrist-based but probably fall short:
- HCHS/SOL Sueño: about 1,900 participants on NSRR, and published work so far does not follow people over time.
- Rotterdam Study (GENEActiv): about 1,200–1,400 people, requested by email.

## What I could not find
No openly downloadable wrist dataset that is also linked to hospital records. NHANES has deaths only.

## Next step
1. Start on NHANES now.
2. Check whether your university has an All of Us agreement, and register.
3. Draft a UK Biobank application for when it reopens.
4. Email the Whitehall II team about the raw device files.

Pooling NHANES or All of Us with UK Biobank and Whitehall II would give you external validation on different wrist devices.

I've saved an interactive version of this shortlist, where you can filter, compare datasets and export an access plan: `/private/tmp/e-Dth5Qj/home/cwd/dataset-shortlist.html`

Sources: [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/), [UK Biobank apply page](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/), [The Scientist](https://www.the-scientist.com/uk-biobank-to-restore-access-months-after-massive-data-leak-75197), [CDC public mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm), [CDC linked-data FTP](https://ftp.cdc.gov/pub/Health_Statistics/NCHS/datalinkage/linked_mortality/), [NHANES mortality paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/), [All of Us Workbench](https://www.researchallofus.org/data-tools/workbench/), [All of Us data access framework](https://support.researchallofus.org/hc/en-us/articles/22346942074132-Data-Access-Framework), [DPUK cohort availability](https://portal.dementiasplatform.uk/data/cohort-data-availability/), [Whitehall II data sharing](https://www.ucl.ac.uk/brain-sciences/psychiatry/our-research/mental-health-older-people/whitehall-ii/data-sharing), [CKB resurvey](https://www.ckbiobank.org/news-1/3rd-resurvey-of-ckb-participants-completed), [CKB accelerometry paper](https://link.springer.com/article/10.1186/s12966-023-01537-8), [MrOS Online](https://sfcc.ucsf.edu/news/over-16-years-prospective-data-mros-online), [NSRR MrOS](https://sleepdata.org/datasets/mros), [NSRR MESA](https://sleepdata.org/datasets/mesa), [NSRR HCHS/SOL](https://sleepdata.org/datasets/hchs), [RADC study designs](https://www.radc.rush.edu/docs/parentStudyDesigns.htm), [Rotterdam wrist accelerometry paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5739112/)