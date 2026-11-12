You can assemble roughly ten independent cohorts with open processed expression and response labels today, without applying for anything; the largest lung and some kidney trial cohorts need a data access application.

I checked the GEO, ENA and cBioPortal entries below against their live records today. Sample counts are from those records, and the pre-treatment figures marked "about", the access details in the "Apply for access" section and the supplement locations are from memory, so confirm them before planning around them.

## Download right away

| Cohort | Cancer, drug | Samples | Where |
|---|---|---|---|
| IMvigor210 (Mariathasan 2018) | Urothelial, atezolizumab | 347 | R package `IMvigor210CoreBiologies` at research-pub.gene.com; also cBioPortal `blca_iatlas_imvigor210_2017` |
| IMmotion150 (McDermott 2018) | Renal, atezolizumab ± bevacizumab, with a sunitinib arm | 263 | cBioPortal `rcc_iatlas_immotion150_2018` |
| Liu 2019 | Melanoma, anti-PD-1 | 122 | cBioPortal `mel_iatlas_liu_2019` or `mel_dfci_2019` (TPM) |
| Riaz 2017 | Melanoma, nivolumab | 109 (about half pre-treatment) | GEO GSE91061; github.com/riazn/bms038_analysis |
| Gide 2019 | Melanoma, anti-PD-1 ± ipilimumab | 91 RNA-seq runs (about 73 pre-treatment) | ENA PRJEB23709 (raw FASTQ); cBioPortal `mel_iatlas_gide_2019` |
| Van Allen 2015 | Melanoma, ipilimumab | 110 in study (about 40 with RNA) | cBioPortal `skcm_dfci_2015` |
| Hugo 2016 | Melanoma, anti-PD-1 | 28 | GEO GSE78220 |
| Kim 2018 | Gastric, pembrolizumab | 78 RNA-seq runs (45 patients) | ENA PRJEB25780 (raw FASTQ) |
| Rose 2021 | Urothelial, anti-PD-1/PD-L1 | 90 | GEO GSE176307 |
| Foy 2022 | Head and neck, anti-PD-1/PD-L1 | 102 | GEO GSE159067 |
| Foy 2022 | NSCLC, anti-PD-1/PD-L1 | 82 | GEO GSE161537 |
| Jung 2019 | NSCLC, anti-PD-1/PD-L1 | 27 | GEO GSE135222 |
| Cho 2020 | NSCLC, anti-PD-1 | 16 | GEO GSE126044 |
| Hwang 2020 | NSCLC, anti-PD-1 | 21 | GEO GSE136961 |
| Du 2021 | Melanoma, anti-PD-1 | 27 (pre and on-treatment) | GEO GSE168204 |
| Auslander 2018 | Melanoma, anti-PD-1/CTLA-4 | 37 (pre and on-treatment) | GEO GSE115821 |
| Zhao 2019 | Glioblastoma, anti-PD-1 | 34 RNA-seq runs | SRA PRJNA482620 |
| Snyder 2017 | Urothelial, atezolizumab | about 25 | github.com/hammerlab/multi-omic-urothelial-anti-pdl1 |

Other open sets are a worse fit:

- **PRINCE (pancreatic, 93):** nivolumab is given with chemotherapy, so response is not attributable to the checkpoint inhibitor alone (cBioPortal `paad_iatlas_prince_2022`).
- **Cloughesy/Prins glioblastoma (GSE121810, 29):** neoadjuvant design, so much of the tissue is post-treatment.
- **Prat 2017 (GSE93157, 65):** NanoString panel, not RNA-seq.
- **Braun 2020 (renal, nivolumab, CheckMate 009/010/025, about 300 with RNA):** I recall normalised expression and response being in the Nature Medicine supplementary tables, but I did not check this.

## Curated collections

These repackage many of the cohorts above with harmonised response labels, which saves a lot of clinical-table wrangling:

- **ORCESTRA / PredictIO** (orcestra.ca/clinical_icb): each cohort as an R `SummarizedExperiment` with a common response definition.
- **CRI iAtlas**: the source of the "iAtlas Harmonized" cBioPortal studies above, uniformly reprocessed.
- **TIGER** (tiger.canceromics.org) and **TIDE** (tide.dfci.harvard.edu): downloadable processed matrices with responder labels. The TIDE download page returned a 403 to my script, so check it in a browser.

Because these overlap heavily with each other and with the primary sources, de-duplicate by original study before counting independent cohorts.

## Apply for access

| Cohort | Cancer, drug | Size | Access |
|---|---|---|---|
| OAK and POPLAR (Patil 2022) | NSCLC, atezolizumab vs docetaxel | about 700 and 190 with RNA | EGA EGAS00001005013, Genentech committee |
| IMmotion151 (Motzer 2020) | Renal, atezolizumab + bevacizumab | about 800 | EGA EGAS00001004353 |
| SU2C-MARK (Ravi 2023) | NSCLC, anti-PD-1/PD-L1 | about 150 with RNA | dbGaP phs002822 |
| Braun 2020 raw data | Renal, nivolumab | about 300 | EGA EGAS00001004290 to 4292 |
| Miao 2018 | Renal, anti-PD-1 | about 30 with RNA | dbGaP phs001493 |
| Raw reads for Van Allen and Liu | Melanoma | as above | dbGaP phs000452 |
| Raw reads for IMvigor210 | Urothelial | as above | EGA EGAS00001002556 |

dbGaP typically takes a few weeks through your institution's signing official. EGA committees for company trials are slower and may restrict use to non-commercial research.

## Things that will affect your classifier

- **Pre-treatment filtering:** Riaz, Gide, Du and Auslander mix pre- and on-treatment biopsies, so filter on the sample annotation before training.
- **Response definitions differ:** most use RECIST best response, but Liu, Jung and Hwang lean on clinical benefit or progression-free survival thresholds. Decide how to handle stable disease up front.
- **Prior therapy:** part of Riaz and Liu had progressed on ipilimumab before anti-PD-1, which shifts both biology and response rate.
- **Processing differs:** the cohorts span poly-A, total and capture-based RNA-seq libraries, including FFPE material, and the deposited matrices use different units. Re-quantifying from FASTQ is only possible for Gide, Kim, Zhao and the GEO sets with SRA runs.

A practical starting design is to train on melanoma (Liu, Gide, Riaz, Hugo, Van Allen) and hold out IMvigor210, IMmotion150, Kim and the two Foy cohorts as cross-cancer validation.