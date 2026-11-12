I'm answering from memory and haven't checked live, so confirm each accession and access status before you build on it. Access terms do change.

## Download now (open access)

| Cohort | Cancer / treatment | n (pre-treatment RNA-seq, approx.) | Where |
|---|---|---|---|
| Riaz 2017 | Melanoma, nivolumab | ~50 | GEO GSE91061 (counts/FPKM), clinical in the paper's supplement |
| Hugo 2016 | Melanoma, pembrolizumab | ~25–28 | GEO GSE78220 (FPKM) |
| Gide 2019 | Melanoma, anti-PD-1 ± anti-CTLA-4 | ~70 | ENA PRJEB23709, with processed tables in the supplement |
| Kim 2018 | Gastric, pembrolizumab | ~45 | ENA PRJEB25780, clinical in the supplement |
| IMvigor210 (Mariathasan 2018) | Urothelial, atezolizumab | ~300 | The `IMvigor210CoreBiologies` R package from Genentech has counts and clinical data. Raw data are on EGA (EGAS00001002556). |
| Jung 2019 / Cho 2020 | NSCLC, anti-PD-(L)1 | ~15–30 each | GEO (GSE135222, GSE126044) |
| Zhao 2019 | Glioblastoma, anti-PD-1 | ~20 | SRA (PRJNA482620) |

The NSCLC and glioblastoma sets are too small to validate on alone. They are only useful for pooling.

## Controlled access (you have to apply)

- **dbGaP (phs000452):** This covers Van Allen 2015 (ipilimumab, melanoma) and Liu 2019 (anti-PD-1, melanoma, ~120 with RNA-seq). You need an eRA Commons account and a data access request co-signed by your institution's signing official. Expect weeks to a couple of months.
- **EGA:** Braun 2020 (ccRCC, nivolumab, CheckMate 009/010/025, ~300 with RNA-seq) and IMmotion150 (atezolizumab, RCC) sit behind a Data Access Committee. Check each paper's data availability statement for the current accession.
- Some of the processed expression matrices for these cohorts are in the supplements, so check before you apply.

## Harmonized collections

These save a lot of reprocessing time. Check how each one handles licensing and response definitions.
- **CRI iAtlas** (cri-iatlas.org) has several harmonized ICI cohorts, including Riaz, Hugo, Gide, Van Allen and IMvigor210.
- **TIDE** (tide.dfci.harvard.edu) has curated ICI datasets with response labels.
- **TIGER** and **ICBatlas** are curated ICI transcriptome resources. Verify that they are still maintained.
- **Kaplan-Meier Plotter** has an immunotherapy module, but it is mostly useful for exploration, not training.

## Pitfalls for cross-study validation

1. **Overlapping patients:** Liu 2019 and Van Allen 2015 share patients, and some melanoma cohorts overlap in other ways. Deduplicate, or you'll leak data between your training and validation sets.
2. **Pre-treatment samples only:** Riaz and Gide include on-treatment biopsies. Filter them out.
3. **Mixed treatments and prior therapy:** Riaz splits patients by ipilimumab-naive versus progressed. Gide mixes monotherapy and combination. Treat these as covariates, or stratify.
4. **Response definitions:** Studies use RECIST with different cutoffs, "clinical benefit" with different follow-up windows, or both. Harmonize explicitly (for example, CR/PR versus SD/PD).
5. **Batch effects:** Library prep, platform and normalization differ between cohorts. Reprocess from raw reads where you can. If you can't, rank-normalize within each cohort.
6. **Melanoma dominance:** Most of the data is melanoma. Leave-one-cohort-out validation will mostly test melanoma-to-melanoma transfer, and urothelial, gastric and RCC are your real out-of-tissue tests.
7. **No untreated control arm:** A signature that predicts response here may just be prognostic. If that matters for your claims, check it against TCGA survival in untreated patients.

I can do a live search to verify the current accessions and access status for any of these, or draft the dbGaP and EGA access requests. Tell me which you'd like.