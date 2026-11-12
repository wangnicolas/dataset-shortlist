These datasets pair chest X-rays with the radiologist's free-text report. I confirmed each one exists, but the access details come from search snippets and the one page I could fetch. Several pages I didn't open directly, so check the exact terms before you apply.

## English

| Dataset | Size | Access |
|---|---|---|
| **MIMIC-CXR** (v2.1.0) | ~377k radiographs, ~228k reports | Credentialed PhysioNet access |
| **CheXpert Plus** | ~223k image–report pairs, 187,711 studies, 64,725 patients | Stanford AIMI data use agreement |
| **IU X-ray (Open-i)** | ~3,955 reports, ~7,470 images | Open download |

- **MIMIC-CXR:** The DICOM images come with free-text reports from routine care. The reports are also bundled in one archive, `mimic-cxr-reports.tar.gz`. To get access you register on PhysioNet, complete credentialing, and sign the data use agreement. The license is the PhysioNet Credentialed Health Data License 1.5.0. This is the standard main benchmark. Plan for some lead time on credentialing. Don't confuse it with MIMIC-CXR-JPG, which has JPGs and labels derived from the reports.
- **CheXpert Plus:** The reports are split into 11 subsections, and the DICOMs come with metadata and demographics. You download it from the AIMI page after agreeing to the research use agreement. A secondary source says the agreement prohibits commercial use and redistribution. The sources disagree on the exact image count (223,228 vs 223,462), so check the version you download.
- **IU X-ray (Open-i):** Reports have indication, findings and impression sections, and are annotated with MeSH and RadLex codes. The image and report archives (`NLMCXR_png.tgz`, `NLMCXR_reports.tgz`) are listed on the NLM Open-i site. There is also a Kaggle copy, `raddar/chest-xrays-indiana-university`. It is small, so people usually use it as a secondary benchmark next to MIMIC-CXR. Different papers cite slightly different counts.

## Non-English

| Dataset | Language | Size | Access |
|---|---|---|---|
| **PadChest** | Spanish | >160k images, ~109k reports | Request form to BIMCV |
| **PadChest-GR** | English and Spanish | 4,555 studies | Request on BIMCV site |
| **ViX-Ray** | Vietnamese | 5,400 samples | Hugging Face, not gated |
| **CASIA-CXR** | French | 11,111 images | Download from the project site |

- **PadChest:** You request access at the BIMCV project page and agree not to share the data or try to re-identify patients. I couldn't find the form fields or the typical approval time. Many of its labels were extracted automatically from the reports, but the reports themselves are included.
- **PadChest-GR:** It is a curated subset with grounded reports in both languages. That makes it useful if you want English and Spanish together, but it is small.
- **ViX-Ray:** It has 4,320 train, 540 validation and 540 test samples. Each is a PA-view image with Vietnamese findings and impressions. I fetched the page and it shows no gating. The license is inconsistent: the tag says CC BY-NC 4.0 and the description says CC BY-NC-SA 4.0. It is 17.3 GB.
- **CASIA-CXR:** It has frontal radiographs with French reports, but only for five conditions: cardiomegaly, pneumothorax, pleural effusion, pneumonia and mass. The authors say it is freely available at casia-cxr.net, and there is a Hugging Face mirror (`FrancophonIA/CASIA-CXR`). I couldn't open the paper page to confirm the license.

## Not usable
- **Chinese:** CX-CHR and CH-Xray are private. COV-CTR is public but covers CT, not X-ray.
- **German:** The only corpus I found is a private one from University Hospital Bonn, used for report labeling. I found no public German set.
- **Arabic:** I found none.
- **VinDr-CXR:** It has radiologist annotations and labels, not free-text reports.

## Suggested setup
Start the MIMIC-CXR credentialing now, since it is the slowest step. Meanwhile, prototype on IU X-ray, which needs no approval. Add CheXpert Plus as a second large English set. For the secondary experiment, PadChest (Spanish) is the largest non-English option but needs approval. ViX-Ray or CASIA-CXR are the quickest to get, though both are small.

Sources:
- [MIMIC-CXR v2.1.0 (PhysioNet)](https://physionet.org/content/mimic-cxr/2.1.0/)
- [MIMIC-CXR paper (Scientific Data)](https://www.nature.com/articles/s41597-019-0322-0)
- [CheXpert Plus (Stanford AIMI)](https://aimi.stanford.edu/datasets/chexpert-plus)
- [CheXpert Plus paper (arXiv)](https://arxiv.org/abs/2405.19538)
- [IU X-ray overview (Awesome-Medical-Dataset)](https://github.com/openmedlab/Awesome-Medical-Dataset/blob/main/resources/IU-Xray.md)
- [PadChest paper (arXiv)](https://arxiv.org/abs/1901.07441)
- [PadChest-GR](https://www.researchgate.net/publication/392806493_PadChest-GR_A_Bilingual_Chest_X-Ray_Dataset_for_Grounded_Radiology_Report_Generation)
- [ViX-Ray on Hugging Face](https://huggingface.co/datasets/MilitaryHospital175/VNMedical_bv175)
- [CASIA-CXR site](https://www.casia-cxr.net/)
- [CASIA-CXR paper](https://dl.acm.org/doi/10.1016/j.neucom.2024.128478)
- [CASIA-CXR on Hugging Face](https://huggingface.co/datasets/FrancophonIA/CASIA-CXR)