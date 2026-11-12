## What I assumed you need

- **R1 (must):** each image or study comes with the radiologist's actual free-text report, not only labels extracted from it.
- **R2 (preferred):** English reports. A non-English set is fine for a secondary experiment.
- I assumed you'd accept an application if the data is worth it. I flag below what you can start on today.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR (v2.1.0) | Credentialed PhysioNet account, CITI training, signed DUA; days to weeks | PhysioNet Credentialed Health Data License | ~377k images, ~227k studies | Strong, English | Access terms today; size from memory |
| 2 | CheXpert Plus (Stanford AIMI) | Redivis login and terms. The exact tier wasn't readable (from memory: research-use agreement) | Not stated on the pages I could read | 223,462 report–image pairs, 187,711 reports, 64,725 patients | Strong, English | Size today; access partly from memory |
| 3 | ReXGradient-160K | Hugging Face login, accept the gated non-commercial agreement; minutes | Custom non-commercial agreement | 160k studies, 273k images | Strong, English | Today |
| 4 | PadChest (BIMCV) | Google Form request after reading the research use agreement; days to weeks (from memory) | Governed by the agreement; no open licence named | >160k images, ~67k patients, 1.02 TB (167 MB sample on Kaggle) | Strong, **Spanish** | Today |
| 5 | Naija-CXR | Open download from Zenodo; minutes | CC-BY-4.0 | ~390 MB | Partial: reports are mentioned, but I didn't inspect them | Today |

## Details

**1. [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/)**
- It has the original findings and impression text for each study.
- Steps:
  - Create a PhysioNet account.
  - Complete CITI "Data or Specimens Only Research" training.
  - Apply for credentialing.
  - Sign the DUA for your project.
- PhysioNet says: "Only credentialed users who sign the DUA can access the files." The DUA bars you from sharing the data.
- If you plan to send reports to a hosted LLM API, check the DUA first. PhysioNet has restricted this before (from memory).
- Many reports refer to prior exams the model never sees. [CXR-PRO](https://physionet.org/content/cxr-pro/1.0.0/) (same access) removes those references. I found it in the search but didn't verify it further.

**2. [CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus)**
- The [AIMI page](https://aimi.stanford.edu/datasets/chexpert-plus) says it has "223,462 unique pairs of radiology reports and chest X-rays".
- Each report is split into 11 subsections.
- Download goes through a Redivis page. The AIMI page's Terms and Licence sections were empty when I fetched it. Contact aimicenter@stanford.edu if the terms are unclear.

**3. [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)**
- This is the quickest large English set to get.
- Reports are unaltered apart from PHI removal and section splitting, per the [paper](https://arxiv.org/abs/2505.00228).
- The agreement is for non-commercial, non-clinical research and has no redistribution.
- Sources disagree on the number of sites and studies (160k vs 170k). A 10k private test set is held back for the ReXrank leaderboard.

**4. [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/)**
- This is my pick for the non-English experiment, with reports in Spanish.
- The agreement forbids sharing the data and re-identification.
- From memory, only part of the reports are expert-labelled and the rest are auto-labelled. The report text is all radiologist-written.

**5. [Naija-CXR](https://zenodo.org/records/21781842)**
- Its Zenodo description says images come with "expert radiologist annotations and diagnostic reports".
- I didn't open the files, so check they are free text before relying on it.

## Known, not confirmed

- **IU X-Ray / Open-i (Indiana University).**
  - From web search: 7,470 chest X-rays with 3,955 reports (indication, findings, impression), downloadable from NLM with no application.
  - The verifier couldn't check the site because it's a JavaScript app, so open it in a browser.
  - Search results disagree on the licence (one source says CC BY-NC-ND 4.0), so read the terms on the NLM page.
  - It's small, but it's the standard quick-start set, and the one you could start on today.
  - The Hugging Face and Kaggle copies are unofficial mirrors. Use the NLM source.
- **CheXpert Plus tier and licence.** What I believe is research-use terms. I couldn't confirm it.

## Not recommended, and why

- **NIH ChestX-ray14:** labels were mined from reports, and the reports aren't released.
- **MIMIC-CXR-JPG:** images plus structured labels only. Take reports from MIMIC-CXR.
- **BRAX:** labels only, no free text (from memory).
- **FMCEB-CXR (Nigeria):** 5,517 reports with NLP labels, but the record is a 42 KB file with no images.

## What I could not find

- I didn't survey other non-English sets beyond PadChest. BIMCV-COVID19 (Spanish) and Chinese-language collections are worth a look. I didn't search for them.
- Registries searched were PhysioNet, Zenodo, DataCite, OpenAIRE and Hugging Face, plus literature and web search. Any of the checks above may be out of date, so confirm before applying.
- I checked on 2026-11-11 and 2026-11-12.

## Next step

Start your PhysioNet credentialing now, since it's the slowest step and MIMIC-CXR is the standard benchmark. In parallel, accept the ReXGradient-160K terms on Hugging Face and pull IU X-Ray for a quick pipeline test. Then request PadChest for the Spanish experiment.

The interactive page is at `/private/tmp/e-RVOBlu/home/cwd/dataset-shortlist.html`.