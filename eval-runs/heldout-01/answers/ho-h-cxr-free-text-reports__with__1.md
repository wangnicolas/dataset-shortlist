## What I assumed you need
- **R1 (must):** chest X-ray images.
- **R2 (must):** the radiologist's original free-text report for each image or study, not only labels extracted from it.
- Nice-to-have: English first, with one non-English set for a secondary experiment. I assumed non-commercial academic use, and that waiting days for access is acceptable.

I searched DataCite, Hugging Face, OpenAIRE, PhysioNet and Zenodo (about 200 candidates) and did web searches for datasets the registries don't index. "Checked" below says how I know each fact. Checks were done 2026-11-12.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR | Credentialed PhysioNet access, days | PhysioNet Credentialed Health Data License 1.5.0 | 377,110 images, 227,835 studies, 5.1 TB | Strong, English | Today (PhysioNet record and page) |
| 2 | CheXpert Plus | Stanford agreement, days | Stanford Dataset Research Use Agreement | ~223k image-report pairs, 187,711 studies | Strong, English | Web search only |
| 3 | ReXGradient-160K | Hugging Face login plus agreement, minutes | Non-commercial agreement | ~160k studies (from memory) | Strong, English | Access today, contents from memory |
| 4 | IU X-Ray (Open-i) | Open download, minutes | Not confirmed | 3,955 reports, 7,470 images | Strong but small, English | Size from search; terms not readable |
| 5 | PadChest (BIMCV) | Request form, weeks | BIMCV agreement | ~160k images, ~109k reports, ~1 TB | Strong, **Spanish** | Web search only |
| 6 | REFLACX | Free PhysioNet account plus restricted DUA, minutes | PhysioNet Restricted Health Data License | 3,032 cases | Partial, English | Today |
| 7 | Naija-CXR | Open on Zenodo, minutes | CC-BY-4.0 in the record; the description says non-commercial | Not stated | Partial, English | Today (page text) |

## Details
**1. [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/)**
- It has DICOM chest radiographs with free-text reports from Beth Israel Deaconess Medical Center. It is the standard report-generation benchmark.
- **Access (confirmed):** "Only credentialed users who sign the DUA can access the files."
- **Steps:**
  1. Make a PhysioNet account.
  2. Complete the CITI human-subjects training.
  3. Apply for credentialing. This is personal and the usual wait is days. That timing is from memory.
  4. Sign the data use agreement on the project page.
- **Terms:** the agreement forbids sharing the data. PhysioNet's [24 Sept 2025 post](https://physionet.org/news/post/llm-responsible-use/) says you may not send credentialed data through APIs or online platforms, so use locally deployed models only.
- **Reports:** the reports contain de-identification placeholders.

**2. [CheXpert Plus](https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1)**
- It adds de-identified reports, split into sections, to the CheXpert images. It also has CheXbert labels, RadGraph-XL annotations and demographics.
- **Access:** accept Stanford's research use agreement on the AIMI site. It is research-only, with no commercial use and no redistribution. The full set is about 6.8 TB.
- **Not confirmed:** this comes from search snippets, not the page itself. The pair count is 223,228 unique pairs in the paper's text and 223,462 in its table.

**3. [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)**
- **Access (confirmed):** the repo is gated. You accept the "ReXGradient-160K Non-Commercial Data Access and Use Agreement" with a Hugging Face login. It is non-commercial and non-clinical only.
- **From memory, not confirmed:** it is a multi-site set of about 160k studies with reports. Check the dataset card for the report fields.

**4. [IU X-Ray / Open-i](https://openi.nlm.nih.gov/)**
- The NLM FAQ is reported to give 3,955 reports (XML, with indication, findings and impression) and 7,470 images (PNG or DICOM). The usual published counts agree.
- The Open-i page is drawn by JavaScript, so I could not read its terms. Check the NLM terms before redistributing.
- Use the NLM copy rather than the Hugging Face mirrors, which are unofficial.
- It is small, so it works for a quick run but not for pretraining.

**5. [PadChest](http://bimcv.cipf.es/bimcv-projects/padchest/)**
- This is your non-English set. It has Spanish reports from San Juan Hospital (2009–2017), 67k patients, 54 zip files, about 1 TB.
- **Access (from search results):** request through the BIMCV form and agree not to share the data or re-identify anyone. The URL may have moved, so check it. Allow weeks.
- **Public reports:** they were heavily processed for anonymisation. [PadChest-GR](https://arxiv.org/abs/2411.05085) retrieved the original, anonymised reports and is bilingual.

**6. [REFLACX](https://physionet.org/content/reflacx-xray-localization/1.0.0/)**
- **Contents:** radiologists dictated reports on 3,032 frontal MIMIC-CXR images, with timestamped transcripts and eye tracking.
- **Access (confirmed):** "Only registered users who sign the specified data use agreement can access the files." You need a free account, not credentialing.
- **Limit:** it is small. The images also need MIMIC-CXR access.

**7. [Naija-CXR](https://zenodo.org/records/21781842)**
- The page says frontal CXRs are "paired with expert radiologist annotations and diagnostic reports". It is open, so you can start on it today.
- **Not confirmed:** I don't know the size or whether the reports are raw text.
- **Licence conflict:** the record says CC-BY-4.0, but the text says "non-commercial scientific research and educational purposes only". Treat it as non-commercial.

## Known, not confirmed
- **[FMCEB-CXR](https://zenodo.org/records/20750284)** (Zenodo, CC-BY-4.0) is built from 5,517 reports from a Lagos hospital. The page does not say whether the raw report text is released or only labels extracted from it. Open the files to check before using it.
- **PadChest, CheXpert Plus and IU X-Ray** are listed above and need a first-hand look at their access pages. I did not verify them through a registry.

## Not recommended, and why
- **NIH ChestX-ray14, VinDr-CXR and similar:** labels only, with no report text (from memory).
- **MIMIC-CXR-JPG:** images and labels. The reports are in MIMIC-CXR.
- **BRAX:** its 14 labels came from Brazilian Portuguese reports, but the page doesn't say the report text is released.
- **Derivatives such as RadGraph and CXR-PRO:** annotations built on MIMIC-CXR reports, useful add-ons but not independent report sets.
- **Hugging Face copies of IU X-Ray:** unofficial mirrors, so use the NLM source.

## What I could not find
I found no open, non-English chest X-ray set with full report text confirmed. PadChest is the best non-English option and needs a request. I did not search for Chinese, German or Portuguese hospital sets. I did not run the evidence-of-use paper lookup per dataset.

## Next step
Start with IU X-Ray, REFLACX or ReXGradient while you apply for credentialing for MIMIC-CXR and send the PadChest request. For a first model, the standard route is to train on MIMIC-CXR and test on IU X-Ray.

Interactive page: `/private/tmp/e-zuULR7/home/cwd/dataset-shortlist.html`