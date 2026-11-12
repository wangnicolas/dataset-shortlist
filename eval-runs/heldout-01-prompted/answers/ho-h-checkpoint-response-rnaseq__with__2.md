Several accessions are verified against the registry records and some rest on secondary sources. I've marked which is which. NCBI's GEO web pages blocked my fetches with a CAPTCHA, so I confirmed the GEO records through NCBI's E-utilities API instead.

## Download now (open access)

| Cohort | Cancer / treatment | n (RNA-seq) | Where | Checked |
|---|---|---|---|---|
| **Hugo 2016** | Melanoma, anti-PD-1 | 28 | [GSE78220](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78220) | Record confirmed via E-utilities (pre-treatment biopsies, RNA-seq) |
| **Riaz 2017** | Melanoma, nivolumab, with pre- and on-treatment samples | 109 samples | [GSE91061](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061) | Record confirmed via E-utilities |
| **Gide 2019** | Melanoma, anti-PD-1 or anti-PD-1 + anti-CTLA-4 | not checked | ENA [PRJEB23709](https://www.ebi.ac.uk/ena/browser/api/xml/PRJEB23709) | Status PUBLIC, RNA-seq. Fetched directly. |
| **Amato 2020** | Melanoma, anti-PD-1, RECIST 1.1 | see caveat | [GSE145996](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145996) | Record exists. The summary says 52 patients, but the record lists only 14 samples. Check the files before relying on it. |
| **Mariathasan 2018 (IMvigor210)** | Urothelial, atezolizumab | 348 | [IMvigor210CoreBiologies R package](http://research-pub.gene.com/IMvigor210CoreBiologies/) (CC 3.0 licence) | Found via search, not downloaded. It contains processed counts and clinical data, and it's the easiest large cohort to get. |
| **Braun 2020** | Clear-cell RCC, nivolumab (CheckMate 009/010/025) | about 311 combined | Supplementary tables of [the Nature Medicine paper](https://www.nature.com/articles/s41591-020-0839-y) | A reuse paper reports normalized expression and clinical data in the supplement. I didn't open the paper myself. |
| **Kim 2018** | Gastric, pembrolizumab | about 45–61 | ENA [PRJEB25780](https://www.omicsdi.org/dataset/project/PRJEB25780). Processed versions are on [CRI iAtlas](https://cri-iatlas.org/resources/) and TIDE. | Project listing confirmed. Reports of the usable n differ between papers. |

[CRI iAtlas](https://cri-iatlas.org/about/) harmonizes about 23 immuno-oncology datasets, including Riaz, Miao, Kim, Anders (TNBC, pembrolizumab), Padrón (pancreatic) and Rose (urothelial). It's worth checking for ready-made matrices, but verify each study's access terms there.

GSE168204 (27 samples) is not a new cohort. It's a pathway-signature paper that reuses the Riaz, Hugo and other data, so don't count it as an independent validation set.

## Apply for access (controlled)

- **Mariathasan raw data:** EGA [EGAS00001002556](https://ega-archive.org/studies/EGAS00001002556), with RNA-seq dataset EGAD00001003977 (348 samples). You'd only need this if you want to re-process from raw reads. The EGA page didn't state the DAC, so check the dataset page.
- **Liu 2019 and Van Allen 2015 (melanoma):** dbGaP [phs000452](https://pmc.ncbi.nlm.nih.gov/articles/PMC12410410/). Sources disagree on whether v2 or v3 maps to which study, so check the version when you apply.
- **Miao 2018 (RCC):** dbGaP phs001493.
- **Ravi 2023 (NSCLC, SU2C-MARK):** dbGaP [phs002822.v1.p1](https://www.nature.com/articles/s41588-023-01355-5), which has about 393 patients with WES and/or RNA-seq. It has site-specific use restrictions, including disease-specific use. It is the largest lung cohort I found.
- **Newer MGH melanoma cohort:** dbGaP phs002683.v1.p1.
- **Braun 2020 raw data:** EGA EGAS00001004290, EGAS00001004291 and EGAS00001004292. These came from a secondary citation, so confirm them.
- **McDermott 2018 (RCC, atezolizumab):** EGA EGAS00001002928.

## Not verified
- I found no data-access information for Cho (NSCLC).
- I didn't find or check the full Ravi accession list beyond the two above.
- I didn't verify the n for Gide or any response-label coding, so you'll need to check each cohort's clinical table.

## Practical advice
- **Starting set:** Hugo, Riaz, Gide and Amato (melanoma), plus IMvigor210 (bladder), Braun (RCC) and Kim (gastric). That gives you about seven cohorts across four cancer types with no applications.
- **Batch effects:** Cohorts differ in platform, tissue handling and treatment line. Plan for cross-study normalization.
- **Response labels:** Riaz includes on-treatment samples, so filter to pre-treatment. Labels are mixed between RECIST and clinical benefit, so harmonize them.
- **Overlap:** The Gide and Riaz cohorts might include some of the same patients as other cohorts, so check for duplicates.

Sources:
- [GSE78220](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78220)
- [GSE91061](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE91061)
- [PRJEB23709 (ENA)](https://www.ebi.ac.uk/ena/browser/api/xml/PRJEB23709)
- [GSE145996](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE145996)
- [EGAS00001002556](https://ega-archive.org/studies/EGAS00001002556)
- [IMvigor210CoreBiologies](http://research-pub.gene.com/IMvigor210CoreBiologies/)
- [PRJEB25780 on OmicsDI](https://www.omicsdi.org/dataset/project/PRJEB25780)
- [CRI iAtlas resources](https://cri-iatlas.org/resources/)
- [Ravi et al. 2023](https://www.nature.com/articles/s41588-023-01355-5)
- [Braun et al. 2020](https://www.nature.com/articles/s41591-020-0839-y)
- [Gene-pair signatures paper listing the melanoma accessions](https://pmc.ncbi.nlm.nih.gov/articles/PMC12410410/)