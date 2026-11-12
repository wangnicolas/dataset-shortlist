You can download these right away. There are enough open cohorts with pre-treatment RNA-seq and response labels to train on several studies and test on others. The large controlled-access cohorts add more training data but take weeks to months to get. I wrote this from memory and didn't check the links in this session, so confirm each accession on GEO, ENA or EGA before you build a pipeline around it.

## 1. Download now (open access)

| Cohort | Cancer / drug | ~n with pre-treatment RNA | Where |
|---|---|---|---|
| **Hugo 2016** (Cell) | Melanoma, anti-PD-1 | ~27 | GEO **GSE78220** (FPKM; raw on SRA) |
| **Riaz 2017** (Cell, CheckMate 038) | Melanoma, nivolumab; some patients had already progressed on ipilimumab | ~50 pre, plus on-treatment | GEO **GSE91061** |
| **Gide 2019** (Cancer Cell) | Melanoma, anti-PD-1 ± anti-CTLA-4 | ~90 | ENA **PRJEB23709** (FASTQ) |
| **Auslander 2018** (Nat Med) | Melanoma, anti-PD-1 / anti-CTLA-4 | ~37 | GEO **GSE115821** |
| **Kim 2018** (Nat Med) | Gastric, pembrolizumab | ~45 | ENA **PRJEB25780** |
| **IMvigor210** (Mariathasan 2018, Nature) | Urothelial, atezolizumab | ~350 (the largest open cohort) | R package **IMvigor210CoreBiologies** (counts and RECIST). Raw data is in EGA (controlled). |
| **Braun 2020** (Nat Med, CheckMate 009/010/025) | ccRCC, nivolumab (everolimus control arm) | ~180 on nivolumab | Processed expression and clinical data in the paper's supplementary tables. Raw data is controlled. |
| **Rose 2021** | Urothelial, anti-PD-1/PD-L1 | ~90 | GEO **GSE176307** |
| **Jung 2019** / **Cho 2020** | NSCLC, anti-PD-1/PD-L1 | ~27 / ~16 | GEO **GSE135222** / **GSE126044** |
| **Zhao 2019** (Nat Med) | GBM, anti-PD-1 | small | SRA **PRJNA482620** |

GBM response is not RECIST-based, so I'd treat Zhao 2019 as a stress test rather than a core cohort.

## 2. Apply first (controlled access)

- **Van Allen 2015** (melanoma, anti-CTLA-4, n≈42) and **Liu 2019** (melanoma, anti-PD-1, n≈120): both are under dbGaP **phs000452**. Processed matrices are in the paper supplements and on cBioPortal, so you may not need the raw data.
- **Miao 2018** (ccRCC, n≈33): dbGaP **phs001493**.
- **IMmotion150** (McDermott 2018, RCC, atezolizumab ± bevacizumab): EGA **EGAS00001002928**.
- **JAVELIN Renal 101**, **IMmotion151**, **POPLAR/OAK**: these are trial-sponsor datasets. Access goes through EGA data access committees or sponsor platforms such as Vivli or YODA.
- **Ravi 2023** (NSCLC, SU2C-MARK, n≈150 RNA) and the **CPI1000+ compendium** (Litchfield 2021): raw data is controlled. Check the supplements for processed data.

dbGaP approval usually takes 4–8 weeks and needs your institution's signing official. EGA timelines depend on each committee.

## 3. Curated collections (fastest way to start)

These sites have already harmonised many of the cohorts above, with response labels attached:
- **ORCESTRA / PredictIO** (Haibe-Kains lab): ICB cohorts packaged as R MultiAssayExperiment objects. This is the best fit for cross-study validation.
- **CRI iAtlas ICI module**: harmonised ICB cohorts on Synapse. Downloading needs a free Synapse account.
- **TIGER** (tiger.canceromics.org) and **TIDE** (tide.dfci.harvard.edu): processed expression with response labels.

## Things that can quietly bias cross-study validation

1. **Response definitions differ between studies.** Hugo used irRECIST, Van Allen used clinical benefit, and Riaz kept stable disease as a separate group. Decide whether stable disease counts as a responder, and apply that rule the same way in every cohort.
2. **Some samples were taken after treatment started.** Riaz and Gide include on-treatment biopsies, so filter to pre-treatment samples explicitly.
3. **Prior treatment and combination therapy vary.** Riaz has ipilimumab-progressed patients and Gide includes combination therapy. Stratify on these or report them.
4. **The same patients can appear twice.** Patients may show up in both the curated collections and the original deposits, and the DFCI melanoma cohorts may share patients. Deduplicate before you treat two datasets as independent.
5. **Expression units and pipelines differ.** Studies ship FPKM, TPM or counts from different pipelines. Where you can, reprocess from FASTQ with one pipeline: Gide, Kim, Hugo and Riaz all have raw data. Otherwise, use rank-based or within-sample features so the model stays robust across batches.

A good holdout is leaving out a whole cancer type, for example training on melanoma and testing on IMvigor210 and Braun. Reviewers will ask for it.