I found sources for all of these through web search, but I could only partly verify them. NCBI's GEO pages returned a bot-check page, and the Genentech host refused my connection. So the accessions and access routes below come from search results and papers that cite them. I did not open the repository records. Check each record before you build on it.

## Download now (no application)

| Cohort | Cancer / drug | Accession | Notes |
|---|---|---|---|
| Hugo 2016 | Melanoma, anti-PD-1 | GEO GSE78220 | 28 patients with pre-treatment RNA-seq |
| Riaz 2017 | Melanoma, nivolumab | GEO GSE91061 (also SRP094781, PRJNA356761) | 68 patients, 108 biopsies. Includes both pre-treatment and on-treatment samples, so filter to pre-treatment. Some patients had prior anti-CTLA-4. |
| Gide 2019 | Melanoma, anti-PD-1 alone or with anti-CTLA-4 | ENA PRJEB23709 | Not in GEO. One paper lists EGA EGAD00001005738, so check whether the raw data are open or controlled. |
| Amato | Melanoma, anti-PD-1 | GEO GSE145996 | 52 patients with exome and RNA-seq. I haven't checked how response is annotated. |
| Jung 2019 | NSCLC, anti-PD-1/PD-L1 | GEO GSE135222 | Only 27 patients (7 durable clinical benefit, 20 non-benefit, using PFS > 180 days). |
| Kim 2018 | Gastric, pembrolizumab | ENA ERP107734 | 61 patients deposited. Downstream papers used only 39–45 because of problems with the expression matrix. |
| IMvigor210 | Urothelial, atezolizumab | R package `IMvigor210CoreBiologies` from research-pub.gene.com/IMvigor210CoreBiologies/ | Processed counts and clinical data, including RECIST response. Papers cite 298 to 348 patients. Raw reads are controlled-access (see below). |

## Needs an application, or has restricted raw data

- **Liu 2019 (melanoma, anti-PD-1):** dbGaP phs000452.v3.p1. One paper says it can also be downloaded from cBioPortal, which would let you skip dbGaP for processed data.
- **Van Allen 2015 (melanoma, anti-CTLA-4):** this is the anti-CTLA-4 cohort you'd want, but I did not confirm its accession. I believe it is also under dbGaP phs000452, so verify that.
- **Miao 2018 (ccRCC):** dbGaP phs001493, controlled access.
- **Mariathasan 2018 (IMvigor210 raw data):** EGA EGAS00001002556, controlled access. The processed package above is enough for most uses.
- **Braun 2020 (nivolumab, ccRCC, CheckMate 025):** EGA EGAS00001004290, EGAS00001004291 and EGAS00001004292. EGA requires a Data Access Committee request. One citing paper describes the deposited data as normalized RNA-seq rather than raw. That description is second-hand.
- **MGH melanoma cohort:** dbGaP phs002683.v1.p1.

## Shortcuts: curated compendia

- **TIDE** (tide.dfci.harvard.edu) hosts processed data from published ICB trials. One comparison table counts about 1,247 patients.
- **CRI iAtlas** has preprocessed expression data in TPM, plus clinical and treatment information. A 2026 preprint downloaded 8 cohorts from it.
- **ICBatlas** (bioinfo.life.hust.edu.cn/ICBatlas/) covers 1,515 samples from 25 studies across nine cancer types. I couldn't confirm that it offers bulk download.
- **Cancer-Immu and ICB-Portal** are compared in the bioRxiv review linked below. Cancer-Immu lists 3,652 patients.

## Practical notes

- **Open-access starting set:** Hugo, Riaz, Gide, Amato, IMvigor210, Kim and Jung. That is four melanoma cohorts plus bladder, gastric and lung. Add Liu and Van Allen (via dbGaP or cBioPortal) for more melanoma, and Braun or Miao for kidney.
- **Pre-treatment samples:** Riaz includes on-treatment biopsies and the MGH GSE115821/GSE168204 cohorts include both timepoints. Keep only pre-treatment samples to avoid leakage.
- **Response definitions:** these differ between cohorts (RECIST, durable clinical benefit by PFS, and so on). Harmonize them before pooling.
- **Batch effects:** the cohorts were run on different platforms and pipelines. Plan to reprocess raw data or use cross-cohort normalization, and validate leave-one-cohort-out.
- **Overlap:** check for patients appearing in more than one cohort before you split train and test sets.
- **Not for your use case:** GSE120575 is single-cell, not bulk.

Sources:
- [Search: melanoma anti-PD-1 RNA-seq cohort accessions](https://pmc.ncbi.nlm.nih.gov/articles/PMC13687651)
- [Combined tumor and immune signals… (Cell Reports Medicine)](https://www.sciencedirect.com/science/article/pii/S2666379121003773)
- [Review of ICB transcriptome databases (bioRxiv)](https://www.biorxiv.org/content/10.1101/2024.12.09.627506v1.full)
- [Large-scale public data reuse to model immunotherapy response (TIDE)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7045518/)
- [ICBatlas (Cancer Immunology Research)](https://aacrjournals.org/cancerimmunolres/article/10/11/1398/709876/ICBatlas-A-Comprehensive-Resource-for-Depicting)
- [A Pan-Cancer Immunogenomic Atlas for ICB](https://pmc.ncbi.nlm.nih.gov/articles/PMC9189237/)
- [IMvigor210 ML paper (npj Precision Oncology)](https://www.nature.com/articles/s41698-025-00969-8)
- [Tumor and immune reprogramming in RCC (Cancer Cell)](https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00117-3)
- [Kim 2018 gastric (PubMed)](https://pubmed.ncbi.nlm.nih.gov/30013197/)

I can try fetching the GEO and ENA records through their APIs (E-utilities or the ENA portal) to confirm sample counts and file availability. I can also draft a harmonization table for the response labels.