These are the datasets that pair chest X-rays with the radiologist's actual report text. I checked each one against search results. I didn't open every access form, so the gaps are noted below.

## English

| Dataset | Size | Access |
|---|---|---|
| **[MIMIC-CXR v2.1.0](https://physionet.org/content/mimic-cxr/2.1.0/)** | About 377k images and 227k studies. Reports are one text file per study, plus a single `mimic-cxr-reports.tar.gz`. | PhysioNet credentialed access. You register, complete credentialing, and sign the data use agreement. |
| **[CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus)** | About 223k image-report pairs across 187,711 studies. Reports are split into 11 subsections, including history, findings and impression. | Stanford AIMI Research Use Agreement. Code and models are in [Stanford-AIMI/chexpert-plus](https://github.com/Stanford-AIMI/chexpert-plus). |
| **[ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)** | 160k studies and 273k images from 3 US institutions. The paper is [arXiv 2505.00228](https://arxiv.org/abs/2505.00228). | You sign a license on Hugging Face. |
| **IU X-Ray (Open-i)** | 7,470 images and 3,955 reports. | Public download of PNG or DICOM images and XML reports from [NLM Open-i](https://openi.nlm.nih.gov/faq). A [Kaggle mirror](https://www.kaggle.com/datasets/raddar/chest-xrays-indiana-university) also exists. |

- **MIMIC-CXR:** This is the standard benchmark, so use it if you need results comparable to published work. The PhysioNet data use agreement appears to restrict sending the data to external LLM services. One derived dataset said it used an agreement-compliant setup for LLM processing. Read the terms before you use API-based models.
- **CheXpert Plus:** One study notes that the official test split is only 200 studies, so you may need your own splits.
- **ReXGradient-160K:** I only saw the Hugging Face license-gating step. I didn't see the license terms.
- **IU X-Ray:** It's small but easy to get, which makes it good for quick prototyping. The common split is 2,770 / 395 / 790 reports for train / val / test. A third-party catalog lists its license as "none provided", so check NLM's terms before redistributing.

## Non-English (secondary experiment)

- **[PadChest](https://arxiv.org/abs/1901.07441)** has Spanish reports, with more than 160k images from 67k patients at San Juan Hospital. It is hosted by BIMCV at `bimcv.cipf.es/bimcv-projects/padchest/`.
  - You request access through a form on that page and agree not to share the data or re-identify patients.
  - About 27% of the labels were manually annotated and the rest came from a model. That doesn't affect the report text itself.
  - I didn't find approval times or eligibility rules.
- **PadChest-GR** has 4,555 studies with grounded reports in both English and Spanish. It is available on request at `bimcv.cipf.es/bimcv-projects/padchest-gr/`. It is small, but the bilingual reports are useful.
- **[BIMCV COVID-19+](https://arxiv.org/abs/2006.01174)** has Spanish reports, but it is small (about 2,400 radiographs) and COVID-focused. It is also available on request from BIMCV.

## What I couldn't confirm

- I didn't open the BIMCV pages, so confirm their current status and forms yourself.
- My searches for Rad-ReStruct and CTRG returned nothing, so I'm not recommending them. CTRG may be a Chinese-language report set, but I couldn't verify that.
- Chinese, German and other non-English chest X-ray report sets may exist, but I didn't search for them. I can look if you want a language other than Spanish.

I'd start with IU X-Ray while you wait for MIMIC-CXR credentialing, which is usually the slowest step. CheXpert Plus and ReXGradient add scale.

Sources:
- [MIMIC-CXR v2.1.0](https://physionet.org/content/mimic-cxr/2.1.0/)
- [MIMIC-CXR paper](https://www.nature.com/articles/s41597-019-0322-0)
- [MIMIC-CXR-JPG](https://physionet.org/content/mimic-cxr-jpg/2.1.0/)
- [NLM Open-i FAQ](https://openi.nlm.nih.gov/faq)
- [IU X-Ray on Kaggle](https://www.kaggle.com/datasets/raddar/chest-xrays-indiana-university)
- [PadChest paper](https://arxiv.org/abs/1901.07441)
- [PadChest-GR](https://www.researchgate.net/publication/392806493_PadChest-GR_A_Bilingual_Chest_X-Ray_Dataset_for_Grounded_Radiology_Report_Generation)
- [BIMCV COVID-19+](https://arxiv.org/abs/2006.01174)
- [CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus)
- [CheXpert Plus paper](https://arxiv.org/pdf/2405.19538)
- [ReXGradient-160K](https://arxiv.org/abs/2505.00228)