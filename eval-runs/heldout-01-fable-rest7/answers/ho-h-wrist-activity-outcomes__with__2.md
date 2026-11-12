Six datasets fit, but the best-known one, UK Biobank, appears to have paused new applications since April 2026, so NHANES (open today) and All of Us (days, if your university has an agreement in place) are where to start. I could not open the official UK Biobank, All of Us, Whitehall II or NSRR pages directly (they block automated readers), so their access terms below come from search results and memory, as marked.

## What I assumed you need

- **Wrist placement (must):** a research accelerometer or consumer tracker worn on the wrist.
- **Wear time (must):** free-living wear for several days to a week or longer.
- **Size (must):** at least a few thousand adults.
- **Outcomes (must):** linked deaths, hospital records or diagnoses after the wear period.
- **Access (must):** obtainable from a US university; applications are fine.
- **Activity and sleep (nice to have):** 24-hour wear with minute-level or raw data, so both can be derived.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES 2011–2014 wrist accelerometry + public linked mortality files | Open download, minutes | No formal licence; NCHS data-use terms | 14,693 wearers of all ages; about 7,100 adults in a 2026 mortality paper | Strong, but deaths only | Today |
| 2 | All of Us Fitbit + health records | Institutional agreement, then individual registration and training; days if the agreement exists; cloud-only analysis | Data User Code of Conduct | More than 59,000 with wearable data | Strong, but consumer device with no raw signal | Search results today; official site not read |
| 3 | UK Biobank accelerometer sub-study | Application, institutional agreement and fee; new applications reported paused; months | Material Transfer Agreement | About 100,000 | Strongest on content | Search results today; official site not read |
| 4 | Whitehall II accelerometer sub-study | Application to the study's data sharing committee plus signed agreement; months | Study access agreement | About 4,000 | Strong | Search results today; official site not read |
| 5 | MrOS and SOF wrist actigraphy | Free account plus click-through data use agreement; days | Data Use Agreement | About 3,000 men and 3,000 women | Partial | Today (home pages) |
| 6 | MESA Sleep actigraphy | NSRR request plus a separate BioLINCC application for outcomes; weeks | Per-dataset agreements | 2,237 | Partial | Search results and memory |

## Details

**1. NHANES 2011–2014** ([accelerometer documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm), [linked mortality files](https://www.cdc.gov/nchs/linked-data/mortality-files/))
- **Contents:** ActiGraph GT3X+ on the non-dominant wrist for seven 24-hour days, in a US national sample. Minute-level and raw 80 Hz files are public, with an algorithm-predicted wake/sleep/non-wear flag.
- **Outcomes:** deaths only, through 31 December 2019. The public mortality files replace follow-up time or cause of death with synthetic values for some records; vital status is unaltered.
- **What is missing:** no public hospital or diagnosis linkage. Unaltered mortality data need an approved project at the NCHS Research Data Center; Medicare and Medicaid linkage sits there too (from memory).
- **Steps:** download the accelerometer files for both cycles, download the mortality files, merge on the participant ID.
- **Shortcut:** an open [PhysioNet release](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/) (CC0) provides minute-level step counts already derived from the raw data.
- **Used by:** [activity fragmentation and cause-specific mortality, 2026](https://doi.org/10.1186/s12889-026-29778-9).

**2. All of Us** ([CDR v8 release notes](https://support.researchallofus.org/hc/en-us/articles/30294451486356-Curated-Data-Repository-CDR-version-8-Release-Notes), [NIH research page](https://www.nih.gov/allofus/research))
- **Contents:** Fitbit steps, heart rate, activity and sleep stages, often over months or years, linked to health record diagnoses. Wearable data are in the Registered Tier.
- **What is missing:** no raw acceleration, and metrics come from Fitbit's proprietary algorithms. Device model is recorded for about 90% of donors, so filter to wrist models. Death capture is incomplete (from memory).
- **Steps:**
  1. Confirm your university has signed the Data Use and Registration Agreement.
  2. Register with identity verification.
  3. Complete the responsible conduct training and sign the code of conduct.
  4. Create a workspace with a public project description.
- **Conditions:** analysis happens only inside the cloud Workbench, with no participant-level downloads. Compute is billed after initial credits (from memory).
- **Used by:** [sleep patterns and chronic disease](https://doi.org/10.1038/s41591-024-03155-8), [11 million days of Fitbit data](https://doi.org/10.1038/s41467-026-78529-2), [activity and chronic disease risk](https://doi.org/10.1038/s43856-025-01372-x).

**3. UK Biobank** ([apply for access](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/))
- **Contents:** Axivity AX3 wrist accelerometer for seven days in 2013–2015, with raw data, linked to hospital records and to cancer and death registries. This is the cohort most wrist studies compare against.
- **Current status:** search results say the analysis platform was suspended on 23 April 2026 after exported data were found for sale. New project applications were still paused as of late October, with a "late 2026" target and no confirmed date. Confirm this on the official page before planning.
- **Steps when open:** register in the Access Management System, submit a project application, have your institution sign the transfer agreement, and pay the fee.
- **Fees:** search results cite £3,000 to £9,000 plus VAT for three years depending on tier, with a reduced student rate. I did not confirm which tier covers accelerometry.
- **Timing:** about 15 weeks was quoted for normal times. Analysis is on the cloud platform only.
- **Interim route:** ask whether a colleague already holds an approved project you could join. I could not confirm that additions are being processed during the pause.
- **Used by:** [the methods paper](https://doi.org/10.1371/journal.pone.0169649), [sleep regularity and mortality](https://doi.org/10.1093/sleep/zsad253), [step counts and mortality](https://doi.org/10.1249/mss.0000000000003478).

**4. Whitehall II** ([data sharing page](https://www.ucl.ac.uk/brain-sciences/psychiatry/our-research/mental-health-older-people/whitehall-ii/data-sharing))
- **Contents:** GENEActiv on the non-dominant wrist for nine days in 2012–2013, with 4,008 valid recordings in adults aged 60–83. Deaths come from the NHS register (633 deaths, followed to November 2023 in a 2025 paper), and diagnoses from hospital records.
- **What is missing:** it is an occupational cohort that is about three-quarters men. I could not confirm whether raw accelerometer files and linked hospital data are released to external applicants on the same terms as the core data.
- **Steps:** apply directly to the study team or through the Dementias Platform UK portal. The platform triages, the Whitehall II committee decides, and you sign the access agreement.
- **Used by:** [Whitehall II and UK Biobank mortality comparison](https://doi.org/10.1038/s41598-025-30237-5), which is a ready template for cross-cohort comparability, and [activity and successful ageing](https://doi.org/10.1038/srep45772).

**5. MrOS and SOF** ([MrOS Online](https://mrosonline.ucsf.edu/), [SOF Online](https://sofonline.ucsf.edu/))
- **Contents:** wrist actigraphy in older US men (about 5 days, 2003–2005) and older women, with long study-adjudicated follow-up for death, fractures and cardiovascular events.
- **What is missing:** these are count-based actigraphs from the early 2000s, so intensity metrics will not map onto modern raw-acceleration measures. I could not confirm whether epoch-level files are downloadable or what actigraphy SOF Online holds.
- **Steps:** register on each site and accept the data use agreement. Both home pages state: "You must have an account and accept the terms of a Data Use Agreement before you can download or explore clinical data."
- **Used by:** [rest-activity rhythms and mortality in MrOS](https://doi.org/10.3109/07420520903419157), [incident diabetes](https://doi.org/10.2337/dc20-0557), [SOF and MrOS combined](https://doi.org/10.1093/geroni/igy023.363).

**6. MESA Sleep** ([NSRR page](https://sleepdata.org/datasets/mesa))
- **Contents:** Actiwatch Spectrum on the wrist for seven days in 2010–2013, in a multi-ethnic US cohort; 2,159 people have epoch files.
- **What is missing:** cardiovascular events and deaths are not on NSRR. They need a separate BioLINCC application with an ethics determination and an institution-signed agreement (from memory).
- **Steps:** request the actigraphy from NSRR, apply to BioLINCC for the events data, and merge on the BioLINCC participant ID.

## Known, not confirmed

- **China Kadoorie Biobank, third resurvey:** about 20,000 adults wore an Axivity AX3 on the wrist for seven days in 2020–2021 ([description paper](https://doi.org/10.1186/s12966-023-01537-8)). The open-access policy I found covers baseline, the first two resurveys and disease follow-up, not this resurvey. Check the [data access page](https://www.ckbiobank.org/data-access) for the release schedule; collaboration with the study team may be the only route.
- **Rotterdam Study:** wrist actigraphy with mortality follow-up in 1,734 people ([paper](https://doi.org/10.1093/aje/kwu245)). From memory, data go by request to the study's management team and export is restricted. I did not confirm the procedure or any later, larger wave.
- **CoLaus|PsyCoLaus (Lausanne):** from memory, about 2,900 adults with 14 days of wrist GENEActiv. It was used as the external validation cohort for a Whitehall II mortality model. Access is by request to the study's committee, not confirmed.

## Not recommended, and why

- **NHANES 2003–2006:** open with long mortality follow-up, but the device was hip-worn.
- **German National Cohort (NAKO):** hip-worn, and applications were described as limited to researchers in EU countries.
- **WHI OPACH, Women's Health Study, REGARDS:** large US cohorts with outcomes, but hip-worn (from memory).
- **HCHS/SOL Sueño:** wrist actigraphy for a week, but only 1,887 people in the public epoch files and I found no outcome linkage.
- **CAPTURE-24 and similar activity-recognition sets:** open raw wrist data, but about 150 people and no outcomes.

## What I could not find

- No dataset accessible now pairs raw wrist accelerometry with hospital-record linkage at UK Biobank scale. NHANES has deaths only in its public files; All of Us has diagnoses but no raw signal.
- Registry searches returned almost only paper supplements and unrelated datasets; everything above came from the literature and study portals.

## Next step

Download NHANES today and build your pipeline on it. In parallel, ask your research office whether the All of Us agreement is signed, and send the Whitehall II application, since it is the slowest. Check the UK Biobank application page for a reopening date, and ask your institution early whether these secondary analyses need an ethics exemption.

The interactive shortlist, with filters and an exportable access plan, is at `/private/tmp/e-JDr6IM/home/cwd/dataset-shortlist.html`. Checked 12 November 2026.

Sources not linked above:
- [UK Biobank Research Analysis Platform](https://www.ukbiobank.ac.uk/use-our-data/research-analysis-platform/)
- [UK Biobank community FAQ: Can I apply to use UK Biobank data?](https://community.ukbiobank.ac.uk/hc/en-gb/articles/37284734505117-Can-I-apply-to-use-UK-Biobank-data)
- [UK Biobank Oversight Committee report, June 2026](https://www.ukbiobank.ac.uk/wp-content/uploads/2026/06/UK-Biobank-Oversight-Committee-report-June-2026.pdf)
- [All of Us Data Access Framework](https://support.researchallofus.org/hc/en-us/articles/22346942074132-Data-Access-Framework)
- [The All of Us wearables dataset, Nature Medicine](https://www.nature.com/articles/s41591-026-04352-3)
- [Dementias Platform UK cohort data availability](https://portal.dementiasplatform.uk/data/cohort-data-availability/)
- [Movement-behaviour profiles and mortality in Whitehall II](https://pmc.ncbi.nlm.nih.gov/articles/PMC11216065/)
- [NSRR MrOS page](https://sleepdata.org/datasets/mros)
- [NSRR MESA actigraphy introduction](https://sleepdata.org/datasets/mesa/pages/actigraphy-introduction.md)
- [NSRR HCHS/SOL actigraphy introduction](https://sleepdata.org/datasets/hchs/pages/actigraphy-introduction.md)
- [China Kadoorie Biobank third resurvey news item](https://www.ckbiobank.org/news-1/3rd-resurvey-of-ckb-participants-completed)
- [Pooled UK Biobank and NAKO accelerometer analysis](https://link.springer.com/article/10.1186/s12966-026-01980-3)