You can assemble roughly ten independent cohorts with open processed expression and response labels today, and the biggest trial cohorts (lung, kidney, liver) need an application. I checked the accessions and counts below against GEO, ENA, EGA and the cBioPortal API; items I could not check are marked "from memory".

## Download right away

**Start with the CRI iAtlas harmonised studies on cBioPortal** (no login, via the web, API or datahub). Each has gene-level expression plus `RESPONSE` (RECIST category), `RESPONDER`, `CLINICAL_BENEFIT` and `SAMPLE_TREATMENT` (pre/on) fields.

| Cohort (cBioPortal study ID) | Cancer | Drug | RNA samples | Notes |
|---|---|---|---|---|
| IMvigor210 (`blca_iatlas_imvigor210_2017`) | Urothelial | Atezolizumab | 347, all pre | 298 with response; also in the Genentech `IMvigor210CoreBiologies` R package |
| IMmotion150 (`rcc_iatlas_immotion150_2018`) | Renal | Atezolizumab ± bevacizumab | 263, all pre | 89 are sunitinib-only; drop them |
| Liu 2019 (`mel_iatlas_liu_2019`) | Melanoma | Pembrolizumab or nivolumab | 122, all pre | Also as `mel_dfci_2019` (same patients) |
| Gide 2019 (`mel_iatlas_gide_2019`) | Melanoma | Anti-PD-1 ± ipilimumab | 91 (73 pre) | FASTQ open at ENA PRJEB23709 |
| Riaz 2017 (`mel_iatlas_riaz_nivolumab_2017`) | Melanoma | Nivolumab | 107 (51 pre) | GEO GSE91061 |
| Hugo 2016 (`mel_iatlas_hugo_ucla_2016`) | Melanoma | Pembrolizumab | 27 (26 pre) | GEO GSE78220; also as `mel_ucla_2016` |
| Van Allen 2015 (`skcm_dfci_2015`) | Melanoma | Ipilimumab | about 40 with RNA (from memory) | Your main anti-CTLA-4 cohort; not iAtlas-harmonised |
| PRINCE (`paad_iatlas_prince_2022`) | Pancreatic | Chemo ± nivolumab ± sotigalimab | 93 (64 pre) | 24 samples had no ICI |
| Anders 2022 (`brca_iatlas_anders_2022`) | Triple-negative breast | Pembrolizumab + cyclophosphamide | 31, all pre | |
| Choueiri 2016 (`ccrcc_iatlas_choueiri_2016`) | Renal | Nivolumab | 16, all pre | |
| Prins 2019 (`gbm_iatlas_prins_2019`) | Glioblastoma | Neoadjuvant pembrolizumab | 30 (15 pre) | No responders recorded |

**Open cohorts in GEO, ENA or SRA.** I confirmed these records and sample counts, but not where the response labels sit; they may be in the paper supplement instead of the series metadata.

- **Urothelial:** GSE176307, 90 samples, mixed ICI.
- **Gastric:** ENA PRJEB25780 (Kim 2018, pembrolizumab), 78 RNA-seq runs.
- **Lung (NSCLC):** GSE135222 (27), GSE136961 (21) and GSE126044 (16), all anti-PD-1.
- **Melanoma:** GSE115821 (37) and GSE168204 (27); both mix pre- and on-treatment samples.
- **Glioblastoma:** SRA PRJNA482620 (Zhao 2019), 34 RNA-seq runs.
- **Thymic carcinoma:** GSE181815 (30, pembrolizumab).
- **Head and neck / lung:** GSE159067 (102) and GSE161537 (82). I believe these are targeted panels, not whole transcriptome; check before using.

**Open in paper supplements (from memory, not checked):**
- Braun 2020 (*Nat Med*), renal CheckMate 009/010/025: normalised expression for about 311 patients, of whom about 181 received nivolumab.
- JAVELIN Renal 101 (Motzer 2020, *Nat Med*): avelumab + axitinib, about 700 patients.

**Curated bundles:** ORCESTRA (orcestra.ca/clinical_icb, from the PredictIO project) and TIGER (tiger.canceromics.org) repackage many of the above. I confirmed the sites are live but not their contents.

## Need an application

| Cohort | Cancer / drug | Accession | Route |
|---|---|---|---|
| OAK + POPLAR (Patil 2022) | Lung, atezolizumab vs docetaxel; about 890 RNA-seq (from memory) | EGAS00001005013 | Genentech committee via EGA |
| IMmotion151 | Renal, atezolizumab + bevacizumab; about 820 (from memory) | EGAS00001004353 | Same |
| IMbrave150 / GO30140 | Liver, atezolizumab + bevacizumab | EGAS00001005503 | Same |
| IMvigor210 and IMmotion150 raw data | Urothelial, renal | EGAS00001002556, EGAS00001002928 | Same; only needed for raw reads |
| Braun renal raw data | Renal | EGAS00001004290–92 | EGA |
| Van Allen / Liu melanoma raw data | Melanoma | dbGaP phs000452 (from memory) | dbGaP, institutional sign-off |
| SU2C-MARK lung (Ravi 2023) | Lung, about 150 RNA-seq | dbGaP (accession not confirmed) | dbGaP |
| Hartwig Medical Foundation | Pan-cancer metastatic, with treatment and response | — | Data access request |

Expect weeks to months for EGA and dbGaP. OAK/POPLAR is the one worth applying for now, because open lung data is otherwise small.

## Before you train

- **Filter to pre-treatment samples and ICI arms.** Riaz, Gide, PRINCE and Prins include on-treatment biopsies; IMmotion150 and PRINCE include non-ICI patients.
- **Don't double-count.** Hugo and Liu each appear twice in cBioPortal, and the bundles repackage the same cohorts.
- **Expression units differ** (TPM, log TPM, upper-quartile counts). For a uniform pipeline, reprocess from the open FASTQs (Gide, Kim, Riaz, Hugo, Zhao).
- **Decide how to treat stable disease.** `RESPONDER` is CR/PR only; `CLINICAL_BENEFIT` also counts stable disease.
- **Melanoma dominates the open data**, so hold out whole cohorts in other cancer types (IMvigor210, IMmotion150, Kim) for validation.