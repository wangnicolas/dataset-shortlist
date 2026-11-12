Four English datasets and four non-English ones have real report text and are obtainable. Two of the English ones (Open-i and ReXGradient-160K) can be downloaded today, and MIMIC-CXR takes a credentialing application. Everything was checked on 12 Nov 2026; "from memory" marks what I could not confirm at source.

## What I assumed you need
- **Must:** chest X-ray images paired with report text; the text is the radiologist's own prose (not labels, captions or synthetic text); an outside researcher can actually get it.
- **Nice to have:** English; tens of thousands of studies or an established benchmark; quick access.
- **Assumed:** academic, non-commercial use. Almost every dataset below forbids commercial use, so say if that is wrong.

## Shortlist
| # | Dataset | Language | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR | English | Application: PhysioNet credentialing, training course and signed agreement; days to ~2 weeks | PhysioNet Credentialed DUA 1.5.0 | 227,835 studies, 377,110 images | Strong | today (timing from memory) |
| 2 | ReXGradient-160K | English | Free Hugging Face account, automatic click-through; minutes | Custom, non-commercial | 160,000 studies, 273,004 images, 156 GB | Strong | today |
| 3 | IU X-Ray (Open-i) | English | Direct download, no login; minutes | CC BY-NC-ND 4.0 | ~3,955 reports, ~7,470 images, 1.4 GB | Strong but small | today (licence via secondary sources) |
| 4 | CheXpert Plus | English | Account and click-through via Redivis, I believe; steps not confirmed | Sources conflict (see details) | 187,711 reports, 223,462 images | Strong | partly today |
| 5 | Interpret-CXR (RRG24) | English, partly machine-translated | Application: owner approves, training certificate needed; days | None stated | ~196k findings plus MIMIC built locally, 74.5 GB | Partial | today |
| 6 | PadChest | Spanish | Google Form and research use agreement; turnaround not stated | Custom, research only | 109,931 reports, 160,868 images, 1.02 TB | Partial | today |
| 7 | CASIA-CXR | French | Application: request form and signed agreement; turnaround not stated | Custom, academic only | ~11k pairs (from memory) | Partial | today |
| 8 | PadChest-GR | Spanish and English | Google Form and research use agreement | Custom, research only | 4,555 studies, 46 GB | Partial | today |
| 9 | BIMCV-COVID19+ | Spanish (from memory) | Google Form and research use agreement | Custom | 56,171 X-ray studies | Partial | today |
| 10 | REFLACX | English | Free PhysioNet account and agreement click; minutes | PhysioNet Restricted DUA 1.5.0 | ~3,000 reports (from memory) | Weak, supplement only | today |

## Details

**1. [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/)** is the standard benchmark, from Beth Israel Deaconess in Boston.
- **Contents:** one plain-text report per study, with identifying details replaced by `___`.
- **Steps:** create a PhysioNet account, apply for credentialed status, complete the CITI "Data or Specimens Only Research" course, then sign the agreement on the project page. The need for a named reference is from memory.
- **Download:** take the reports archive plus [MIMIC-CXR-JPG](https://physionet.org/content/mimic-cxr-jpg/2.1.0/) (612 GB) for the images, rather than the 5.1 TB of DICOMs.
- **Conditions:** access is personal, so each team member applies separately. You may not share the data, and you must release the code behind any publication.
- **Hosted language models:** PhysioNet's 2025 policy forbids sending this data through third-party APIs unless zero retention, no training use and no human review are verified. This matters if you plan LLM-based evaluation or rewriting; I took it from the skill's notes, so [check the policy](https://physionet.org/news/post/llm-responsible-use/).

**2. [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)** is the largest set you can have today, from 109,487 patients at three US health systems.
- **Contents:** reports with Indication, Comparison, Findings and Impression; a 140k/10k/10k split.
- **Steps:** log in to Hugging Face and accept the agreement.
- **Conditions:** "No commercial use of the Data is permitted"; no disclosure to third parties; credit Gradient Health in every publication.
- **Limits:** images are PNGs downsampled to 25% of the original dimensions. The agreement does not say whether you may publish trained weights.

**3. [IU X-Ray / Open-i](https://openi.nlm.nih.gov/faq)** is the only fully open one, and the usual second benchmark.
- **Steps:** download `NLMCXR_reports.tgz` (1.1 MB) and `NLMCXR_png.tgz` (1.36 GB) from the FAQ's "Where can I get the Chest X-ray images" entry. Both answered without login today.
- **Limits:** too small to train on alone, many words are masked as `XXXX`, and there is no official split.
- **Licence:** non-commercial, no derivatives. I could not read the FAQ page itself, so this comes from a search snippet of it and a 2024 AJR letter.

**4. [CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus)** covers 64,725 Stanford patients, so it gives you a second large site for cross-hospital evaluation.
- **Contents:** each report is split into 11 sections; images come as DICOM and PNG.
- **Steps:** the page's "Download here" link goes to Redivis. Creating an account and accepting Stanford's terms there is from memory.
- **Licence conflict:** the Stanford portal's own record names the "Open Use of Data Agreement v1.0", which permits redistribution. The paper and other sources say the Stanford Research Use Agreement, which is non-commercial with no redistribution. Assume non-commercial until you see the terms at download.
- **Size:** 3.46 TB in total. A third party reports a Redivis export cap of 100 GB per 30 days, which I could not verify.

**5. [Interpret-CXR](https://huggingface.co/datasets/StanfordAIMI/rrg24-shared-task-bionlp)** is a ready-made Findings/Impression training set from the RRG24 shared task.
- **Contents:** sections drawn from CheXpert, PadChest, BIMCV-COVID19 and Open-i, plus a script to add MIMIC-CXR once you hold that credential.
- **Steps:** submit your Hugging Face details and a CITI training verification link, then wait for owner approval.
- **Limits:** the PadChest and BIMCV text is GPT-4 translation from Spanish, not what the radiologist wrote.

**6. [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/)** is the largest non-English option, from Hospital San Juan in Alicante.
- **Steps:** read the [research use agreement](https://bimcv.cipf.es/bimcv-projects/padchest/padchest-dataset-research-use-agreement/), then fill in the Google Form behind "Descargar Dataset completo". The page does not say whether requests are reviewed.
- **Limits:** the paper describes the `Report` field as "a text snippet extracted from the original report", so it is an excerpt. From memory it is also lower-cased with punctuation stripped; look at the 167 MB Kaggle sample linked on the page before committing.
- **Conditions:** research only; do not pass the link outside your organisation.

**7. [CASIA-CXR](https://www.casia-cxr.net/)** has reports written natively in French and was built for report generation, with published baselines.
- **Steps:** submit the request form with an institutional email and a project description, then sign the agreement the authors send. An 80 MB sample downloads freely.
- **Conditions:** the agreement forbids translating the reports into other languages without written permission, which rules out translate-then-train. No redistribution.

**8. [PadChest-GR](https://bimcv.cipf.es/bimcv-projects/padchest-gr/)** is a bilingual evaluation set with radiologist-drawn boxes.
- **Limits:** the 10,459 one-finding sentences were produced by GPT-4 extraction and translation, then checked by radiologists, so they are not the original prose.
- **Steps:** same form and agreement as PadChest.

**9. [BIMCV-COVID19+](https://bimcv.cipf.es/bimcv-projects/bimcv-covid19/)** is a second Spanish source from the Valencia region.
- **Contents:** the page confirms radiology reports are included; that they are Spanish free text is from memory.
- **Limits:** all patients are COVID-19 positive, so the mix of findings is skewed. It also holds 7,918 CT studies to filter out.
- **Steps:** Google Form for "Iteration 1+2+3".

**10. [REFLACX](https://physionet.org/content/reflacx-xray-localization/1.0.0/)** has reports freshly dictated by radiologists for MIMIC-CXR frontal images, with eye tracking. It is useful as second-reader references, but the images still need the MIMIC credential.

**Papers that used these:**
- MIMIC-CXR: [describing paper](https://www.nature.com/articles/s41597-019-0322-0); [cross-domain audit with IU X-Ray](https://doi.org/10.2196/95888).
- ReXGradient-160K: [describing paper](https://arxiv.org/pdf/2505.00228).
- IU X-Ray: [describing paper](https://scholarworks.indianapolis.iu.edu/server/api/core/bitstreams/9ab6a7d1-790f-4fc1-85b9-18afeb0d0c3f/content).
- CheXpert Plus: [describing paper](https://arxiv.org/pdf/2405.19538); [LLaVA-Rad](https://doi.org/10.1038/s41467-025-58344-x); [AAAI 2026 report generation](https://doi.org/10.1609/aaai.v40i40.40688).
- Interpret-CXR: [RRG24 system paper](https://aclanthology.org/2024.bionlp-1.51.pdf).
- PadChest: [describing paper](https://arxiv.org/html/1901.07441v2). PadChest-GR: [NEJM AI](https://doi.org/10.1056/aidbp2401120).
- CASIA-CXR: [Neurocomputing 2024](https://www.sciencedirect.com/science/article/abs/pii/S0925231224012499).

## Known, not confirmed
- **CheXpert Plus:** the dataset and its contents are confirmed from Stanford's pages. The current download steps and governing licence are not; check the Redivis page.
- **Open-i:** the files are confirmed downloadable. The licence wording is second-hand.

## Not recommended, and why
- **[CANDID-PTX](https://auckland.figshare.com/articles/dataset/CANDID-PTX/14173982) and CANDID** (New Zealand, 19k and 53k radiographs with reports): the CANDID-PTX record states that since Feb 2024 it "is not available for access by users outside Health New Zealand". The larger CANDID record could not be read; whether it is closed too is my assumption.
- **[BRAX](https://physionet.org/content/brax/1.1.0/)**: labels derived from Portuguese reports, but the report text is not released (from memory).
- **CheXpert (original), NIH ChestX-ray14, VinDr-CXR**: images and labels only.
- **CX-CHR, CH-Xray (Chinese)**: used in papers but not publicly released, per search results.
- **Kaggle, Hugging Face or torrent copies** of IU X-Ray, MIMIC-CXR or PadChest: unofficial mirrors; the original terms still apply.

## What I could not find
- No public chest X-ray set with native German, Portuguese, Japanese, Korean, Italian, Russian, Vietnamese or Chinese report text that an outsider can obtain.
- I did not check MIDRC or Emory CXR.
- One paper index was down, so the evidence-of-use list is thinner than it could be.

## Next step
Download IU X-Ray and accept the ReXGradient-160K terms today, and start the PhysioNet credentialing now, since its training certificate also serves the Interpret-CXR request. For the secondary experiment, send the PadChest form and the CASIA-CXR request in parallel, because neither states a turnaround.

The interactive version, with filters and an exportable access plan, is at `/private/tmp/e-0kxBml/home/cwd/dataset-shortlist.html`.