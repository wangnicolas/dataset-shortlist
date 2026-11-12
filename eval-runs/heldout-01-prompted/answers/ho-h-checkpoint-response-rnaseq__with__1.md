I found most of these through secondary sources. NCBI's GEO and dbGaP pages blocked my fetches with a browser check, so I couldn't open the GEO records myself. Accessions marked "from memory" were not confirmed by any search result.

## Download now (open access)

| Cohort | Drug and cancer | Where | Verified? |
|---|---|---|---|
| **Hugo 2016** | anti-PD-1, melanoma, about 28 patients | GEO [GSE78220](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78220) | Accession confirmed by a paper. Page not opened. |
| **Riaz 2017** | nivolumab, melanoma, pre- and on-treatment biopsies | GEO [GSE91061](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061) (also SRP094781, PRJNA356761) | Accession confirmed by a paper. Page not opened. |
| **Gide 2019** | anti-PD-1 with or without anti-CTLA-4, melanoma | Raw reads from ENA PRJEB23709. Clinical data from the paper. | Confirmed by papers. Processed data is also on TIGER. |
| **Kim 2018** | pembrolizumab, gastric cancer, 61 patients | ENA [PRJEB25780](https://www.ncbi.nlm.nih.gov/bioproject/PRJEB25780) | The BioProject exists. I couldn't confirm that it holds the RNA-seq, so check the ENA record. |
| **IMvigor210** (Mariathasan 2018) | atezolizumab, urothelial, 348 patients | Processed counts and clinical data in the [IMvigor210CoreBiologies tarball](http://research-pub.gene.com/IMvigor210CoreBiologies/IMvigor210CoreBiologies.tar.gz) under CC 3.0. Raw data is on EGA. | Confirmed. About 298 patients have response data. |
| **Braun 2020** | nivolumab, ccRCC (CheckMate 009, 010 and 025) | Normalised RNA-seq, clinical and mutation data in the Nature Medicine supplementary file `41591_2020_839_MOESM2_ESM.xlsx` | Confirmed by papers. Raw data is on EGA (see below). |

Notes on these cohorts:
- **IMvigor210 package:** it needs the old DESeq package, which is no longer on Bioconductor. One reanalysis reads the saved data objects from the tarball directly with only Biobase.
- **Riaz and Hugo response labels:** I didn't check how response is coded in these. RECIST categories and the pre-treatment versus on-treatment labels in Riaz need care so that on-treatment samples don't leak into training.

## Apply for access

- **Raw IMvigor210:** EGA [EGAS00001002556](https://ega-archive.org/studies/EGAS00001002556), controlled access. You probably don't need it, because the processed counts are already open.
- **IMvigor210/211/130/010 combined (Cancer Cell 2024):** EGA EGAS50000000497, which I did not open.
- **IMmotion150 and PCD4989g (renal and other):** EGA EGAS00001004343, restricted.
- **Braun raw data:** a Cancer Cell paper cites EGA EGAS00001004290, EGAS00001004291 and EGAS00001004292. Braun's own data statement may differ, so check it.
- **Liu 2019 (melanoma, anti-PD-1):** dbGaP phs000452.v3.p1, according to one paper. The same paper says the data is also on cBioPortal, which may be the quicker route.
- **Miao 2018 (ccRCC, CheckMate 009):** dbGaP phs001493, taken from a Cancer Cell paper that sourced its raw RNA-seq there.
- **MGH melanoma:** dbGaP phs002683.v1.p1, according to one paper. GEO GSE115821 and GSE168204 are also listed as MGH cohorts. I didn't check their access status, so confirm whether they are open.

## Other candidates

- **Amato:** GEO GSE145996, melanoma anti-PD-1, 52 patients with WES and RNA-seq. This was only listed in a search result.
- **Van Allen 2015:** an anti-CTLA-4 melanoma cohort used as validation in several papers. Its dbGaP accession is phs000452 from memory, which matches Liu's accession, so verify it.
- **GSE120575:** this is single-cell data, so it isn't suitable for a bulk classifier.

## Suggestions

1. **Start with the open cohorts.** Hugo, Riaz, Gide, IMvigor210, Kim and Braun cover melanoma, urothelial, gastric and renal cancer, and use anti-PD-1, anti-PD-L1 and anti-CTLA-4.
2. **Check for overlap.** Several melanoma cohorts share patients or pre-treatment samples across papers, which would inflate cross-study validation.
3. **Harmonise the platforms.** The cohorts mix FPKM, TPM and raw counts, so reprocess or rank-normalise them consistently.
4. **Verify GEO details in a browser.** Check the sample counts and the response columns before you commit to a design.

I can run the ENA and GEO checks through their APIs if you'd like. They may be reachable from here even though the NCBI web pages were blocked.

Sources:
- [Melanoma cohort accession search results](https://pmc.ncbi.nlm.nih.gov/articles/PMC12410410/)
- [Nature Communications, molecular patterns of resistance in melanoma](https://www.nature.com/articles/s41467-024-47425-y)
- [Cancer Cell 2024, urothelial carcinoma](https://www.cell.com/cancer-cell/fulltext/S1535-6108(24)00404-5?uuid=uuid%3A3f29ac99-d89a-46ff-ad73-5698e4fb578e)
- [Kim 2018 in Nature Medicine](https://www.nature.com/articles/s41591-018-0101-z)
- [PRJEB25780 on BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJEB25780)
- [PRJEB40416 on BioProject](https://www.ncbi.nlm.nih.gov/bioproject/PRJEB40416)
- [Cancer Cell 2021, tumor and immune reprogramming in renal cell carcinoma](https://www.cell.com/cancer-cell/fulltext/S1535-6108(21)00117-3)
- [Nature Communications, 9p21 loss](https://www.nature.com/articles/s41467-021-25894-9)
- [PMC9382843, IO score in urothelial cancer](https://pmc.ncbi.nlm.nih.gov/articles/PMC9382843/)