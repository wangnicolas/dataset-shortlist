I found eight datasets that pair chest X-rays with the radiologist's free-text report: five in English and three non-English. ReXGradient-160K and IU X-ray you can download today. MIMIC-CXR takes about one to two weeks of credentialing, so start that application now. All checks were done on 2026-11-12.

## What I assumed you need
- **R1 (must-have):** the original free-text report for each study, not labels extracted from it.
- **R2:** English for the main experiment. Spanish or French is fine for the secondary one.
- **R3 (assumed):** at least about 10k studies for training. Small sets are listed as test sets.
- **R4 (assumed):** you're an academic researcher, and non-commercial terms are acceptable.

## Shortlist
| # | Dataset | Language | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|---|
| 1 | **MIMIC-CXR v2.1.0** | EN | Credentialed (training + data use agreement), ~1–2 weeks | PhysioNet Credentialed DUA 1.5.0 | ~227k studies / 377k images | strong | today |
| 2 | **ReXGradient-160K** | EN | Free Hugging Face login + accept agreement, minutes | Non-commercial, non-clinical only | 160k studies / 273k images, 156 GB | strong | today |
| 3 | **CheXpert Plus** | EN | Redivis account + Stanford research use agreement, ~days | Stanford Research Use Agreement | 187,711 reports / ~223k images | strong | page today; terms from search results |
| 4 | **IU X-ray (Open-i)** | EN | Direct download, minutes | CC BY-NC-ND 4.0 (from a mirror) | 3,955 reports / 7,470 images | partial (small) | files today |
| 5 | **PadChest** | ES | Request form, ~days | CC BY-SA 4.0 (from memory) | ~110k reports / 160k images | strong for ES | site down; from papers and memory |
| 6 | **PadChest-GR** | ES + EN | On request, ~days | not confirmed | 4,555 studies, grounded | strong for evaluation | site down; from the paper |
| 7 | **CASIA-CXR** | FR | Sample open; full set on request | not stated | ~11k (from a 2026 paper) | partial | today |
| 8 | **BIMCV-COVID19+** | ES | On request | not confirmed | ~1.3k patients in release 1 | partial (COVID only) | from the paper |
| – | REFLACX | EN | PhysioNet account + DUA (images need MIMIC credentialing) | PhysioNet Restricted DUA | ~3k images | weak (evaluation only) | today |

## Details

**1. MIMIC-CXR** — https://physionet.org/content/mimic-cxr/2.1.0/
- **What's in it:** one full free-text report per study (Beth Israel Deaconess, Boston), with DICOM images. It's the default benchmark, so you'll need it for comparisons with published work (R2Gen, MAIRA-2 and similar).
- **Access, confirmed today:**
  1. Create a PhysioNet account.
  2. Complete the CITI "Data or Specimens Only Research" course.
  3. Apply for credentialing, which needs a reference.
  4. Sign the data use agreement. The page says: *"Only credentialed users who sign the DUA can access the files."*
- **Agreement terms:** no sharing the data, no attempts to re-identify anyone, and any publication must release its code.
- **Images:** for JPGs, use MIMIC-CXR-JPG (same credential). It has images and labels but no reports.
- **Limits:**
  - Access is personal: every team member must be credentialed.
  - Under PhysioNet's [LLM policy](https://physionet.org/news/post/llm-responsible-use/) you can't send the reports to a hosted LLM API unless zero data retention, no training on the data and no human review are verified.
  - Don't use the copies on Hugging Face (e.g. `X-iZhang/MIMIC-CXR-RRG`). They're unofficial, and the DUA still applies to them.

**2. ReXGradient-160K** — https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K
- **What's in it, confirmed today:** reports from 3 US health systems (79 sites), *"unaltered except for PHI removal"*. They're split into Indication, Comparison, Findings and Impression.
  - Splits: 140k train, 10k validation, 10k public test. Another 10k studies are held back as a private test set for the ReXrank leaderboard.
- **Access:** log in to Hugging Face and accept the Non-Commercial Data Access and Use Agreement.
- **Limits:**
  - Use is non-commercial and non-clinical only.
  - Images are downsampled to 25% of their original size.
  - The report sections were split out with GPT-4o.

**3. CheXpert Plus** — https://aimi.stanford.edu/datasets/chexpert-plus
- **What's in it:** *"187,711 radiology reports, each meticulously divided into 11 subsections"*, aligned with the CheXpert images (Stanford Hospital). Code is at [github.com/Stanford-AIMI/chexpert-plus](https://github.com/Stanford-AIMI/chexpert-plus).
- **Access:** the AIMI page's "Download here" link goes to Redivis.
- **Not confirmed:** the licence name (Stanford University Dataset Research Use Agreement) comes from search results, not the page itself. I couldn't read the terms page because it's built with JavaScript. Check whether approval is manual and what it says about commercial use.

**4. IU X-ray / Open-i** — https://openi.nlm.nih.gov/faq
- `NLMCXR_png.tgz` and `NLMCXR_reports.tgz` under `openi.nlm.nih.gov/imgs/collections/` both responded today.
- The reports are XML with findings and impression. The "XXXX" strings are de-identification masks.
- It's too small to train on, so use it for prototyping and as a cross-institution test set.
- The CC BY-NC-ND licence is what the Academic Torrents mirror states; I didn't confirm it on Open-i.

**5. PadChest** — https://bimcv.cipf.es/bimcv-projects/padchest/
- **What's in it:** Spanish reports from Hospital San Juan, Alicante, 2009–2017. About 1 TB, in 54 zip files.
- **Access:** a formal request through the site. You agree not to share the data and not to re-identify anyone (from the authors' GitHub). The site returned 503 errors today, so I couldn't confirm the current form.
- **Caveat for generation:** the released report text has been normalised: lower-cased, with stop words and word endings stripped. It isn't raw prose.

**6. PadChest-GR** — https://bimcv.cipf.es/bimcv-projects/padchest-gr/ ([NEJM AI 2025](https://doi.org/10.1056/aidbp2401120))
- Built for grounded report generation: finding sentences (present and absent) in both English and Spanish, each with a bounding box.
- Available on request.
- Good for a bilingual secondary experiment.

**7. CASIA-CXR** — https://www.casia-cxr.net/ ([Neurocomputing 2024](https://dl.acm.org/doi/10.1016/j.neucom.2024.128478))
- **What's in it:** reports *"originally written in French"* with high-resolution frontal JPEGs from several French hospitals.
- **Access:** an ~80 MB sample is downloadable. For the full records the site says *"We may provide them upon request."*
- **Not confirmed:** no licence is stated on the pages I could read. The Hugging Face copy (FrancophonIA/CASIA-CXR) is empty.

**8. BIMCV-COVID19+** ([arXiv 2006.01174](https://arxiv.org/abs/2006.01174))
- Spanish reports for COVID-19-positive patients from 11 hospitals in the Valencia region, available on request through BIMCV.
- The population is narrow, and it mixes CXR with CT, so you'd filter to the X-ray studies.

## Not recommended, and why
- **CANDID-PTX:** it does have 19k free-text reports, but the figshare record says today: *"not available for access by users outside Health New Zealand"* (closed since February 2024).
- **CheXpert (original), NIH ChestX-ray14, VinDr-CXR:** labels only, no report text. CheXpert's reports are what CheXpert Plus adds.
- **PARROT:** multilingual, but the reports are fictional and there are no images.

## What I could not find
- No public chest X-ray dataset with images and reports in Chinese, German, Portuguese or Vietnamese turned up.
- I couldn't confirm the current request forms or licences for the BIMCV datasets (PadChest, PadChest-GR, BIMCV-COVID19+) because the site was down. Retry it before you plan around them.

## Next step
1. Today: start MIMIC-CXR credentialing (the CITI course takes a few hours), accept the ReXGradient agreement, and download IU X-ray.
2. For the secondary experiment, PadChest-GR is the simplest choice: one study set with reports in both languages. If you'd rather have full-length non-English report text, use CASIA-CXR (French), since PadChest's released Spanish reports are preprocessed.
3. Check with your institution whether this work needs an ethics review exemption.

The interactive page with filters and an access-plan export is at `/private/tmp/e-tg8IBR/home/cwd/dataset-shortlist.html`.

Sources: [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/), [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K), [CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus), [CheXpert Plus paper](https://arxiv.org/abs/2405.19538), [Open-i FAQ](https://openi.nlm.nih.gov/faq), [IU X-ray on Academic Torrents](https://academictorrents.com/details/5a3a439df24931f410fac269b87b050203d9467d), [PadChest paper](https://arxiv.org/abs/1901.07441), [PadChest README](https://github.com/auriml/Rx-thorax-automatic-captioning), [PadChest-GR](https://arxiv.org/abs/2411.05085), [CASIA-CXR](https://www.casia-cxr.net/), [BIMCV-COVID19+](https://arxiv.org/abs/2006.01174), [CANDID-PTX](https://figshare.com/articles/dataset/CANDID-PTX/14173982), [REFLACX](https://physionet.org/content/reflacx-xray-localization/1.0.0/), [Awesome-RRG list](https://github.com/mk-runner/Awesome-Radiology-Report-Generation)