I found 12 cohorts you can download today with no application, covering melanoma, gastric, lung, urothelial and glioblastoma, so you can validate across studies straight away. The most valuable data for melanoma, kidney and large lung trials is under controlled access, but the processed melanoma and kidney matrices are published in the papers' supplements.

I checked everything on 2026-11-12. NCBI's GEO and dbGaP web pages blocked automated access, so I confirmed the GEO studies through NCBI's FTP server, which listed each study's files and title. Response labels and sample counts mostly come from my memory of the papers. Check them in each study's sample table or the paper's supplement.

## What I assumed you need
- **R1 (must):** patients treated with anti-PD-1/PD-L1 and/or anti-CTLA-4.
- **R2 (must):** bulk tumour RNA-seq taken before treatment.
- **R3 (must):** a response label for each patient (RECIST or clinical benefit).
- **R4 (must):** several independent cohorts.
- **R5 (nice to have):** downloadable today.

## Shortlist
| # | Cohort | Cancer / drug | Access | Size (from memory) | Checked |
|---|---|---|---|---|---|
| 1 | **IMvigor210CoreBiologies** (Mariathasan 2018) | Urothelial, atezolizumab | **Open**: R package tarball | ~348 patients, ~298 with RECIST | today (download link) |
| 2 | **Riaz 2017**, GSE91061 | Melanoma, nivolumab (with or without prior ipilimumab) | **Open**: raw counts and FPKM on GEO | 51 before / 58 during treatment, 65 patients | today (BioProject page) |
| 3 | **Gide 2019**, PRJEB23709 | Melanoma, anti-PD-1 or ipilimumab + nivolumab | **Open**: raw reads on ENA | ~90 samples | today (ENA's API) |
| 4 | **Kim 2018**, PRJEB25780 | Gastric, pembrolizumab | **Open**: raw reads on ENA | ~45 with RNA-seq, 61 patients | today (ENA's API) |
| 5 | **Hugo 2016**, GSE78220 | Melanoma, anti-PD-1 | **Open**: FPKM spreadsheet on GEO | ~28 | today |
| 6 | **Jung 2019**, GSE135222 | Lung (NSCLC), anti-PD-1/PD-L1 | **Open**: expression table on GEO | ~27; benefit defined by PFS | today |
| 7 | **Auslander 2018**, GSE115821 | Melanoma, anti-PD-1/CTLA-4 | **Open**: counts on GEO | ~37 samples, some during treatment | today |
| 8 | **Rose 2021**, GSE176307 | Urothelial, real-world ICI | **Open**: normalised data and RSEM files on GEO | response field not checked | today |
| 9 | **Snyder 2017**, Zenodo 546110 | Urothelial, atezolizumab | **Open**, CC BY 4.0, kallisto quantifications | ~25 | today (Zenodo's API) |
| 10 | **Cho 2020**, GSE126044 | Lung (NSCLC), anti-PD-1 | **Open**: counts on GEO | ~16 | today |
| 11 | Zhao 2019, PRJNA482620 | Glioblastoma, anti-PD-1 | **Open**: raw reads on SRA (open status from memory) | small; response is not RECIST | today (page exists) |
| 12 | Cloughesy 2019, GSE121810 | Glioblastoma, neoadjuvant pembrolizumab | **Open** | small; outcome is survival, not response | today |
| 13 | **Liu 2019 + Van Allen 2015**, dbGaP phs000452 | Melanoma, anti-PD-1 / ipilimumab | Raw data: **dbGaP application, weeks**. Processed TPM + clinical table: **open in the Nat Med supplement** (from memory) | ~120 (Liu) + ~40 (Van Allen) | page exists; terms from memory |
| 14 | **Braun 2020** (CheckMate 009/010/025), Miao 2018 | Kidney (RCC), nivolumab | Raw data: **dbGaP application** (page says "Request access via Authorized Access", "Data Use Certification Agreement"). Processed data: open in the supplement (from memory) | ~180 | today (dbGaP page read) |
| 15 | **OAK/POPLAR** (Patil 2022), EGAS00001005013 | NSCLC, atezolizumab vs docetaxel | **Data Access Committee (DAC) application, months** | ~900, randomised | today (EGA page) |
| 16 | IMvigor210 raw reads, EGAS00001002556 | Urothelial | **DAC application** | same patients as #1 | today (EGA page) |

## Details that matter
- **IMvigor210:** download `http://research-pub.gene.com/IMvigor210CoreBiologies/IMvigor210CoreBiologies.tar.gz`. It contains counts plus best overall response (`binaryResponse`), mutation burden (TMB) and immune phenotype. The package depends on old Bioconductor versions. If installing it fails, load the `.rda` files directly. I believe the licence is CC BY 3.0 (from memory).
- **Riaz, Hugo, Auslander, Jung, Cho, Rose:** the GEO supplementary files exist (I saw the file listings). For Riaz, the per-patient best overall response is in the paper's supplementary table, not in GEO. Match on patient ID.
- **Gide and Kim:** raw FASTQ only, so plan a day to quantify them with salmon. Run Riaz and Hugo's raw reads (also open on SRA, from memory) through the same pipeline to cut down batch effects.
- **Liu 2019 / Braun 2020:** most published classifiers use the processed matrices from the supplements, so you can use these cohorts now without dbGaP. You only need a dbGaP application (eRA Commons login plus your institution's signing official, typically 2–6 weeks) if you want uniform reprocessing from raw reads.
- **OAK/POPLAR:** this is the strongest validation set because it is large and randomised against docetaxel, which separates "predicts ICI benefit" from "just prognostic". Access goes through an EGA application to the Roche/Genentech access committee, which takes months and isn't guaranteed.
- **Shortcuts:** CRI iAtlas (its site lists 23 ICI datasets; confirmed today), TIGER (tiger.canceromics.org) and TIDE already host harmonised versions of most of the open cohorts. They're useful for cross-checking your labels. I'd still build from the original sources so you control the processing.

## Known, not confirmed
- **JAVELIN Renal 101** (avelumab + axitinib) and **IMmotion150/151** (atezolizumab, RCC): these are on EGA under controlled access, from memory. The EGA accession I tried pointed to an unrelated prostate study, so look up the correct accession in the papers' data statements.
- **Ravi 2023 SU2C-MARK NSCLC** (Nat Genet; 393 patients with WES and/or RNA-seq and response): it came up in the literature search. I didn't check how to get the data.
- **Snyder 2017** may partly overlap with IMvigor210 patients. Check before treating it as an independent cohort.

## Not recommended
- **TCGA:** patients weren't treated with checkpoint inhibitors.
- **MSK-IMPACT / Samstein 2019:** DNA panel only, no RNA.
- **Rizvi 2015 and Le 2015:** exome sequencing only.
- **Prat 2017:** NanoString panel, not RNA-seq.
- **Zenodo "Immunotherapy Clonal Dynamics Cohort":** a commercial vendor's free sample with unclear provenance.

## Next step
A practical split:
- **Training:** Liu 2019 (supplement) + Riaz + Gide + Hugo, all melanoma.
- **Validation in other cancers:** IMvigor210, Kim gastric, Braun RCC (supplement), and Jung/Cho NSCLC.
- **Application to start now:** OAK/POPLAR, for the randomised predictive-vs-prognostic test.

I didn't check the per-sample response fields for Rose (GSE176307) and Cho (GSE126044), so look at those first.

The interactive shortlist is at `/private/tmp/e-uFqWsj/home/cwd/dataset-shortlist.html`. The working files, including the list of everything checked, are in `dataset-scout/`.