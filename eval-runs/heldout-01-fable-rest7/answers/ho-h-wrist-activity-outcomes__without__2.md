Four datasets fit your criteria well, and the most obvious one, UK Biobank, is not taking new applications right now. NHANES and All of Us are the ones you can start on today.

| Dataset | Wrist device and wear | Size | Linked outcomes | Access |
|---|---|---|---|---|
| **UK Biobank** | Axivity AX3, 7 days | ~100,000 (from memory) | Hospital, cancer and death registries | New applications paused |
| **NHANES 2011–2014** (US) | ActiGraph GT3X+, non-dominant wrist, up to 7 full days | 13,603 with minute-level data (includes children) | Deaths only, via the National Death Index | Open download |
| **All of Us** (US) | Participants' own Fitbits, long-running records | 68,000+ in the 2026 release | Electronic health records | Registration, no project review |
| **China Kadoorie Biobank** | Axivity AX3, 7 days | 20,370 | Death and hospital records | Application; accelerometer release unconfirmed |
| **Whitehall II** (UK) | GENEActiv, non-dominant wrist, 9 days | 4,204 | Hospital records and deaths | Application via Dementias Platform UK |

**UK Biobank**
- **Status:** Researcher access was suspended on 23 April 2026 after exported participant data were found for sale online. New applications were targeted to reopen in "late 2026", and I found no confirmation that they have.
- **Cost:** The tier that covers linked health records is £3,000 for three years, plus cloud compute. I could not confirm which tier the accelerometer data sit in.
- **Process:** Analysis is only on its cloud platform, and about 15 weeks typically pass from application to data. Expect tighter export rules on reopening.
- **Caveat:** I could not open the official pages directly, so the status comes from search summaries of them; check the Apply for access page.

**NHANES 2011–2014**
- **Access:** Both the accelerometer files (raw 80 Hz and minute-level summaries) and the public mortality file are free downloads with no application.
- **Follow-up:** Public mortality follow-up runs to 31 December 2019, for adults only.
- **Limits:** The public file perturbs some follow-up times and causes of death. The unaltered files require a proposal to the NCHS Research Data Center. There is no disease incidence linkage.

**All of Us**
- **Access:** Your university signs a data use agreement (many already have), then you verify your identity and complete training. Analysis is in its cloud workbench, and you pay for compute.
- **Limits:** Fitbit owners are self-selected, device data are processed by Fitbit's proprietary algorithms, and death capture is incomplete. This makes it the least comparable to research-grade wrist studies.

**China Kadoorie Biobank**
- **Access:** You apply to the Oxford team, and your institution contracts with the University of Oxford. The fee is £2,500 per approved request for researchers outside mainland China and Hong Kong.
- **Limits:** The accelerometer data come from the 2020–2021 resurvey, and I could not confirm they are released to external researchers yet. Email ckbaccess@ndph.ox.ac.uk before planning around it. Follow-up after wear is still short.

**Whitehall II**
- **Access:** Requests are triaged by Dementias Platform UK and then reviewed by the study's data sharing committee.
- **Follow-up:** A recent analysis followed participants to August 2024.
- **Limits:** Participants were aged 60–83 at wear and are all civil servants. I could not confirm fees, timelines, or whether raw files are available.

**Smaller sleep-focused options**
- **MESA Sleep:** 2,237 adults with a week of wrist actigraphy. The actigraphy is at the National Sleep Research Resource, and cardiovascular events need a separate request to NHLBI's BioLINCC repository.
- **HCHS/SOL Sueño:** About a week of wrist actigraphy in US Hispanic/Latino adults (roughly 2,200, from memory), through the same two repositories.
- **MrOS Sleep:** 3,135 older men, but only 3–5 days of wear, and the actigraphy requires an analysis proposal to the coordinating center.

I left out cohorts that used hip or thigh devices (for example Women's Health Study, REGARDS, HUNT4), since they would break your comparability requirement.

My recommendation: start with NHANES for mortality now, register for All of Us in parallel, and prepare a UK Biobank application to submit when the pause lifts, since it is the main comparator for wrist-based outcome studies.

Sources:
- [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)
- [UK Biobank apply for access](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/)
- [UK Biobank Oversight Committee report, June 2026](https://www.ukbiobank.ac.uk/wp-content/uploads/2026/06/UK-Biobank-Oversight-Committee-report-June-2026.pdf)
- [UK Biobank: can I apply?](https://community.ukbiobank.ac.uk/hc/en-gb/articles/37284734505117-Can-I-apply-to-use-UK-Biobank-data)
- [NCHS public-use linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm)
- [NCI physical activity resources (NHANES raw data)](https://epi.grants.cancer.gov/physical/research-resources.html)
- [NHANES 2011–2014 minute-level data on PhysioNet](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/)
- [All of Us data release v9 notes](https://support.researchallofus.org/hc/en-us/articles/50653909888788-Our-Largest-Genomic-Dataset-Curated-Data-Repository-version-9)
- [All of Us wearables dataset paper](https://www.nature.com/articles/s41591-026-04352-3)
- [China Kadoorie Biobank accelerometer paper](https://link.springer.com/article/10.1186/s12966-023-01537-8)
- [China Kadoorie Biobank data access policy](https://www.ckbiobank.org/data-access/data-2)
- [China Kadoorie Biobank data overview](https://www.ckbiobank.org/data-access/data-overview)
- [Whitehall II data sharing](https://www.ucl.ac.uk/brain-sciences/psychiatry/our-research/mental-health-older-people/whitehall-ii/data-sharing)
- [Whitehall II accelerometer consent paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4208789/)
- [NSRR: MESA](https://sleepdata.org/datasets/mesa)
- [NSRR: HCHS/SOL](https://sleepdata.org/datasets/hchs)
- [NSRR: MrOS](https://sleepdata.org/datasets/mros)