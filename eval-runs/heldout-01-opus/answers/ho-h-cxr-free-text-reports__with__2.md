I found eight datasets that pair chest X-rays with the radiologist's report text, plus two smaller supplements. Three are large English sets: MIMIC-CXR, CheXpert Plus and ReXGradient-160K. The only English set you can download today with no sign-up or agreement is the small IU X-ray set. For the non-English experiment, Spanish (PadChest) is the strongest option. All checks were done on 2026-11-12.

## What I assumed you need
- **R1 (must have):** the original free-text report linked to each image or study, not just labels.
- **R2:** English reports; one non-English set is fine for a secondary experiment.
- **R3:** enough data to train a model (tens of thousands of studies or more). A small set is still useful for evaluation.
- **Assumed:** non-commercial academic research, and you can wait days to weeks for credentialing.

## Shortlist
| # | Dataset | Language | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR v2.1.0 | EN | Application: PhysioNet credentialing + CITI training + data agreement, ~1–3 weeks | PhysioNet Credentialed DUA 1.5.0 | 377k images / 227k studies | strong | today |
| 2 | CheXpert Plus | EN | Log in on Redivis and accept Stanford's research use agreement, ~days | Stanford research use agreement, non-commercial | 223k pairs / 187,711 reports | strong | today (page); terms from search results |
| 3 | ReXGradient-160K | EN | Free Hugging Face account, agreement accepted automatically, minutes | Non-commercial agreement | 160k studies / 273k images, 79 US sites | strong | today |
| 4 | IU X-ray (Open-i) | EN | Open download, minutes | CC BY-NC-ND 4.0 (from memory) | ~3,955 reports / 7,470 images | strong but small | from memory |
| 5 | PadChest | ES | Request form, ~days | Not stated; no sharing, no re-identification | 160k images / 109,931 studies | partial | search results (site down) |
| 6 | PadChest-GR | ES + EN | Request form, ~days | Not stated | 4,555 studies with grounded findings | strong (bilingual) | search results (site down) |
| 7 | CASIA-CXR | FR | Sample download; full set by request form and use agreement | Not named on site | Not stated (several thousand exams) | partial | today |
| 8 | REFLACX | EN | PhysioNet account + agreement (images need MIMIC credentialing) | PhysioNet Restricted DUA | ~3k readings (from memory) | supplement | today |
| 9 | BIMCV-COVID19+ | ES | Request + research use agreement | BIMCV agreement | Thousands of studies, COVID+ only | partial | search results |
| 10 | Naija-CXR | EN | Open Zenodo download | CC BY 4.0, but the text says non-commercial | 389 MB, count unknown | weak / unknown | today |

## Details
**1. MIMIC-CXR**: https://physionet.org/content/mimic-cxr/2.1.0/
- **Contents:** images from Beth Israel Deaconess in Boston, each study with its full report (findings and impression sections). It is the main benchmark in this field.
- **Access:** create a PhysioNet account → apply for credentialing (ID check and a reference) → complete the CITI "Data or Specimens Only Research" course → sign the agreement on the project page.
- **Agreement terms** (quoted on the page): no sharing, no attempt to re-identify, and "any publication which makes use of the data will also make the relevant code available."
- **Images:** MIMIC-CXR-JPG has JPGs and labels but no reports. Most papers use its images with the MIMIC-CXR reports; the same credential covers both.
- **Watch out:** PhysioNet's rules forbid sending this data to third-party online LLM services, so use local models or an approved cloud setup. Reports often refer to earlier exams; CXR-PRO on PhysioNet is a cleaned version with those references removed.
- **Paper using it:** "Evaluating progress in automatic chest X-ray radiology report generation" (Patterns 2023, [10.1016/j.patter.2023.100802](https://doi.org/10.1016/j.patter.2023.100802)), which introduced the RadGraph F1 and RadCliQ metrics.

**2. CheXpert Plus**: https://aimi.stanford.edu/datasets/chexpert-plus
- **Contents:** Stanford Hospital reports, each split into 11 sections, with images as DICOM and PNG.
- **Access:** follow "Download here" to Redivis, log in, accept the agreement, then download the `df_chexpert_plus` CSV (the reports) and the images.
- **Terms:** search results quoting the agreement say research use only, no commercial use, no redistribution. I couldn't confirm whether Redivis approves requests automatically or by hand.
- **Why use it:** it is a second large English hospital, which makes it a good check of how well a MIMIC-trained model transfers.

**3. ReXGradient-160K**: https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K
- **Contents:** reports with Indication, Comparison, Findings and Impression sections. Official train/validation/test splits are 140k/10k/10k, and a further 10k private test set backs the ReXrank leaderboard.
- **Access:** log in to Hugging Face and accept the agreement; this is the fastest way to get large-scale English data.
- **Limits:** non-commercial and non-clinical use only, no redistribution. Images are PNGs shrunk to 25% of original size.

**4. IU X-ray / Open-i** (openi.nlm.nih.gov)
- **Contents:** findings and impression text with frontal and lateral images. You can start on it today; it's commonly used as a second test set.
- **Check:** the site is a JavaScript app the tool couldn't read, so the download link and the CC BY-NC-ND licence are from memory. Confirm them in a browser and use the NLM original rather than Hugging Face copies.

**5–6. PadChest and PadChest-GR** (BIMCV, Spain): bimcv.cipf.es/bimcv-projects/padchest/ and /padchest-gr/
- **PadChest:** Spanish reports from Hospital San Juan, about 1 TB. **Caveat:** the released report text was heavily normalised for anonymisation (case, accents and stop-words removed), so it isn't natural prose.
- **PadChest-GR:** reports written by radiologists in both Spanish and English, with a box for each finding. It is the cleanest bilingual option ([NEJM AI 2025](https://doi.org/10.1056/aidbp2401120)), but the reports were curated for the dataset rather than taken from clinical practice.
- **Access:** the BIMCV site returned errors (HTTP 503) today, so the request-form process comes from secondary sources ([arXiv 1901.07441](https://arxiv.org/abs/1901.07441), [authors' GitHub](https://github.com/auriml/Rx-thorax-automatic-captioning)).

**7. CASIA-CXR (French)**: https://www.casia-cxr.net/
- **Contents:** narrative reports "originally written in French" ([Neurocomputing 2024](https://doi.org/10.1016/j.neucom.2024.128478)).
- **Access:** an ~80 MB sample is downloadable now; the full set needs a request form and a use agreement.
- **Unknowns:** the site gives no total size and names no licence.

**8. REFLACX**: https://physionet.org/content/reflacx-xray-localization/1.0.0/
- Reports dictated by radiologists while their eye movements were tracked, on MIMIC-CXR images. Useful as a supplement, not on its own.

**9. BIMCV-COVID19+**: Spanish reports, COVID-positive patients only, available by request under BIMCV's research use agreement. Its population is narrow.

**10. Naija-CXR**: https://zenodo.org/records/21781842
- A new (2026) Nigerian dataset whose contents list "free radiologist reports." Report coverage and image count aren't stated.
- The record says CC BY 4.0, but its description limits use to non-commercial research, so treat it as non-commercial.

## Known, not confirmed
- **IU X-ray:** the licence and download page are from memory.
- **PadChest family:** the exact terms are unconfirmed because the BIMCV site was down. Check both before you plan around them.

## Not recommended, and why
- **MIMIC-CXR-JPG, original CheXpert, NIH ChestX-ray14, VinDr-CXR:** labels or boxes only, no report text.
- **BRAX (Brazil):** labels taken from Portuguese reports; the report text isn't released (from memory).
- **CANDID-PTX (New Zealand):** has 19,237 X-rays with free-text reports, but since 2024 it is closed to anyone outside Health New Zealand (figshare record, version 2).
- **FMCEB-CXR:** 5,517 Nigerian reports, but I couldn't confirm it includes the images.
- **MIMIC add-ons (CXR-PRO, RadGraph, ReXErr, etc.):** processed versions of MIMIC-CXR, not new image–report sources.

## What I could not find
- An English set bigger than IU X-ray that you can download with no sign-up or agreement.
- Report sets in German, Chinese, Japanese or Korean weren't searched in depth.

## Next step
Start PhysioNet credentialing now, since it takes the longest. While it runs, you can be working within the hour: accept the ReXGradient-160K agreement and download the IU X-ray set. For the secondary experiment, submit a PadChest-GR request: being bilingual, it gives you a direct English vs. Spanish comparison. Request full PadChest as well if you want scale.

The interactive shortlist is at `/private/tmp/e-kZvH16/home/cwd/dataset-shortlist.html`.

Sources: [CheXpert Plus paper](https://arxiv.org/pdf/2405.19538), [AIMI data](https://aimi.stanford.edu/data), [CANDID-PTX figshare](https://auckland.figshare.com/articles/dataset/CANDID-PTX/14173982), [CASIA-CXR OpenReview](https://openreview.net/forum?id=4tj6oWXDGo), [BIMCV-COVID19 datos.gob.es](https://datos.gob.es/es/catalogo/pudat0002-bimcv-covid-19-un-gran-conjunto-de-datos-anotados-de-imagenes-de-rx-y-tc-de-pacientes-con-covid-19), [BIMCV-COVID19 arXiv](https://arxiv.org/abs/2006.01174), [PadChest-GR arXiv](https://arxiv.org/html/2411.05085v1)