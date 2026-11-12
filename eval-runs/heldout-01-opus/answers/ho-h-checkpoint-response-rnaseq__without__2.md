Plenty of public ICB cohorts have pre-treatment RNA-seq and response labels. The main gap is lung cancer: the large NSCLC trial cohorts are mostly controlled-access. I wrote this from memory and didn't check the accessions live, so confirm each ID and sample count when you download.

## Download right away (open access)

| Cohort | Cancer / drug | ~N with RNA + response | Where | Notes |
|---|---|---|---|---|
| **Mariathasan 2018 (IMvigor210)** | Urothelial, atezolizumab (anti-PD-L1) | ~300 | `IMvigor210CoreBiologies` R package (Genentech) | Largest open cohort: counts plus RECIST, TMB and immune phenotype. Raw reads are on EGA (controlled). Many patients had prior platinum. |
| **Riaz 2017 (CheckMate 064)** | Melanoma, nivolumab | ~50 pre-treatment | GEO **GSE91061** (raw in SRA) | Has both pre- and on-treatment samples, so keep only "Pre". Split into ipilimumab-naive vs ipilimumab-progressed patients. |
| **Hugo 2016** | Melanoma, anti-PD-1 | ~27 | GEO **GSE78220** | Small, FPKM only. |
| **Gide 2019** | Melanoma, anti-PD-1 ± anti-CTLA-4 | ~90 pre-treatment | ENA **PRJEB23709** | Raw FASTQ is open. Clinical data is in the paper's supplement. |
| **Braun 2020 (CheckMate 009/010/025)** | Clear-cell RCC, nivolumab | ~180 | Nat Med supplementary tables | Expression and clinical data are in the supplement. Includes an everolimus control arm, which is handy for checking whether a signature is ICB-specific or just prognostic. |
| **Kim 2018** | Gastric, pembrolizumab | ~45 | ENA **PRJEB25780** | Enriched for MSI-high and EBV+, which drive much of the response. |
| **Zhao 2019** | Glioblastoma, anti-PD-1 | ~30 | SRA **PRJNA482620** | |
| **Cloughesy 2019** | Glioblastoma, neoadjuvant pembrolizumab | ~30 | GEO **GSE121810** | Outcome is survival, not RECIST. |
| **Jung 2019 / Cho 2020** | NSCLC, anti-PD-(L)1 | ~27 / ~16 | GEO **GSE135222** / **GSE126044** | Small, but they are the main open NSCLC cohorts. |
| **Auslander 2018** | Melanoma, ICB | ~37 | GEO **GSE115821** | Mixed timepoints. |

**Harmonised compendia** save a lot of reprocessing:
- **ORCESTRA / PredictIO** (Bareche et al. 2022): uniformly processed ICB datasets as downloadable objects. This is probably the fastest start for cross-study validation.
- **CRI iAtlas, ICI module** (data on Synapse): harmonised expression and response for roughly 10+ cohorts.
- **TIGER** (tiger.canceromics.org) and **TIDE** (tide.dfci.harvard.edu): processed ICB cohorts you can download.
- **Litchfield 2021 (CPI1000+, Cell)**: a reprocessed meta-cohort. It's mostly the same studies listed here, so don't count it as independent validation.

## Apply first (controlled access)

| Cohort | Cancer / drug | Repository |
|---|---|---|
| Van Allen 2015 | Melanoma, ipilimumab (anti-CTLA-4), ~40 with RNA | dbGaP **phs000452** |
| Liu 2019 (Nat Med) | Melanoma, anti-PD-1, ~120 | dbGaP **phs000452** (processed matrices may be in the supplement, check) |
| Miao 2018 | ccRCC, anti-PD-(L)1 | dbGaP |
| McDermott 2018 (IMmotion150), Motzer 2020 (IMmotion151 / JAVELIN Renal 101) | RCC, atezolizumab/avelumab plus VEGF inhibitors | EGA |
| Patil 2022 (POPLAR/OAK) | NSCLC, atezolizumab, several hundred | EGA |
| Ravi 2023 (SU2C-MARK) | NSCLC, anti-PD-(L)1, ~150 | dbGaP (some processed data in the supplement) |

dbGaP approval usually takes weeks to a few months and needs an institutional signing official. EGA requests go to each study's own Data Access Committee, and pharma trial DACs can be slow or restrictive.

## Things that will bite a cross-study classifier
1. **Inconsistent labels.** Studies define "response" differently: CR/PR vs the rest, clinical benefit including durable stable disease (Van Allen), or survival only. Pick one definition, re-derive it from each study's supplementary clinical data, and report it per cohort.
2. **Timepoint leakage.** Several cohorts mix pre- and on-treatment biopsies, so filter to baseline samples explicitly.
3. **Duplicate patients.** The compendia (iAtlas, TIDE, Litchfield, PredictIO) repackage the same patients. Pick "independent" test cohorts by original study, not by portal.
4. **Batch and platform effects.** Data arrives as FPKM, TPM, counts or microarray, with poly-A or capture libraries. Rank-based or within-sample features (e.g. gene-pair or ssGSEA scores) usually transfer across studies better than z-scored expression. Leave-one-study-out cross-validation is the honest evaluation.
5. **Confounders.** Prior ipilimumab, MSI or EBV status, and combination arms (anti-PD-1 plus anti-CTLA-4, or ICB plus VEGF inhibitors) all shift response rates. Stratify by them or adjust for them.
6. **Benchmarks.** Compare against simple baselines like TMB, CD274 expression, IFN-γ/T-cell-inflamed signatures and TIDE. Reviewers will ask for them.

**Suggested start:** download IMvigor210, Braun 2020, Riaz, Gide and Hugo now, and pull the ORCESTRA/PredictIO versions to cross-check your processing. Submit the dbGaP request for phs000452 (Van Allen and Liu) at the same time, since it's the slowest step and would give you an independent anti-CTLA-4 cohort.