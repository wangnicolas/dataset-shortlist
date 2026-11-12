Everything below is from memory. I haven't checked any accession or access policy in this session, so confirm each one before you build on it. Several of the access terms have changed over the years.

## Download now (open: GEO, ENA, or supplementary tables)

| Cohort | Cancer / drug | Approx. n | Where |
|---|---|---|---|
| Hugo 2016 | Melanoma, anti-PD-1 | ~28 | GEO GSE78220 (FPKM) |
| Riaz 2017 | Melanoma, nivolumab (pre and on-treatment, some ipilimumab-pretreated) | ~100 | GEO GSE91061 |
| Gide 2019 | Melanoma, anti-PD-1 or anti-PD-1 + anti-CTLA-4 | ~90 | ENA PRJEB23709 |
| Kim 2018 | Gastric, pembrolizumab | ~45 | ENA PRJEB25780 |
| Auslander 2018 | Melanoma, anti-PD-1 | small | GEO GSE115821 |
| Cloughesy 2019 | Glioblastoma, neoadjuvant pembrolizumab | small | GEO (check the paper) |
| IMvigor210 | Urothelial, atezolizumab | ~300 | `IMvigor210CoreBiologies` R package from Genentech, with counts and clinical data. Raw data is on EGA. |

IMvigor210 is the largest cohort you can get quickly. The package's hosting and license have changed before, so check that it still works.

## Apply for access (controlled)

- **Van Allen 2015 (ipilimumab) and Liu 2019 (anti-PD-1), melanoma:** dbGaP phs000452. Check whether Liu's processed expression is in the supplementary tables, since that would let you skip the application.
- **Genentech trials on EGA:** IMmotion150 (RCC), IMmotion151, POPLAR/OAK (NSCLC), and the raw IMvigor210 data. These need a Data Access Committee application and data transfer agreement.
- **Braun 2020 (ccRCC, nivolumab, CheckMate 009/010/025):** the clinical and processed data are partly in the supplement. The raw data is controlled, so check the data availability statement.
- **BMS trials (e.g. CheckMate):** apply through BMS's data-sharing portal or Vivli. Expect slow turnaround.
- **Hartwig Medical Foundation and POG570:** metastatic WGS plus RNA-seq with treatment records. Access requires an application. Response annotation is less uniform, and you'd have to build the ICI subcohort yourself.

## Harmonized collections (a good shortcut)

These package many of the cohorts above with curated clinical data:
- **CRI iAtlas** (cri-iatlas.org)
- **TIDE** (tide.dfci.harvard.edu)
- **TIGER**
- **PredictIO / ORCESTRA** (Bareche et al., Ann Oncol 2022)
- **ICBatlas**

They are useful for finding cohorts and for sanity-checking your own processing. I'd still take the primary data from the source when you can. Curated clinical labels sometimes differ from the papers, and the portals' own access terms vary.

## Pitfalls for cross-cohort validation

- **Timepoint:** Riaz, Hugo and Gide include on-treatment samples. Keep pre-treatment samples only.
- **Prior therapy:** Riaz has ipilimumab-progressed and naive patients. Liu and Van Allen are pretreated to varying degrees.
- **Response definitions:** RECIST CR/PR against SD/PD, versus clinical benefit with a minimum SD duration. Harmonize these explicitly.
- **Patient overlap:** Van Allen and Liu may share patients, and some melanoma sets reuse samples. Check this before treating them as independent.
- **Platform and processing:** FPKM, TPM, raw counts, polyA versus exome-capture RNA-seq. Reprocess from raw reads where you can.
- **Cohort size:** most are under 100 patients. Melanoma dominates, so leave-one-cohort-out across cancer types will be harder than within melanoma.

I can check the current accessions and access terms for any of these with web search, or draft a table of cohort, accession, n and access route. Tell me which you'd like.