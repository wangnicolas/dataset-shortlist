Several English datasets pair each chest X-ray with the radiologist's original report text, and a few non-English ones do too. I checked what I could today (2026-11-11). Two official pages (Stanford AIMI and Open-i) are JavaScript apps the tool couldn't read, so those entries rest on web search.

## What I assumed you need
- **R1 (must):** a free-text radiologist report for each study, not just labels extracted from it.
- **R2 (nice to have):** English reports. Other languages are fine for a secondary experiment.
- I assumed research use only. Several licences below are non-commercial.

## Shortlist
| # | Dataset | Language | Access | Licence | Size | Checked |
|---|---|---|---|---|---|---|
| 1 | [MIMIC-CXR 2.1.0](https://physionet.org/content/mimic-cxr/2.1.0/) | English | Credentialed PhysioNet account, CITI training, signed DUA; weeks | PhysioNet Credentialed Health Data License 1.5.0 | 227,835 studies, 377,110 images | today |
| 2 | [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K) | English | Hugging Face login and click-through agreement; minutes | Non-commercial agreement | ~160,000 studies, 3 US health systems | today (registry); size per paper |
| 3 | [CheXpert Plus](https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1) | English | Register on Stanford AIMI and accept the Research Use Agreement; days | Stanford Research Use Agreement, non-commercial | 223,228 report-image pairs | web search only |
| 4 | [IU X-ray / Open-i](https://openi.nlm.nih.gov/faq) | English | Direct download from NLM | not confirmed | 3,955 reports, 7,470 images | web search only |
| 5 | [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/) | Spanish | Access request to BIMCV, then approval; weeks | PadChest Research Use Agreement | 160k+ images, ~109k reports | page read today |
| 6 | [ViX-Ray](https://huggingface.co/datasets/MilitaryHospital175/VNMedical_bv175) | Vietnamese | Open download, not gated | CC-BY-NC (registry); web search said CC BY-NC-SA 4.0 | not checked | today (registry) |
| 7 | [CASIA-CXR](https://www.casia-cxr.net/) | French | ~80 MB sample is open; full set on request | Use agreement on the site | not checked | today |

## Details
1. **MIMIC-CXR.** This is the standard benchmark. The page states "free-text radiology reports", with one `.txt` per study and a combined `mimic-cxr-reports.tar.gz`.
   - **Steps:** make a PhysioNet account, complete the CITI "Data or Specimens Only Research" course, apply for credentialing, sign the DUA, then download.
   - **Caveats:** the DUA says you won't share the data. If you plan to send reports to an online LLM service, check that clause first. Reports also mention prior exams. [CXR-PRO](https://physionet.org/content/cxr-pro/1.0.0/) is a version with those references removed (same credentialed access).
   - **Paper:** [the MIMIC-CXR dataset paper](https://doi.org/10.1038/s41597-019-0322-0).
2. **ReXGradient-160K.** Reports are split into Indication, Comparison, Findings and Impression, and there are 140k/10k/10k train/val/test splits. A further 10k test set is held back for the ReXrank leaderboard. Use is non-commercial and non-clinical only. This is the quickest large set to get.
3. **CheXpert Plus.** Search results describe it as report text, RadGraph annotations and demographics added to CheXpert images. I couldn't machine-check the page, so confirm in a browser where the images are hosted.
4. **IU X-ray / Open-i.** It's small, so it's useful mainly for cross-dataset testing rather than training. Use the NLM source, not the Kaggle or Hugging Face copies, which are unofficial mirrors. Licence terms are unconfirmed.
5. **PadChest.** This is the best large non-English option. The page says to read the Research Use Agreement before downloading. The request steps beyond that come from web search. [PadChest-GR](https://bimcv.cipf.es/bimcv-projects/padchest-gr/) is a smaller bilingual (Spanish/English) subset of 4,555 studies, also on request. I haven't read its page, so that is from web search.
   - **Paper:** [the PadChest paper](https://doi.org/10.1016/j.media.2020.101797).
6. **ViX-Ray.** It pairs PA chest X-rays with Vietnamese reports by certified radiologists. Quality and size are unchecked.
   - **Paper:** [the dataset paper](https://doi.org/10.63317/3do8tpzockx8).
7. **CASIA-CXR.** Its page says the full records "are not available to download. We may provide them upon request." Timeline unknown.

## Known, not confirmed
- **CN-X2RG / Chinese MRGMI.** A search result describes 40,000+ Chinese X-ray/report pairs as public. I didn't find or verify a download page. Check the [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-031-47401-9_8) for the data link.
- **Derived MIMIC-CXR sets** (CXR-PRO, REFLACX, RadGraph, CXRGraph) all need PhysioNet access. [REFLACX](https://physionet.org/content/reflacx-xray-localization/1.0.0/) adds eye-tracking and dictated reports.

## Not recommended, and why
- **BRAX** (Brazilian Portuguese): its page says "Free-text reports are not yet provided in the current version". It has labels only.
- **NIH ChestX-ray14, VinDr-CXR, RSNA Pneumonia, original CheXpert and MIMIC-CXR-JPG:** labels only, with no report text. This is from memory, except MIMIC-CXR-JPG, whose page I read.

## What I could not find
No public German or Portuguese chest X-ray report set turned up. I searched DataCite, Hugging Face, OpenAIRE, PhysioNet and Zenodo, plus the web. Private hospital collections wouldn't show up this way.

## Next step
Start the MIMIC-CXR credentialing now, since the CITI course and approval take the longest. While you wait, ReXGradient-160K and IU X-ray need no approval wait. For the secondary experiment, PadChest (Spanish) is the largest, and ViX-Ray (Vietnamese) is available immediately.

The interactive comparison page is at `/private/tmp/e-ByaFNw/home/cwd/dataset-shortlist.html`.

Sources: [PadChest search results](https://arxiv.org/abs/1901.07441), [CheXpert Plus](https://arxiv.org/abs/2405.19538), [ReXGradient-160K](https://arxiv.org/abs/2505.00228), [Open-i FAQ](https://openi.nlm.nih.gov/faq).