There are about 12 cohorts you can download today, across melanoma, urothelial, kidney, gastric, glioblastoma and lung cancer. That is enough for leave-one-study-out validation. Most of the very large trial cohorts need an application, and lung cancer is where that hurts most.

I checked every link and accession today (2026-11-12). Anything marked "from memory" is something I couldn't confirm today. GEO's web pages blocked automated access, so I confirmed the GEO series through NCBI's programmatic API instead (title and sample count for each).

## What I assumed you need
- **R1 (must):** patients actually treated with anti-PD-1, anti-PD-L1 or anti-CTLA-4
- **R2 (must):** bulk tumour RNA-seq, before treatment
- **R3 (must):** a response label for each patient (RECIST or clinical benefit)
- **R4 (preferred):** downloadable now; if not, the application route stated
- I assumed microarray and NanoString data don't count, and that trials combining a checkpoint inhibitor with other drugs count for less.

## Shortlist

**Download today**

| # | Cohort | Cancer / drug | Data | Access | Checked |
|---|---|---|---|---|---|
| 1 | **Riaz 2017**, GSE91061 | Melanoma, nivolumab | 109 samples, before and during treatment | Open | today |
| 2 | **Gide 2019**, ENA PRJEB23709 | Melanoma, anti-PD-1 with or without ipilimumab | 91 runs, raw FASTQ only | Open | today |
| 3 | **IMvigor210CoreBiologies** (R package) | Urothelial, atezolizumab | 368 patients, processed counts plus clinical data | Open | today |
| 4 | **Braun 2020**, CheckMate 009/010/025 | Kidney (clear cell), nivolumab vs everolimus | Normalised RNA-seq in Supplementary Table 4 | Open (journal supplement) | today |
| 5 | **Rose 2021**, GSE176307 | Urothelial, anti-PD-1/PD-L1 | 90 samples | Open | today |
| 6 | **Hugo 2016**, GSE78220 | Melanoma, anti-PD-1 | 28 samples, before treatment | Open | today |
| 7 | **Kim 2018**, ENA PRJEB25780 | Gastric, pembrolizumab | 188 runs, including whole-exome; about 45 RNA-seq patients (from memory) | Open, raw only | today |
| 8 | **Cloughesy 2019**, GSE121810 | Glioblastoma, pembrolizumab before surgery | 29 samples; outcome is survival | Open | today |
| 9 | **Auslander 2018**, GSE115821 | Melanoma, anti-PD-1/anti-CTLA-4 | 37 samples, mixed timepoints | Open | today |
| 10 | **Jung 2019**, GSE135222 | Lung (NSCLC), anti-PD-(L)1 | 27 samples; benefit defined by PFS | Open | today |
| 11 | **Hwang 2020**, GSE136961 | Lung (NSCLC), anti-PD-1 | 21 samples; durable clinical benefit | Open | today |
| 12 | **Cho 2020**, GSE126044 | Lung (NSCLC), anti-PD-1 | 16 samples | Open | today |

**Application needed**

| # | Cohort | Cancer / drug | Data | Access | Checked |
|---|---|---|---|---|---|
| 13 | **SU2C-MARK** (Ravi 2023), dbGaP phs002822 | Lung (NSCLC), anti-PD-(L)1 | 393 patients with whole-exome and/or RNA-seq | dbGaP request, a few weeks | today |
| 14 | **Liu 2019 / Van Allen 2015**, dbGaP phs000452 | Melanoma, anti-PD-1 (about 120) and ipilimumab (about 40) | RNA-seq | Raw reads via dbGaP request; processed tables in the paper supplements (from memory) | today |
| 15 | IMvigor210 raw reads, EGA EGAS00001002556 | Urothelial, atezolizumab | Raw FASTQ | EGA access committee (Genentech), months | today |
| 16 | IMmotion150 (McDermott 2018) | Kidney, atezolizumab with or without bevacizumab | RNA-seq | EGA access committee | from memory |
| 17 | OAK/POPLAR (Patil 2022) | Lung (NSCLC), atezolizumab vs docetaxel | RNA-seq | EGA, Genentech committee | from memory |
| 18 | JAVELIN Renal 101 (Motzer 2020) | Kidney, avelumab plus axitinib | RNA-seq | Request to Pfizer | from memory |

## Details that matter for your design
- **Response labels usually aren't in GEO or ENA.** For Riaz, Gide, Kim, Hugo and Rose they are in the papers' supplementary clinical tables. IMvigor210 is the exception: best overall response is in the package's sample annotation (from memory).
- **Platform effects:** IMvigor210 used a capture-based library method (TruSeq RNA Access), not the usual poly-A method. Gide and Kim give you raw FASTQ only. Reprocessing everything with one pipeline (for example salmon) will help cross-study transfer.
- **Only keep pre-treatment samples.** Riaz, Auslander and Cloughesy mix in samples taken during treatment, or after treatment before surgery.
- **Possible patient overlap:** GSE135222 and GSE136961 are both Korean lung cancer cohorts, so check for shared patients before using one to validate the other.
- **Liu 2019:** the paper says "Raw sequencing data are available in dbGaP (accession number phs000452.v3.p1)." Its processed expression table in the supplement (from memory) means you can start before any approval.
- **SU2C-MARK:** use limits vary by contributing hospital (some disease-specific only, some general research). Samples from Cleveland Clinic and UC Davis were not deposited.
- **Braun 2020:** the paper says "Normalized RNA-seq expression data … are available in Supplementary Table 4." There are no raw RNA-seq reads. Exome data are at EGA (EGAS00001004290 to EGAS00001004292) under controlled access.
- **Licences:** I couldn't confirm the IMvigor210 package licence today (CC BY 3.0 from memory; check the package's DESCRIPTION file). Journal supplements fall under the publisher's reuse terms.
- **Benchmark papers worth reading:** two comparisons of published expression-based response markers (Cancers 2021, doi:10.3390/cancers13071639, and Cancers 2023, doi:10.3390/cancers15164094, which curated 29 cohorts with about 1,400 patients). There is also a meta-analysis of six bladder cancer cohorts (Nat Commun 2025, doi:10.1038/s41467-025-56462-0). Their cohort tables are a good way to find what I missed.

## Not recommended, and why
- **GSE93157 and GSE173839:** NanoString panel and microarray, not RNA-seq. GSE173839 also combines the checkpoint inhibitor with a PARP inhibitor and chemotherapy.
- **GSE165252 (PERFECT trial):** atezolizumab was given with chemoradiotherapy, so response can't be credited to the checkpoint inhibitor.
- **GSE100797 (Lauss 2017):** adoptive T-cell therapy, not checkpoint inhibitors (from memory).
- **Compendia (CPI1000+, TIGER, CRI iAtlas, TIDE):** these re-process the same cohorts listed above. They are handy for harmonised matrices but are not independent cohorts, so don't count them as extra validation sets.

## What I couldn't find
- An open, large lung cancer cohort. The big ones (SU2C-MARK, OAK/POPLAR) all need applications.
- Many anti-CTLA-4-only RNA-seq cohorts beyond Van Allen 2015.
- I couldn't confirm the access terms for IMmotion150, OAK/POPLAR or JAVELIN today.

## Next step
1. Download cohorts 1–8 and 10–12, plus the Liu and Van Allen supplement tables.
2. Reprocess the raw-only sets (Gide, Kim) with the same pipeline as the rest.
3. File the dbGaP request for SU2C-MARK now, since it takes weeks, and use it as a held-out lung cancer test set.

I also built an interactive version of this list, where you can filter the cohorts and export an access plan: `/private/tmp/e-SBuduR/home/cwd/dataset-shortlist.html`