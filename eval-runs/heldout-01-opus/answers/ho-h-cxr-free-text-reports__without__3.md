Five main public datasets pair chest X-rays with the radiologist's actual report text. Four are in English, and PadChest is the main non-English (Spanish) option. Most CXR datasets only release labels extracted from the reports, so the list is short.

## English free-text reports

**1. MIMIC-CXR (Beth Israel Deaconess, Boston)**
- **Size:** about 377K images, 227K studies and 65K patients, with full reports (findings, impression, indication, comparison).
- **Access:** through PhysioNet. You need a credentialed account (ID check plus a reference), the CITI "Data or Specimens Only Research" human-subjects course, and a signed data use agreement. Expect this to take a few days to a couple of weeks.
- **Files:** the reports are in the MIMIC-CXR DICOM release (`mimic-cxr-reports.zip`). Most people use MIMIC-CXR-JPG for images (about 570 GB) and take the reports from the main release. The full DICOM set is several TB.
- **Watch out:** the PhysioNet agreement forbids sending the data to third-party services. That includes consumer LLM APIs, which matters if you plan to use LLMs for evaluation or report cleanup. PhysioNet has published guidance on which hosted setups are acceptable.
- **Role:** the de facto standard benchmark for report generation, so you'll almost certainly need it for comparisons.

**2. CheXpert Plus (Stanford)**
- **Size:** 223K report–image pairs, 188K studies and 65K patients. Reports are split into sections, and the release includes DICOM and PNG images, demographics, CheXpert/CheXbert labels and RadGraph annotations.
- **Access:** register on the Stanford AIMI Shared Datasets site and accept a research-use agreement (non-commercial, no redistribution). It's quicker than PhysioNet because no training course is required.
- **Watch out:** the official test set is tiny (about 200 studies, and only about 61 have a Findings section), so plan your own splits.

**3. ReXGradient-160K (Gradient Health / Rajpurkar lab, 2025)**
- **Size:** 160K studies, about 273K images and about 109K patients from 79 US sites across several health systems. That makes it more diverse than single-hospital sets.
- **Format:** images are PNGs converted from DICOM. GPT-4o was used to split the reports into sections, so the text is sectioned but not raw.
- **Access:** a gated Hugging Face dataset (`rajpurkarlab/ReXGradient-160K`). You accept the license on the dataset page, which is the fastest route here.
- **Splits:** train/validation/public test of 140K/10K/10K, plus a private 10K test set behind the ReXrank leaderboard. A later paper gives slightly larger counts, probably because it includes the private split.

**4. IU X-ray / Open-i (Indiana University, via NLM)**
- **Size:** about 7.5K images and about 3.9K reports with findings and impression.
- **Access:** free download from Open-i with no agreement step.
- **Watch out:** it's small, and de-identification replaced many tokens with "XXXX". It's fine for prototyping and as a second benchmark, but too small to train on alone.

**5. CANDID-PTX (Dunedin, New Zealand)**
- **Size:** about 19K CXRs with free-text reports, focused on pneumothorax, chest tubes and rib fractures.
- **Access:** you need a data use agreement, and typically institutional ethics approval, so it's slower to get.
- **Role:** useful as an out-of-distribution English test set from a non-US site.

## Non-English

**PadChest (Hospital San Juan, Alicante): Spanish**
- **Size:** about 160K images, 67K patients and about 110K reports, with 174 labeled findings mapped to UMLS.
- **Access:** request it through a form on the BIMCV site, agreeing not to share the data or try to re-identify anyone.
- **Watch out:** the release contains report excerpts that were preprocessed, possibly normalized. Check that the text is close enough to the original reports for your generation experiment before you rely on it.
- **PadChest-GR:** a smaller derived set with 4,555 studies and finding-level sentences in both Spanish and English, plus bounding boxes. It's good for grounded or bilingual generation, and you request it through BIMCV too.

**BIMCV-COVID19+ (Valencia)** also includes Spanish reports, but it's narrower (COVID-era cohort).

## What to skip
These are often mistaken for report datasets but only release labels or derived annotations:
- **Label-only sets:** ChestX-ray14 (NIH), the original CheXpert, VinDr-CXR and BRAX.
- **MIMIC derivatives:** Chest ImaGenome, MS-CXR and CXR-PRO add annotations or cleaned reports to MIMIC. They need the same PhysioNet credentials and don't add any new patients.
- **Caption sets:** ROCO and MedPix have figure captions, not clinical reports.

## Suggested plan
1. Start the PhysioNet credentialing now, because it has the longest lead time.
2. Meanwhile, accept the ReXGradient license and register for CheXpert Plus, which are both quick.
3. Train on MIMIC-CXR and/or CheXpert Plus, and test across institutions on ReXGradient and IU X-ray.
4. Request PadChest or PadChest-GR for the Spanish experiment.

I checked the ReXGradient, CheXpert Plus and PadChest details against current sources. The MIMIC-CXR, IU X-ray, CANDID-PTX and BIMCV details are from my own knowledge, so confirm sizes and terms on their pages before you depend on them.

Sources:
- [ReXGradient-160K paper (arXiv 2505.00228)](https://arxiv.org/abs/2505.00228)
- [ReXGradient-160K on Hugging Face (paper page)](https://huggingface.co/papers/2505.00228)
- [ReXVQA paper (alternate ReXGradient counts)](https://arxiv.org/pdf/2506.04353)
- [CheXpert Plus paper (arXiv 2405.19538)](https://arxiv.org/html/2405.19538)
- [CheXpert Plus GitHub](https://github.com/Stanford-AIMI/chexpert-plus)
- [PadChest paper (arXiv 1901.07441)](https://arxiv.org/abs/1901.07441)
- [PadChest access notes (GitHub repo)](https://github.com/auriml/Rx-thorax-automatic-captioning)
- [PadChest-GR](https://www.researchgate.net/publication/385700830_PadChest-GR_A_Bilingual_Chest_X-ray_Dataset_for_Grounded_Radiology_Report_Generation)
- [Report generation review (arXiv 2405.10842)](https://arxiv.org/pdf/2405.10842)