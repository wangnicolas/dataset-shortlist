For your design, three datasets do most of the work: NHANES 2011–2014 (usable today), UK Biobank (the field's reference dataset, but access is suspended right now), and All of Us (the only large tracker-based option). I checked access terms on the web today; items marked "from memory" I did not re-verify.

## Main options

| Dataset | Wrist device and wear | Size | Linked outcomes | Access |
|---|---|---|---|---|
| **NHANES 2011–2014** | ActiGraph GT3X+, non-dominant wrist, 7 days, 24 h | About 7,600 adults with valid wear | Deaths via National Death Index through 31 Dec 2019 | Public download, no application |
| **UK Biobank** | Axivity AX3, 7 days (2013–15) | About 100,000 adults (from memory) | Hospital records, cancer and death registries | Paid application; currently on hold |
| **All of Us** | Participants' Fitbits, often months to years | About 59,000 with Fitbit data; roughly 22,000–29,000 also have health records | Electronic health records; deaths only from those records | Institutional agreement, free |
| **Whitehall II** | GENEActiv, non-dominant wrist, 9 days (2012–13) | About 4,200, aged 60–83 | NHS mortality register through 2024; hospital records | Application to UCL |
| **China Kadoorie Biobank** | Axivity AX3, 7 days (2020–21) | About 20,000–21,000 | Death and hospitalisation records (from memory) | Application; release status unconfirmed |

## What access involves

- **NHANES:** Download the minute-level files (PAXMIN) and the public-use linked mortality file from CDC.
  - The public mortality file has perturbed follow-up values for some records and limited cause-of-death detail.
  - Full mortality detail and Medicare/Medicaid linkage need a proposal to the NCHS Research Data Center, with fees and on-site or remote enclave analysis (from memory).
- **UK Biobank:** Normally you register, submit a project application, have your institution sign a Material Transfer Agreement, and pay.
  - Fees are £3,000 for three years at Tier 1, plus VAT and cloud compute; analysis runs only on their cloud platform. I could not confirm which tier covers the accelerometer data.
  - Access was suspended on 23 April 2026 after exported data appeared for sale. New applications are on hold, with "late 2026" targeted for reopening and no firm date.
  - Approval took about 15 weeks on average before the suspension.
- **All of Us:** Your university signs a Data Use and Registration Agreement (many US universities already have one). You then verify your identity, complete training, and work in the Researcher Workbench.
  - Access is free, with $300 in initial compute credits.
  - Fitbit owners are a self-selected group, the measures are consumer-device outputs rather than raw acceleration, and deaths are under-counted.
- **Whitehall II:** Submit a data-sharing application to the UCL study team. I did not confirm whether linked hospital records are released to external applicants.
- **China Kadoorie Biobank:** Apply through the CKB Data Access System. I could not confirm that the accelerometer data are released yet, and follow-up since 2020–21 is short.

## Smaller or narrower cohorts

- **MrOS and SOF:** About 3,000 older men and about 3,000 older women (SOF from memory) with wrist actigraphy. MrOS wear was only 3–5 days. Deaths and events come from cohort follow-up rather than records, and data are free through MrOS Online and SOF Online after registration and a data use agreement.
- **Northern Finland Birth Cohort 1966:** About 5,500 people wore a wrist Polar Active for two weeks at age 46, linked to Finnish national registers. Access is by request to the University of Oulu with a Data Transfer Agreement. The cohort is still young, so events are few.
- **MESA Sleep and CoLaus:** Each has roughly 2,000–3,000 participants with wrist devices and adjudicated events (from memory). MESA goes through NSRR and BioLINCC; CoLaus is by collaboration request.

Many well-known accelerometer cohorts used hip or thigh devices and don't fit your requirement, including NHANES 2003–2006, the Women's Health Study, REGARDS and HUNT4.

## Recommendation

Start on NHANES now, since it needs no approval and uses a research-grade wrist device. Prepare a UK Biobank application to submit when applications reopen, because most published wrist-based outcome studies use it. Add All of Us if you want long-duration tracker data and can live with the weaker death ascertainment.

Sources:
- [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)
- [UK Biobank Research Analysis Platform](https://www.ukbiobank.ac.uk/use-our-data/research-analysis-platform/)
- [UK Biobank: Can I apply to use UK Biobank data?](https://community.ukbiobank.ac.uk/hc/en-gb/articles/37284734505117-Can-I-apply-to-use-UK-Biobank-data)
- [UK Biobank Oversight Committee report, June 2026](https://www.ukbiobank.ac.uk/wp-content/uploads/2026/06/UK-Biobank-Oversight-Committee-report-June-2026.pdf)
- [NHANES PAXMIN_G documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm)
- [NCHS public-use linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm)
- [Leroux et al., NHANES 2011–2014 and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/)
- [All of Us wearables dataset, Nature Medicine](https://www.nature.com/articles/s41591-026-04352-3)
- [All of Us registration](https://www.researchallofus.org/register/)
- [All of Us mortality ascertainment, AJE](https://doi.org/10.1093/aje/kwaf118)
- [All of Us reweighting and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC13716494)
- [Whitehall II walking cadence and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC13695056)
- [Whitehall II and UK Biobank epoch measures](https://www.nature.com/articles/s41598-025-30237-5)
- [CKB accelerometer paper](https://link.springer.com/article/10.1186/s12966-023-01537-8)
- [CKB third resurvey](https://www.ckbiobank.org/news-1/3rd-resurvey-of-ckb-participants-completed)
- [MrOS on NSRR](https://sleepdata.org/datasets/mros)
- [MrOS/SOF actigraphy and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC8996026/)
- [NFBC1966 cohort profile](https://academic.oup.com/ije/article/50/6/1786/6359466)
- [NFBC information for researchers](https://www.oulu.fi/en/university/faculties-and-units/faculty-medicine/northern-finland-birth-cohorts-and-arctic-biobank/nfbc-aineistopyynto)