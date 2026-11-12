You can start today: twelve of the fifteen sources I shortlisted are open downloads with no application, covering melanoma, urothelial, renal, gastric and small lung cohorts. The large lung cohorts and the biggest renal cohort need a data access application that takes weeks.

Everything was checked on 11 November 2026 (UTC). "Today" in the tables means I confirmed it against the hosting archive; "memory" means I recall it and did not confirm it.

## What I assumed you need
- **R1 (must):** patients actually treated with anti-PD-1/PD-L1 or anti-CTLA-4.
- **R2 (must):** bulk tumour RNA-seq, not arrays or gene panels.
- **R3 (must):** recorded response (RECIST or clinical benefit).
- **R4 (must):** pre-treatment samples.
- **R5 (nice to have):** downloadable now.
- I assumed academic, non-commercial use and that processed expression matrices are acceptable, with raw reads a bonus.

## Shortlist

**Download today**

| # | Cohort | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | IMvigor210: urothelial, atezolizumab | Direct download | ODbL (cBioPortal); CC0 (Zenodo copy) | 347 pre-treatment; 298 with RECIST | Strong | Today |
| 2 | IMmotion150: renal, atezolizumab ± bevacizumab vs sunitinib | Direct download | ODbL | 263 pre-treatment; 174 on atezolizumab | Strong | Today |
| 3 | Liu 2019: melanoma, anti-PD-1 | Direct download | CC0 | 122 pre-treatment, all with RECIST | Strong | Today |
| 4 | Gide 2019: melanoma, anti-PD-1 ± ipilimumab | Direct download, raw reads also open | CC0 | 73 pre-treatment, 18 on-treatment | Strong | Today |
| 5 | Riaz 2017: melanoma, nivolumab | Direct download | GEO open; CC0 | 51 pre-treatment, 56 on-treatment | Strong | Today |
| 6 | Braun 2020: clear cell renal, nivolumab | Direct download | CC0 | About 311 RNA-seq, about 181 on nivolumab (memory) | Strong | Access today; size and labels from memory |
| 7 | Kim 2018: gastric, pembrolizumab | Direct download, raw reads also open | CC BY 4.0 | 78 RNA-seq runs; about 45 patients (memory) | Strong | Access today; labels from memory |
| 8 | Rose 2021: urothelial, mixed checkpoint inhibitors | Direct download | GEO open | 90 samples | Strong | Existence and size today; labels from memory |
| 9 | Hugo 2016: melanoma, anti-PD-1 | Direct download | GEO open; CC BY 4.0 | 28 samples | Partial (small) | Today |
| 10 | Van Allen 2015: melanoma, ipilimumab | Direct download | CC0 | About 40 RNA-seq (memory) | Partial (small) | Access today; labels from memory |
| 11 | Small lung cohorts: Jung, Hwang, Cho | Direct download | GEO open | 27, 21 and 16 samples | Partial (tiny) | Sizes today; labels from memory |
| 12 | PredictIO data archive | Direct download | CC BY 4.0 | One 52 MB archive | Partial (copies of the above) | Today |

**Application required**

| # | Cohort | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 13 | IMmotion151: renal, atezolizumab + bevacizumab vs sunitinib | Institutional agreement with the Genentech access committee, weeks | Non-commercial, project-specific | 823 tumours | Strong | Today |
| 14 | OAK and POPLAR: lung, atezolizumab vs docetaxel | Access committee application, weeks | Agreement text not read | Several hundred (memory) | Strong | Study today; details from memory |
| 15 | SU2C-MARK: lung, anti-PD-(L)1 | dbGaP Authorized Access, weeks | Lung and thoracic cancer research only | 393 patients, about 152 with RNA-seq | Strong | Today |

## Details

**Three open collections hold most of the cohorts above**
- **[ORCESTRA](https://www.orcestra.ca/clinical_icb)** lists 21 checkpoint cohorts, each as an R `MultiAssayExperiment` file on Zenodo with expression and clinical data.
- **cBioPortal** hosts nine cohorts reprocessed by CRI iAtlas with uniform clinical columns (`RESPONSE`, `CLINICAL_BENEFIT`, `ICI_RX`, `SAMPLE_TREATMENT`). Its FAQ says data are under the ODC Open Database License unless a study notes otherwise, and that you should cite the original study.
- **[PredictIO](https://zenodo.org/records/6142546)** is a single archive of the tables behind the PredictIO meta-analysis ([Bareche 2022](https://doi.org/10.1016/j.annonc.2022.08.084)).

These three overlap heavily, so count each cohort once when you set up cross-study validation.

**Open cohorts**
1. **IMvigor210** is at [cBioPortal](https://www.cbioportal.org/study/summary?id=blca_iatlas_imvigor210_2017) and as [ICB_Mariathasan](https://doi.org/10.5281/zenodo.7332183).
   - Response is 25 CR, 43 PR, 63 SD and 167 PD.
   - The original [Genentech R package](http://research-pub.gene.com/IMvigor210CoreBiologies/) is still up, but the download link in its vignette returned 404 today; the file answered under `packageVersions/IMvigor210CoreBiologies_1.0.0.tar.gz`.
   - Original paper: [Mariathasan 2018](https://doi.org/10.1038/nature25501).
2. **IMmotion150** is at [cBioPortal](https://www.cbioportal.org/study/summary?id=rcc_iatlas_immotion150_2018).
   - Response is 19 CR, 53 PR, 96 SD and 79 PD across all arms.
   - Drop or separate the 89 sunitinib-only patients; about half the atezolizumab patients also had bevacizumab.
3. **Liu 2019** is at [ICB_Liu](https://doi.org/10.5281/zenodo.7332172) and [cBioPortal](https://www.cbioportal.org/study/summary?id=mel_iatlas_liu_2019).
   - 71 patients had pembrolizumab and 51 nivolumab; response is 16 CR, 32 PR, 18 SD and 56 PD.
   - Some patients had prior ipilimumab (`PRIOR_ICI_RX`).
4. **Gide 2019** is at [ICB_Gide](https://doi.org/10.5281/zenodo.7332096) and [cBioPortal](https://www.cbioportal.org/study/summary?id=mel_iatlas_gide_2019).
   - Raw FASTQ is open at [ENA PRJEB23709](https://www.ebi.ac.uk/ena/browser/view/PRJEB23709) (91 runs), so you can reprocess it yourself.
5. **Riaz 2017** is at [GEO GSE91061](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061), [ICB_Riaz](https://doi.org/10.5281/zenodo.7332230) and cBioPortal.
   - More than half the samples are on-treatment, so filter on `SAMPLE_TREATMENT`.
6. **Braun 2020** is at [ICB_Braun](https://doi.org/10.5281/zenodo.7332074).
   - It pools CheckMate 009, 010 and 025; from memory, 025 includes an everolimus arm to exclude, and the tissue is archival.
7. **Kim 2018** is at [ICB_Kim](https://doi.org/10.5281/zenodo.7332153), with raw reads at [ENA PRJEB25780](https://www.ebi.ac.uk/ena/browser/view/PRJEB25780).
8. **Rose 2021** is at [GEO GSE176307](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE176307).
   - It is in neither collection, which makes it a clean external test for a model trained on IMvigor210.
9. **Hugo 2016** is at [GEO GSE78220](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78220) and [ICB_Hugo](https://doi.org/10.5281/zenodo.7332108).
10. **Van Allen 2015** is at [ICB_Van_Allen](https://doi.org/10.5281/zenodo.7332289) and is the main open anti-CTLA-4 cohort.
11. **Small lung cohorts** are at GEO [GSE135222](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE135222), [GSE136961](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE136961) and [GSE126044](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE126044).

Smaller cohorts on cBioPortal that I did not give rows: PRINCE pancreatic (64 pre-treatment, nivolumab plus chemotherapy), Anders triple-negative breast (31), Prins glioblastoma (15 pre-treatment) and Choueiri renal (16).

**Application-only cohorts**

13. **[IMmotion151](https://ega-archive.org/studies/EGAS00001004353)** includes processed log2(TPM+1) for 823 tumours plus outcome data (PFS, ORR).
    - Steps: create an EGA account, request the datasets, e-mail the access committee, and have your institution sign Genentech's agreement.
    - Terms quoted from the agreement: "You agree not to use the data for the creation of products for sale or for any commercial purpose"; "use of the Data for a new purpose or project will require a new application".
    - Collaborators at other institutions apply separately, and the agreement ends after three years.
14. **[OAK and POPLAR](https://ega-archive.org/studies/EGAS00001005013)** is also a Genentech study on EGA, so expect the same route; I did not read this study's agreement.
15. **[SU2C-MARK](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs002822)** needs an eRA Commons account and a Data Access Request co-signed by your institution's signing official.
    - Its single consent group restricts use to lung and thoracic cancer research.
    - Two sites' samples are not deposited ([Ravi 2023](https://www.nature.com/articles/s41588-023-01355-5)).

Raw reads for several open cohorts are also controlled: IMvigor210 and IMmotion150 on EGA, and Van Allen and Liu on [dbGaP phs000452](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000452).

## Known, not confirmed
- **Response labels in some open files:** I did not open the files for Braun, Kim, Van Allen, Rose or the small lung cohorts. I recall response being present; check before relying on them.
- **SU2C-MARK processed matrix:** the paper may post expression in its supplementary tables, which would avoid the dbGaP wait. I could not confirm this.
- **TIGER portal** (tiger.canceromics.org): I recall it offering curated immunotherapy expression downloads; the site answered but I could not read its contents.
- **Hartwig Medical Foundation:** from memory, a large pan-cancer metastatic cohort with RNA-seq and treatment response, available by application. Not checked today.
- **JAVELIN Renal 101** (avelumab plus axitinib): from memory, expression and outcome are in the Nature Medicine paper's supplement. Not checked today.
- **IMvigor210 R package licence:** recalled as CC BY 3.0.

## Not recommended, and why
- **TCGA:** no checkpoint-inhibitor treatment or response recorded.
- **MSK-IMPACT immunotherapy cohorts** (for example the 1,661-patient TMB study): panel DNA only, no RNA-seq.
- **GSE93157 (Prat):** NanoString array, not RNA-seq.
- **GSE100797 (Lauss):** adoptive T-cell therapy, not checkpoint inhibitors.
- **GSE67501 and GSE173839:** microarrays.
- **`TIDE_RESPONDER` and `TIDE_NO_BENEFITS` columns** in the cBioPortal studies: these are model predictions, not outcomes, so do not use them as labels or features.

## What I could not find
- No open lung cohort above about 30 patients.
- Open anti-CTLA-4-only RNA-seq is limited to small melanoma cohorts.
- The general dataset registries were nearly useless here. The cohorts came from GEO, ENA, cBioPortal, ORCESTRA, EGA and dbGaP directly, so cohorts published only on project sites may be missing.

## Next step
Start with rows 1–8, which give roughly 1,200 pre-treatment tumours across four cancer types. If lung matters, submit the SU2C-MARK and OAK/POPLAR applications now, since they take weeks. Response definitions differ between cohorts (RECIST categories versus clinical benefit), so fix one binarisation before pooling.

The interactive shortlist, with filtering and an exportable access plan, is at `/private/tmp/e-lfJeLe/home/cwd/dataset-shortlist.html`. GEO, cBioPortal and ENA entries show as "not verified" there because the page verifier cannot read those sites; I confirmed them through each site's API instead.