Several good cohorts are fully open, and a few aggregator resources have already reprocessed most of them. I'm writing this from memory and didn't check the links in this session, so confirm each accession on its landing page before you build a pipeline around it. The ones I'm less sure of are marked "(verify)".

## Download right away (open access)

| Cohort | Cancer / drug | ~Patients with RNA-seq | Where | What you get |
|---|---|---|---|---|
| **Mariathasan 2018 (IMvigor210)** | Urothelial, atezolizumab (anti-PD-L1) | ~350 | Bioconductor-style R package `IMvigor210CoreBiologies` (from the Genentech/research-pub site) | Processed counts + RECIST + overall survival. Raw data is on EGA (controlled). Biggest single cohort, so a good anchor. |
| **Gide 2019** | Melanoma, anti-PD-1 ± ipilimumab | ~90 samples (pre and some on-treatment) | ENA **PRJEB23709** | Raw FASTQ. Clinical data is in the paper's supplement. |
| **Riaz 2017 (CheckMate 038)** | Melanoma, nivolumab; ipilimumab-naive and ipilimumab-progressed arms | ~50 pre-treatment, plus on-treatment | GEO **GSE91061**; raw on SRA (PRJNA356761) | Counts/FPKM. Response is in the supplement and GitHub (riazn/bms038_analysis). |
| **Hugo 2016** | Melanoma, anti-PD-1 | 28 | GEO **GSE78220** | FPKM; raw on SRA |
| **Kim 2018** | Gastric, pembrolizumab | ~45 | ENA **PRJEB25780** | Raw FASTQ |
| **Rose 2021** | Urothelial, anti-PD-1/PD-L1 | ~90 | GEO **GSE176307** (verify) | Processed expression |
| **Braun 2020 (CheckMate 009/010/025)** | ccRCC, nivolumab vs everolimus | ~180 on the nivolumab arms | Nat Med supplement | Processed expression and clinical data in the supplement; raw is controlled |
| **Small NSCLC cohorts** | NSCLC, anti-PD-1 | 16–30 each | GEO **GSE126044** (Cho), **GSE135222** (Jung), **GSE136961** (Hwang) (verify) | Processed. Small, but they add cancer-type diversity. |
| **Zhao 2019 / Cloughesy 2019** | GBM, anti-PD-1 (incl. neoadjuvant) | ~15–30 | SRA PRJNA482620 / GEO GSE121810 | Response is weak in GBM, so these are better as negative controls than as training data |

## Have to apply (dbGaP / EGA)

- **Van Allen 2015** (melanoma, anti-CTLA-4) and **Liu 2019** (melanoma, anti-PD-1, ~120 with RNA-seq): dbGaP **phs000452**. Both papers' supplements include processed TPM, which is usually enough for a classifier. Apply only if you want uniform reprocessing from raw.
- **Miao 2018** (ccRCC), **Snyder 2017** (urothelial), **Nathanson 2017** (melanoma, anti-CTLA-4): dbGaP. Some processed data is in the supplements or cBioPortal.
- **Atezolizumab NSCLC trials OAK/POPLAR** (Patil 2022, Cancer Cell): EGA, roughly 900 patients. This is the largest NSCLC resource, but access goes through a Roche data access committee.
- **JAVELIN Renal 101** (Motzer 2020, avelumab + axitinib) and **IMmotion150/151** (ccRCC, atezolizumab ± bevacizumab): EGA, controlled.
- **Ravi 2023 SU2C-MARK** (NSCLC, ~150 with RNA-seq): raw data is controlled; check the supplement and GitHub for processed matrices (verify).

dbGaP typically takes 4–8 weeks and needs an institutional signing official. EGA committees vary a lot, and industry-trial data is the slowest.

## Already-harmonised collections (fastest start)

- **CRI iAtlas, ICI module** (iatlas.org; data on Synapse): harmonised expression and response for about a dozen cohorts. It covers many of the ones above, including some controlled cohorts in processed form.
- **TIGER** (tiger.canceromics.org): bulk and single-cell ICI cohorts with response labels.
- **TIDE** (tide.dfci.harvard.edu): processed ICI cohorts used to benchmark TIDE.
- **ICBatlas** and **CAMOIP**: similar portals.
- **Litchfield 2021 (Cell, "CPI1000+")**: a meta-analysis with processed data on Zenodo, covering about 1,000 patients across 12 cohorts (RNA-seq for a subset).

These save a lot of work. Still, I'd re-derive at least the response labels and sample selection from the original papers, because harmonisation choices differ between portals.

## Pitfalls for cross-study validation

1. **Use pre-treatment samples only.** Riaz, Gide and others mix pre- and on-treatment samples in the same series.
2. **Response definitions differ.** Some studies use RECIST CR/PR vs SD/PD. Others use "clinical benefit", which can count SD lasting at least 6 months, and Van Allen and Liu use their own definitions. Pick one rule and reapply it to every cohort where the data allows. Decide explicitly where stable disease goes.
3. **Prior treatment.** Riaz splits patients by prior ipilimumab, and Gide mixes monotherapy with combination therapy. Treat these as covariates or analyse them as separate strata.
4. **Overlapping patients.** Aggregators and meta-analyses can include the same patients under different IDs. Most published response signatures, such as TIDE and IMPRES, were also built or tuned on exactly these cohorts. A truly held-out validation set is harder to find than it looks, so record which cohorts each comparator signature has already seen.
5. **Batch and platform effects.** Studies differ in poly-A vs capture library prep, FFPE vs fresh-frozen tissue, and processing (FPKM vs TPM vs counts). Rank-based or within-sample features hold up better across studies than z-scores across samples. Leave-one-cohort-out validation is the honest test.
6. **Imbalance by cancer type.** Melanoma dominates the open data. IMvigor210 is about 3× bigger than any other single cohort, so weight or stratify for it, or it will drive your model.

## Suggested starting set

Today you can download IMvigor210, Gide, Riaz, Hugo, Kim and Braun, plus the Liu and Van Allen supplementary TPMs. That gives you roughly 750 patients across 4 cancer types, which is enough for leave-one-cohort-out validation with no data access applications. File the dbGaP request for phs000452 and an EGA request for OAK/POPLAR now if you want raw data or a large NSCLC test set later.

I can also write a script that pulls the open cohorts, harmonises gene IDs and response labels, and runs a leave-one-cohort-out setup.