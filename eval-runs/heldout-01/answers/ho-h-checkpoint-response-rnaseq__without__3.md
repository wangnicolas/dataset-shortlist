I'm answering from memory and haven't checked these against the live repositories. Confirm each accession and its access terms before you build a pipeline on it. All the cohorts below have pre-treatment bulk RNA-seq and a recorded response.

## Download now (open access)

| Cohort | Cancer / drug | n (approx.) | Where |
|---|---|---|---|
| Hugo 2016 | Melanoma, pembrolizumab | ~27 | GEO GSE78220 (FPKM) |
| Riaz 2017 | Melanoma, nivolumab | ~50 pre-treatment | GEO GSE91061 (counts/FPKM); clinical data in the supplement |
| Gide 2019 | Melanoma, anti-PD-1 ± anti-CTLA-4 | ~90 | ENA PRJEB23709; processed matrix and clinical data in the supplement |
| Auslander 2018 | Melanoma, anti-PD-1 and anti-CTLA-4 | ~40 | GEO GSE115821 |
| Kim 2018 | Gastric, pembrolizumab | ~45 | ENA PRJEB25780 |
| Kim/Jung 2019 | NSCLC, anti-PD-1 | ~25–30 | GEO GSE135222 |
| Cho 2020 | NSCLC, anti-PD-1 | ~16 | GEO GSE126044 |
| Zhao 2019 | Glioblastoma, anti-PD-1 | ~30 | SRA PRJNA482620; clinical data in the supplement |
| Mariathasan 2018 (IMvigor210) | Urothelial, atezolizumab | ~300 | `IMvigor210CoreBiologies` R package, which has counts and clinical data. This is the largest open cohort. |

## Controlled access (apply)

- **Liu 2019** is melanoma anti-PD-1 with ~120 patients. The raw data are in dbGaP phs000452, and you apply through a DAC. Check whether the supplement has processed expression.
- **Van Allen 2015** is melanoma ipilimumab, also in dbGaP phs000452. It is mostly exome, so check how much RNA-seq it has.
- **Braun 2020** is ccRCC nivolumab (CheckMate 009/010/025), with raw data in EGA. Clinical data and some processed data are in the paper.
- **IMmotion150** is RCC atezolizumab ± bevacizumab, in EGA (EGAS00001002928).
- **IMvigor210 raw reads** are in EGA (EGAS00001002556). You don't need these if the R package is enough.

EGA and dbGaP approvals usually take weeks to months. Start them early if you need these cohorts.

## Curated aggregators (a good place to start)

- **CRI iAtlas** (cri-iatlas.org) has harmonised ICI cohorts with clinical data.
- **TIDE** (tide.dfci.harvard.edu) has curated expression and response for several of the cohorts above.
- **PredictIO** (Bareche et al., 2022) is a curated ICI transcriptomic compendium with an R interface.

These are convenient, but check their processing and response definitions against the original papers.

## Pitfalls for cross-study validation

- **Timepoint:** Riaz and Auslander include on-treatment biopsies. Keep only pre-treatment samples.
- **Prior therapy:** Riaz includes patients who had prior ipilimumab. Hugo and others are mixed. Decide whether to stratify or exclude.
- **Response definitions:** RECIST (CR/PR vs SD/PD) is not the same as clinical benefit (durable SD, PFS cutoffs). Harmonise explicitly.
- **Drug and regimen:** Gide includes combination therapy, and IMvigor210 is anti-PD-L1. Mixing these will affect generalisation.
- **Overlap:** Check for duplicated patients across the melanoma cohorts, since some were reused in later papers.
- **Technical differences:** Platforms, normalisation and counts vs FPKM all differ. Reprocess raw reads where possible, or use rank-based features.
- **Cancer type:** Melanoma dominates, so leave-one-cohort-out validation will mostly be melanoma-on-melanoma. Gastric, NSCLC, urothelial and RCC cohorts will test transfer to other cancers.

I can check any of these accessions live if you want. I can also draft a harmonisation script for the open cohorts.