## What I assumed you need

- **R1 (must):** patients actually treated with anti-PD-1/PD-L1 and/or anti-CTLA-4.
- **R2 (must):** pre-treatment bulk tumour RNA-seq, as an expression matrix or raw reads.
- **R3 (must):** per-patient clinical response (RECIST category or clinical benefit).
- **R4 (nice):** roughly 25 or more labelled pre-treatment patients per cohort (my assumption).
- **R5 (nice):** downloadable today.

About ten independent cohorts are open today, covering melanoma, urothelial, kidney, gastric and small lung sets. The large lung, liver and second kidney trial cohorts need an application. Everything was checked on 11 Nov 2026 (UTC) unless marked "from memory".

## Shortlist

| # | Dataset | Access | Licence | Size (pre-treatment, with response) | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | ORCESTRA / PredictIO curated collection (Zenodo) | Direct download | CC BY 4.0 / CC0 (uploader's label) | ~20 cohorts in one merged table | Strong | today |
| 2 | cBioPortal "iAtlas Harmonized" ICI studies (9) | Direct download or API, no login | ODbL (share-alike) | IMvigor210 347, IMmotion150 263, Liu 122, Gide 73, PRINCE 64, Riaz 51, three smaller | Strong | today |
| 3 | IMvigor210CoreBiologies (urothelial, atezolizumab) | Direct download | CC 3.0, from memory | 348 tumours, 298 with response | Strong | page today, licence from memory |
| 4 | Braun 2020 ccRCC, nivolumab (CheckMate 009/010/025) | Direct download (processed) | CC0 label on Zenodo copy | ~180 nivolumab-treated, from memory | Strong | record today, counts from memory |
| 5 | Riaz 2017 melanoma, nivolumab (GSE91061) | Direct download | None stated (GEO) | 51 pre (109 samples in total) | Strong | today, via NCBI API |
| 6 | Gide 2019 melanoma, PD-1 ± CTLA-4 (ENA PRJEB23709) | Direct download, raw FASTQ | None stated | 73 pre (91 runs) | Strong | today |
| 7 | Liu 2019 melanoma, anti-PD-1 (paper supplement) | Direct download (processed) | Publisher terms | ~121 | Strong | today |
| 8 | Rose 2021 urothelial, UNC-108 (GSE176307) | Direct download | None stated | 90 samples | Strong, label column unchecked | today, via NCBI API |
| 9 | Kim 2018 gastric, pembrolizumab (ENA PRJEB25780) | Direct download, raw FASTQ | None stated | 45 patients (78 RNA-seq runs) | Strong | today |
| 10 | Hugo 2016 melanoma, anti-PD-1 (GSE78220) | Direct download | None stated | 28 samples | Partial (small) | today, via NCBI API |
| 11 | Small NSCLC sets: GSE135222, GSE126044, GSE136961 | Direct download | None stated | 27, 16, 21 | Partial (small) | today, via NCBI API |
| 12 | OAK + POPLAR NSCLC, atezolizumab vs docetaxel (EGA) | Application to Genentech's committee, ~months | Data access agreement | 891 tumours, both arms | Strong | today |
| 13 | IMmotion151 RCC, atezolizumab + bevacizumab (EGA) | Same Genentech route, ~months | Data access agreement | 823 tumours | Strong | today |
| 14 | IMbrave150 / GO30140 liver cancer (EGA) | Same Genentech route, ~months | Data access agreement | 372 RNA-seq samples | Strong | today |
| 15 | SU2C-MARK NSCLC (dbGaP phs002822) | dbGaP application via PI and institution, ~weeks | NIH Data Use Certification | 90–150, from memory | Strong | today |
| 16 | Van Allen 2015 / Miao 2018 raw reads (dbGaP phs000452, phs001493) | dbGaP application; processed copies open | NIH Data Use Certification | 42 and 33 | Partial | today |
| 17 | Hartwig Medical Foundation (pan-cancer, metastatic) | Institutional licence and board review, ~months | Licence agreement | ICI subset with RNA-seq unknown | Partial | access today, contents from memory |

## Details

**Open today**

1. **ORCESTRA / PredictIO collection** — merged table at https://zenodo.org/records/7459023 (`merged_expr.tsv` 330 MB, `merged_metadata.tsv`).
   - Per-cohort R objects are also on Zenodo, e.g. [ICB_Braun](https://zenodo.org/records/7332074), ICB_Gide (7332096), ICB_Riaz (7332230), ICB_Liu (7332172), ICB_Mariathasan (7332183), ICB_Hugo (7332108), ICB_Van_Allen (7332289), ICB_Kim (7332153), ICB_Jung (7332134).
   - It contains about 20 cohorts; a few are DNA-only (Rizvi, Samstein, Roh, from memory), and ICB_Samstein is restricted.
   - It is a 2022 snapshot, built for Bareche et al., Ann Oncol 2022 (doi:10.1016/j.annonc.2022.08.084).
   - The same collection on Health Data Nexus requires credentialing and a data use agreement; the Zenodo records do not.

2. **cBioPortal iAtlas-harmonized studies** — https://www.cbioportal.org/datasets (search "iAtlas") or https://github.com/cBioPortal/datahub.
   - Study IDs: `blca_iatlas_imvigor210_2017`, `rcc_iatlas_immotion150_2018`, `mel_iatlas_liu_2019`, `mel_iatlas_gide_2019`, `mel_iatlas_riaz_nivolumab_2017`, `paad_iatlas_prince_2022`, `brca_iatlas_anders_2022`, `ccrcc_iatlas_choueiri_2016`, `gbm_iatlas_prins_2019`.
   - All nine were processed through one pipeline and carry `RESPONSE` (CR/PR/SD/PD), `RESPONDER` and `CLINICAL_BENEFIT` fields.
   - This is the only open route I found to IMmotion150 (CR 19 / PR 53 / SD 96 / PD 79); its raw data are behind Genentech's committee.
   - Drop the non-ICI arms: 89 sunitinib patients in IMmotion150 and 24 in PRINCE.
   - `TIDE_RESPONDER` is a computed prediction, not an outcome; do not use it as a label.
   - Prins (glioblastoma) has no responders, and PRINCE is nivolumab plus chemotherapy.

3. **IMvigor210CoreBiologies** — http://research-pub.gene.com/IMvigor210CoreBiologies/. This is the sponsor's own R package with counts and best confirmed response (CR 25 / PR 43 / SD 63 / PD 167). It depends on old Bioconductor packages, so installation can be fiddly (from memory).

4. **Braun 2020** — paper at https://doi.org/10.1038/s41591-020-0839-y; the processed object is ICB_Braun above. Remove the everolimus control arm of CheckMate 025 (from memory). Raw reads are at EGA (EGAS00001004290, 4291, 4292) by application.

5. **Riaz** — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061. Of 109 samples, 56 are on-treatment; keep only the 51 pre-treatment ones.

6. **Gide** — https://www.ebi.ac.uk/ena/browser/view/PRJEB23709. ENA holds reads only; take labels from the Cancer Cell 2019 supplement or the harmonized copies (CR 17 / PR 32 / SD 13 / PD 29).

7. **Liu** — https://doi.org/10.1038/s41591-019-0654-5. The data availability statement says "All analyzed sequencing data are in supplementary tables or data available online"; raw reads are in dbGaP phs000452.

8. **Rose / UNC-108** — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE176307. This is a real-world bladder cohort and the natural external test for an IMvigor210-trained model. I could not open the series matrix, so confirm which column holds response.

9. **Kim gastric** — https://www.ebi.ac.uk/ena/browser/view/PRJEB25780. Response is dominated by MSI-high and EBV-positive tumours, so a model can score well here just by detecting those subtypes.

10. **Hugo and the small NSCLC sets** — GSE78220, GSE135222, GSE126044, GSE136961. Use these as hold-outs only. GSE135222 and GSE126044 come from related Korean groups, so check for shared patients. GSE136961 may be a targeted panel; check the platform.

**Need an application**

11. **Genentech trials on EGA (rows 12–14)** — [OAK/POPLAR](https://ega-archive.org/studies/EGAS00001005013), [IMmotion151](https://ega-archive.org/studies/EGAS00001004353), [IMbrave150](https://ega-archive.org/studies/EGAS00001005503).
    - Steps: create an EGA account, click "Request access" on each dataset, e-mail the Genentech committee (address on the dataset page) with a project description, then sign their agreement.
    - Raw data for IMvigor210 and IMmotion150 sit with the same Genentech contact, so ask for everything in one request.
    - Expect one to several months and an institutional signature (from memory).
    - The control arms (docetaxel, sunitinib, sorafenib) let you separate predictive from prognostic signal.

12. **dbGaP (rows 15–16)** — [phs002822](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs002822), [phs001493](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001493), [phs000452](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000452).
    - Your PI submits the request through eRA Commons, and the institution's signing official co-signs the Data Use Certification.
    - As a postdoc you are usually added as a downloader rather than being the requester (from memory).
    - One request can bundle all three studies; allow two to six weeks.

13. **Hartwig** — https://www.hartwigmedicalfoundation.nl/en/data/data-access-request/. E-mail dataaccess@hartwigmedicalfoundation.nl, submit a proposal, and the institution signs a licence after board review. It is free for research institutes. Ask how many ICI-treated patients have RNA-seq before applying.

Evidence of use: IC2Bert (Sci Rep 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12313928/) trains a response classifier on 13 of these cohorts, 1,214 patients in total.

## Known, not confirmed

- **JAVELIN Renal 101** (avelumab + axitinib vs sunitinib, ~726 patients) — https://doi.org/10.1038/s41591-020-1044-8. I recall per-patient expression and PFS in the supplement, but the page required a login today. Check Supplementary Tables for expression and whether objective response is included.
- **SU2C-MARK processed tables** — these may be in the Nature Genetics 2023 supplement, which would avoid the dbGaP wait; not checked.
- **TIGER** (http://tiger.canceromics.org/), **CIDE/TIDE** (http://tide.dfci.harvard.edu/, now redirecting to cide.ccr.cancer.gov), **ICBatlas** and **IOhub** — curated portals that re-serve many of the same cohorts. The sites returned an empty JavaScript page, HTTP 403 and HTTP 502 to scripts; I believe they are free downloads (from memory).
- **INSPIRE** pan-cancer pembrolizumab (EGA EGAS00001003280, 64 patients in IC2Bert) and **HCRN kidney** (dbGaP phs003618) — both pages exist and are controlled access; I did not check their contents.

## Not recommended, and why

- **TCGA** — no checkpoint-inhibitor treatment or response; useful only for pre-training.
- **MSK-IMPACT / Samstein, Miao pan-cancer, MSK NSCLC 2018 on cBioPortal** — ICI outcomes but DNA only, with no expression profile.
- **GSE93157 (Prat) and GSE140901** — NanoString panels of about 730 genes, not RNA-seq.
- **I-SPY2 (GSE194040, GSE173839)** — microarrays, with pathological complete response to ICI plus chemotherapy as the endpoint.
- **GSE100797 (Lauss)** — adoptive T-cell therapy, not ICI.

## What I could not find

- A sizeable open lung cancer cohort; the open ones have 16–27 patients.
- Open head-and-neck, MSI-high colorectal or Merck KEYNOTE patient-level RNA-seq with response.
- The literature search returned mostly 2026 papers, so a cohort released in 2025–26 may be missing.

## Next step

Start today with the cBioPortal iAtlas set plus ICB_Braun, Rose and Kim; that gives melanoma, bladder, kidney and gastric with one copy per cohort. Many rows above are the same patients re-processed (Riaz, Gide, Liu and IMvigor210 each appear three or four times), so count each cohort once when you report independent validation.

In parallel, have your PI file the single Genentech EGA request and the single dbGaP request now, since those bring the lung and liver cohorts. It is also worth asking your institution whether secondary use of the open de-identified data needs an exemption determination.

The interactive shortlist, with filters, per-requirement evidence and an exportable access plan, is at `/private/tmp/e-YzFR8w/home/cwd/dataset-shortlist.html`.

Sources:
- [IC2Bert, Sci Rep 2025 (PMC12313928)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12313928/)
- [ICB Data TSV Files, Zenodo](https://zenodo.org/records/7459023)
- [PredictIO Sequencing Data, Zenodo](https://zenodo.org/records/6142546)
- [Immune Checkpoint Blockade (ICB) Data v1.0, Health Data Nexus](https://healthdatanexus.ai/content/icb/1.0/)
- [cBioPortal FAQ](https://docs.cbioportal.org/user-guide/faq/)
- [cBioPortal datahub](https://github.com/cBioPortal/datahub)
- [EGA: how to request data](https://ega-archive.org/access/request-data/how-to-request-data/)
- [Hartwig database](https://www.hartwigmedicalfoundation.nl/en/data/database/)
- [Current transcriptome database and biomarker discovery for ICB (IOhub), bioRxiv](https://www.biorxiv.org/content/10.1101/2024.12.09.627506v1.full)