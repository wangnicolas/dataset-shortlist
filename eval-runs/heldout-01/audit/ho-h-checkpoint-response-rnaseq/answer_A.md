## What I assumed you need

- **R1 (must):** patients received anti-PD-1, anti-PD-L1 or anti-CTLA-4.
- **R2 (must):** pre-treatment bulk tumour RNA-seq.
- **R3 (must):** recorded RECIST or clinical-benefit response.
- I assumed any cancer type is fine and that you can wait for a controlled-access application.

**How much I checked:** I confirmed very little today. The registry tool covers Zenodo, OpenAIRE and DataCite, not GEO, EGA or dbGaP, and its hits were mostly noise. The GEO, PMC and ENA pages came back as bot challenges or JavaScript shells, and dbGaP redirected one link to its home page. The only access page I actually read was IMvigor210's. Everything else is from memory, so open each link in a browser before you plan around it.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Riaz 2017, melanoma, nivolumab (GSE91061) | Open on GEO | Not stated | ~50 patients | Strong | From memory |
| 2 | Hugo 2016, melanoma, pembrolizumab (GSE78220) | Open on GEO | Not stated | ~28 patients | Strong | From memory |
| 3 | Gide 2019, melanoma, anti-PD-1 ± anti-CTLA-4 (PRJEB23709) | Probably open via ENA, plus paper supplement | Not stated | ~90 patients | Strong | From memory |
| 4 | Mariathasan 2018 (IMvigor210), urothelial, atezolizumab | Processed data: open R package. Raw data: EGA application | Not stated | ~300 patients | Strong | Page read today |
| 5 | Kim 2018, gastric, pembrolizumab (PRJEB25780) | Likely open (ENA) | Not stated | ~45 patients | Partial | From memory |
| 6 | Liu 2019 / Van Allen 2015, melanoma (dbGaP phs000452) | dbGaP application, weeks to months | dbGaP terms | ~120 patients | Partial | From memory |
| 7 | Braun 2020, renal, nivolumab (CheckMate 009/010/025) | dbGaP application (accession unconfirmed) | dbGaP terms | RNA-seq on a subset | Partial | From memory |
| 8 | Cho 2020 / Jung 2019, NSCLC (GSE126044) | Open on GEO | Not stated | Small | Unknown | From memory |

## Details

- **Open now, from memory (rows 1, 2, 8):** these are GEO series. Download the expression tables from GEO, and take the response labels from each paper's supplement. Riaz includes patients who had already progressed on ipilimumab. For Hugo, check which samples are pre-treatment. For row 8, I haven't checked the platform, treatment or response labels.
- **Gide and Kim (rows 3, 5):** the reads are in ENA. Check the data availability statements for what is processed and what is controlled. I could not load the ENA pages.
- **IMvigor210 (row 4):** this is the only one I confirmed. The page at http://research-pub.gene.com/IMvigor210CoreBiologies/ says:
  - Processed data come with the `IMvigor210CoreBiologies` R package.
  - "The human raw gene expression data will be availabe at the European Genome-phenome archive (EGA) under the accession number EGAS00001002556."
  - The EGA data are the controlled-access part. The package licence is not stated on the page.
  - The cohort is anti-PD-L1 only, and my first attempt to fetch the page failed with a connection error before a later read worked.
- **dbGaP cohorts (rows 6, 7):**
  - Access needs a Data Access Request approved by your institution's signing official, which usually takes weeks to months.
  - The Liu and Van Allen data are mostly exome, so confirm RNA-seq coverage.
  - The Braun accession (phs002277) is my recollection. Its link redirected to the dbGaP home page, so don't trust it yet.
  - Row 6 merges two studies under one accession, and I am not certain both are there.

## Known, not confirmed

- **Larger cohorts from memory:** I recall a Lee et al. cohort at EGA (EGAD00001005738, from a web search result) and a Miao 2018 renal dataset at dbGaP phs001519. I have not confirmed either one's contents.
- **More cohorts via curated resources:** ICBatlas (25 studies, 1,515 samples), the 2023 ICB benchmark (PMC10452274, 29 datasets) and IOhub (36 bulk datasets) list the accessions. None of them is verified, and I could not open any of the tables. Start there for more cohorts, and use ICBatlas Table S1 for accessions.
- **Cross-cohort caution:** an arXiv preprint (2604.05478) is titled "Transcriptomic Models for Immunotherapy Response Prediction Show Limited Cross-cohort Generalisability". I only saw the title and have not read it.

## Not recommended

- **TCGA:** the patients were mostly not treated with checkpoint inhibitors, so there are no response labels.

## What I could not find

- No GEO, EGA or dbGaP accession was confirmed through its own registry page.
- Licences are mostly unstated. GEO data are public, but reuse terms depend on the submitters.
- The tool found no papers using these cohorts for response prediction beyond the IMvigor210 paper.

## Next step

1. Pull the accession tables from ICBatlas and the 2023 benchmark. Together they should give you the 5–10 independent cohorts you want.
2. Start the dbGaP and EGA applications now, since they take the longest, and build on the open GEO cohorts in the meantime.

