Four datasets pair chest X-rays with the radiologist's free-text report, and each one exists and has a documented route to the data. I opened the PhysioNet, BIMCV, Stanford AIMI and BRAX pages. I couldn't open the Open-i page, so its download links come from papers and repositories that cite them.

## English

| Dataset | Size | Report content | Access |
|---|---|---|---|
| **MIMIC-CXR v2.0.0** | About 377k images and 228k reports from 65k patients (Beth Israel Deaconess ED, 2011–2016) | One de-identified free-text report per study, as `sXXXXXXXX.txt` files and as a single `mimic-cxr-reports` archive | Credentialed PhysioNet access. You register, complete CITI "Data or Specimens Only Research" training, and sign the DUA. You can't share the data and you must release code for any publication that uses it. |
| **CheXpert Plus** | 223,462 image–report pairs, 187,711 studies, 64,725 patients (Stanford, 2002–2017) | Full reports split into up to 11 subsections, plus RadGraph annotations and DICOM and PNG images | Hosted on Redivis through the Stanford AIMI page. The sources say a Research Use Agreement bars commercial use, but I couldn't see the terms text, size or login requirements. Check the Redivis page before planning around it. |
| **IU X-ray (Open-i)** | 3,955 reports and 7,470 images | XML reports with indication, comparison, findings and impression sections | Open download, no credentialing. Reports are at `openi.nlm.nih.gov/imgs/collections/NLMCXR_reports.tgz` and images at `NLMCXR_png.tgz`. Academic Torrents mirrors the reports and a Kaggle mirror has CSVs. The license is reported as CC BY-NC-ND 4.0, which is a secondhand claim. |

- **MIMIC-CXR:** This is the standard benchmark. Its derived versions (MIMIC-CXR-JPG, CXR-PRO and others) also need credentialed access. CXR-PRO removes references to prior studies from the reports, which matters for report generation.
- **CheXpert Plus:** It is the largest set of reports from a single institution outside MIMIC.
- **IU X-ray:** It is small, so it works for quick experiments and as a second test set. Some papers report slightly different counts, for example after dropping reports with no findings section. Check the license text yourself, since I only have it from papers.

## Non-English

- **PadChest (Spanish):** It has more than 160k images from 67k patients at Hospital San Juan in Spain, from 2009 to 2017. The reports are in Spanish. The full dataset is about 1 TB and is free for researchers. You request it through a form on the BIMCV page and agree to its Research Use Agreement, which bars sharing and re-identification. A 167 MB sample is on Kaggle, but I couldn't confirm whether it includes report text.
- **PadChest-GR:** It has 4,555 studies with bilingual Spanish and English reports and grounding annotations. It is available on request from BIMCV. That makes it the only bilingual option I found.
- **BIMCV COVID-19+:** It has Spanish reports, but it is small and limited to COVID-19 patients. I didn't check its access terms.

## Datasets to avoid

- **BRAX (Brazilian Portuguese):** It releases only the 14 labels derived from the reports. The paper says free-text reports are not provided in the current version.
- **German:** I found no public German set with reports. The only one that came up (Hannover COVID-19) is 240 images, with no reports mentioned.
- **CX-CHR (Chinese reports):** It is private.

## Suggested plan

Start with IU X-ray because it needs no approval. Apply for MIMIC-CXR credentialing at the same time, since it takes the longest. Request PadChest for the non-English experiment.

Sources:
- [MIMIC-CXR v2.0.0 (PhysioNet)](https://physionet.org/content/mimic-cxr/2.0.0/)
- [MIMIC-CXR paper (Scientific Data)](https://www.nature.com/articles/s41597-019-0322-0)
- [CheXpert Plus (Stanford AIMI)](https://aimi.stanford.edu/datasets/chexpert-plus)
- [CheXpert Plus paper](https://arxiv.org/abs/2405.19538)
- [PadChest (BIMCV)](https://bimcv.cipf.es/bimcv-projects/padchest/)
- [PadChest paper](https://arxiv.org/abs/1901.07441)
- [PadChest-GR](https://ai.nejm.org/doi/full/10.1056/AIdbp2401120)
- [BIMCV COVID-19+](https://arxiv.org/abs/2006.01174)
- [BRAX paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9364309/)
- [IU X-ray on Academic Torrents](https://academictorrents.com/details/66450ba52ba3f83fbf82ef9c91f2bde0e845aba9)
- [IU X-ray usage in PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0259639)