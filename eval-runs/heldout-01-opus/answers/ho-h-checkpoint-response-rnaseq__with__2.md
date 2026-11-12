## What I assumed you need
- **R1 (must):** patients actually treated with anti-PD-1/PD-L1 or anti-CTLA-4, with tumour samples taken **before** treatment
- **R2 (must):** bulk tumour **RNA-seq**. I counted NanoString panels, microarrays and blood samples as not meeting this.
- **R3 (must):** a response label for each patient: RECIST, or clinical benefit
- **R4 (nice to have):** downloadable today. Controlled cohorts are included but ranked lower.

I checked everything on 2026-11-12. GEO and ENA block scripts on their web pages, so I confirmed records through their APIs instead (NCBI E-utilities, ENA portal API, EGA metadata API, cBioPortal API).

## Key finding
**cBioPortal hosts iAtlas-harmonised copies of several major ICI cohorts.** Each has a TPM matrix plus `RESPONSE` and `CLINICAL_BENEFIT` columns, and you can download them now without logging in. This includes cohorts whose raw reads are controlled (Liu 2019 is in dbGaP; IMmotion150 is in EGA). For a classifier you mostly don't need the raw reads, so most of what you need is available today.

## Shortlist
| # | Cohort | Cancer / drug | Pre-treatment RNA-seq n | Access | Checked |
|---|---|---|---|---|---|
| 1 | **IMvigor210** (Mariathasan 2018) | Urothelial, atezolizumab | 348 | **Open now:** R package with counts and response; also on cBioPortal. Raw reads: EGA, controlled | today |
| 2 | **Liu 2019** | Melanoma, anti-PD-1 | ~120 | **Open now:** cBioPortal `mel_iatlas_liu_2019`. Raw: dbGaP phs000452 | today |
| 3 | **Gide 2019** | Melanoma, anti-PD-1 ± anti-CTLA-4 | ~70 | **Open now:** raw FASTQ at ENA PRJEB23709; processed copy on cBioPortal | today |
| 4 | **Riaz 2017** GSE91061 | Melanoma, nivolumab | ~51 pre (109 samples) | **Open now:** GEO; labels on cBioPortal | today |
| 5 | **Kim 2018** PRJEB25780 | Gastric, pembrolizumab | ~45 | **Open now:** ENA, raw reads only, so you quantify them yourself | today |
| 6 | **IMmotion150** | Renal cell, atezolizumab ± bevacizumab vs sunitinib | 263 samples | **Open now:** cBioPortal `rcc_iatlas_immotion150_2018`. Raw: EGA | today |
| 7 | **Hugo 2016** GSE78220 | Melanoma, anti-PD-1 | 28 | **Open now:** GEO | today |
| 8 | **Rose 2021** GSE176307 | Urothelial, mixed PD-(L)1 drugs | 89 | **Open now:** GEO | today |
| 9 | **Braun 2020** CheckMate 009/010/025 | Renal cell, nivolumab vs everolimus | ~181 on nivolumab | Paper supplementary tables; raw reads controlled | partly today |
| 10 | **SU2C-MARK** (Ravi 2023) | NSCLC, anti-PD-(L)1 | 152 | Processed data reportedly in the supplement; raw at dbGaP phs002822 | partly today |
| 11 | **POPLAR + OAK** | NSCLC, atezolizumab vs docetaxel | 891 | **Apply:** EGA access committee (Genentech), likely months | today |
| 12 | **Van Allen 2015** | Melanoma, **ipilimumab** (anti-CTLA-4) | 42 | **Apply:** dbGaP phs000452 | from memory |

**Small open GEO/ENA cohorts, useful only for validation:**
- GSE121810 and PRJNA482620: glioblastoma
- GSE135222, GSE136961, GSE126044: NSCLC, n=16–27
- GSE115821: melanoma, mixed timepoints
- GSE181815: thymic carcinoma
- GSE165252: oesophageal, atezolizumab plus chemoradiation, so the treatment is confounded
- GSE168204: mostly on-treatment samples

## Details that matter
- **IMvigor210:** download `IMvigor210CoreBiologies_1.0.1.tar.gz` (74 MB) from research-pub.gene.com/IMvigor210CoreBiologies/packageVersions/. It's the largest open cohort and the usual anchor for training.
  - The RNA was profiled from FFPE tissue with an exome-capture protocol, which differs from the fresh-frozen poly-A RNA-seq in the melanoma cohorts. Expect a platform effect.
  - About a quarter of patients have no evaluable response.
  - I didn't read the package licence.
- **Riaz:** the GEO series doesn't include response labels. Take them from the paper's Table S2 or the cBioPortal copy. Also split ipilimumab-naive from ipilimumab-progressed patients.
- **Gide:** mixes anti-PD-1 alone with the combination. Use treatment as a covariate and drop the on-treatment samples.
- **Liu 2019:** some patients had already received ipilimumab. The cBioPortal `mel_dfci_2019` copy has TPM but no response field, so use the iAtlas copy for labels.
- **Control arms:** Braun (everolimus), IMmotion150 (sunitinib) and POPLAR/OAK (docetaxel) include patients who didn't get a checkpoint inhibitor. They let you show the classifier predicts ICI response specifically, rather than just general prognosis. Reviewers will ask about this.
- **Response definitions differ** between studies: CR/PR versus clinical benefit, which can include stable disease beyond 6 months. Harmonise them before training.
- **Mind the dbGaP/EGA agreements.** If you do get raw controlled data, they generally forbid sending records to third-party online services, which can include hosted AI tools.
- **Usage evidence:** the 2026 Nature Medicine COMPASS paper (doi:10.1038/s41591-026-04502-7) used IMvigor210 from this package and from iAtlas. A 2022 systematic review (PMC9153191) catalogues about 25 ICI transcriptomic cohorts.

## Known, not confirmed
- **TIDE** (tide.dfci.harvard.edu), **TIGER**, **ORCESTRA/PredictIO** and **ICBatlas** are aggregator portals with harmonised ICI cohorts. None of them could be read by script today: they refused automated requests, are JavaScript-only, or returned a 502 error. Open them in a browser.
- The SU2C-MARK and Braun supplementary matrices were reported by papers that reused them; I didn't open the files.
- Van Allen's access details are from memory.

## Not recommended
- GSE100797: adoptive T-cell therapy, not a checkpoint inhibitor
- GSE93157 and GSE165745: NanoString panels
- GSE94873: whole-blood RT-PCR, not tumour
- GSE67501, GSE111636, GSE122220, GSE140901: arrays with n of 24 or fewer
- TCGA: patients weren't treated with checkpoint inhibitors

## Gaps
Apart from Van Allen 2015, I found no sizeable anti-CTLA-4 *monotherapy* RNA-seq cohort. The PD-1 cohorts heavily outweigh CTLA-4 ones.

## Next step
1. **Today:** pull IMvigor210, the cBioPortal iAtlas studies (Liu, Gide, Riaz, IMmotion150), and Hugo and Rose from GEO.
2. Validate with leave-one-cohort-out.
3. Start the POPLAR/OAK EGA application now, since it takes months.

The interactive shortlist (26 entries, filterable, exportable access plan) is at `/private/tmp/e-MGNaSd/home/cwd/dataset-shortlist.html`.

Sources: [Ravi 2023, Nat Genet](https://www.nature.com/articles/s41588-023-01355-5) · [Systematic review of ICI transcriptomic datasets](https://link.springer.com/article/10.1186/s12967-022-03409-4) · [CRI iAtlas help](https://cri-iatlas.org/help/) · [COMPASS, Nat Med 2026](https://www.nature.com/articles/s41591-026-04502-7) · [Braun 2020 (via Bi 2021, Cancer Cell)](https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00117-3) · [IMvigor210CoreBiologies](http://research-pub.gene.com/IMvigor210CoreBiologies/)