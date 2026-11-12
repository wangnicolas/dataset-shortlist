For English report generation, you can start today with **ReXGradient-160K** (Hugging Face, click-through agreement). **MIMIC-CXR** is the benchmark reviewers will expect you to use, and its credentialing takes about 1–3 weeks, so apply now. For the non-English experiment, **PadChest-GR** (Spanish + English) and **CASIA-CXR** (French) are the realistic choices. I checked everything on 2026-11-12.

## What I assumed you need
- **R1 (must):** the radiologist's original free-text report for each study, not extracted labels.
- **R2 (preferred):** English, with one non-English set for a second experiment.
- **R3 (preferred):** at least ~10k studies for the main training set.
- **R4 (must):** an academic researcher can get it. I assumed non-commercial use is fine.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR v2.1.0 | PhysioNet credentialing + CITI training + DUA, ~1–3 weeks | PhysioNet Credentialed Health DUA 1.5.0 | 227k studies / 377k images | strong | today |
| 2 | ReXGradient-160K | HF login + accept agreement, minutes | non-commercial DUA | 160k studies / 273k images | strong | today |
| 3 | CheXpert Plus | free Stanford AIMI account + research use agreement, ~days | Stanford research use, non-commercial | 187k studies / 223k pairs | strong | web search (portal can't be read by script) |
| 4 | IU X-ray (Open-i) | direct download, minutes | CC BY-NC-ND 4.0 | 3,955 reports / 7,470 images | partial (small) | web search (Open-i FAQ) |
| 5 | Naija-CXR (Nigeria) | direct download, minutes | Zenodo lists CC BY 4.0, but the description says non-commercial only | 389 MB zip | partial | today |
| 6 | CASIA-CXR (French) | sample open; full set needs a request form + hand-signed DUA, ~weeks | custom, academic | not checked | partial (non-English) | today |
| 7 | PadChest (Spanish) | request form, ~days | from memory CC BY-SA 4.0, not confirmed | 160k images / 67k patients | partial | papers/GitHub (site down) |
| 8 | PadChest-GR (Spanish + English) | request form, ~days | not confirmed | 4,555 studies | partial | papers (site down) |

## Details
**1. MIMIC-CXR** – https://physionet.org/content/mimic-cxr/2.1.0/
- **Contents:** the full original reports from Beth Israel Deaconess, Boston. This is the default benchmark (RadGraph F1, RadCliQ, ReXrank all report on it).
- **Steps:**
  1. Create a PhysioNet account.
  2. Apply for credentialed access.
  3. Complete CITI "Data or Specimens Only Research" training and upload the certificate.
  4. Sign the DUA on the project page.
- **DUA terms (quoted from the page today):** you will "not share the data", make "no attempt to reidentify individuals", and publications "will also make the relevant code available."
- **Practical notes:**
  - Use the MIMIC-CXR-JPG images (same credentials) with the reports from this project.
  - Don't send reports to online LLM APIs without checking PhysioNet's rules on that.
  - The derived sets (MS-CXR, Chest ImaGenome, CXR-PRO, ReXErr, RadGraph, REFLACX) come with the same terms.

**2. ReXGradient-160K** – https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K
- **Contents:** 3 US health systems, 79 sites. Reports are split into Indication / Comparison / Findings / Impression (sections were pulled out of the original reports with GPT-4o). Splits are 140k / 10k / 10k, plus a private test set used by ReXrank.
- **Terms:** "non-commercial research and non-clinical purposes only", no redistribution.
- **Caveats:** PNGs are downsampled to 25% of original size, and the download is ~156 GB.
- **Paper:** arXiv [2505.00228](https://arxiv.org/abs/2505.00228).

**3. CheXpert Plus** – [AIMI page](https://aimi.stanford.edu/datasets/chexpert-plus), [paper](https://arxiv.org/pdf/2405.19538)
- **Contents:** Stanford reports split into up to 11 sections, plus demographics, CheXbert labels and RadGraph annotations.
- **Terms:** non-commercial, no redistribution. I didn't read the exact agreement text.
- **Paper using it:** a small multimodal findings-generation model trained on 697k image-text pairs ([Nat Commun 2025](https://doi.org/10.1038/s41467-025-58344-x)).

**4. IU X-ray** – https://openi.nlm.nih.gov/faq
- **Contents:** XML reports with Findings and Impression sections.
- **Caveats:** small and heavily de-identified ("XXXX" tokens). NoDerivatives licence.
- **Use:** the standard secondary benchmark. Use the official Open-i download, not the Kaggle or HF mirrors.

**5. Naija-CXR** – https://zenodo.org/records/21781842
- **Contents:** "frontal chest X-ray images paired with expert radiologist annotations and diagnostic reports", released Aug 2026.
- **Not checked:** report length, language and study count. Look inside the zip first.
- **Use:** good as an out-of-distribution test set. Treat it as non-commercial.

**6. CASIA-CXR (French)** – https://www.casia-cxr.net/
- **Contents:** original French reports from several hospitals, covering only 5 findings.
- **Steps:** download the ~80 MB sample to inspect, then submit the full-dataset request form and sign the DUA by hand.
- **Key restriction:** "You may not translate the radiographic reports… without prior written permission." That rules out translate-to-English experiments unless the authors agree.

**7–8. PadChest / PadChest-GR (Spanish)** – https://bimcv.cipf.es/bimcv-projects/padchest/ and https://bimcv.cipf.es/bimcv-projects/padchest-gr/
- **PadChest:** the largest non-English set. The report excerpts are heavily preprocessed (stop-words and affixes removed), so they are poor targets for fluent text generation.
- **PadChest-GR:** has sentence-level grounded reports in Spanish and English, with bounding boxes. This makes it the better choice for your secondary experiment. The English text is translated from the Spanish originals. Paper: [NEJM AI 2025](https://doi.org/10.1056/aidbp2401120).
- **Access:** both need an access request, and you agree not to share the data or try to re-identify anyone. The BIMCV site returned HTTP 503 today, so these terms come from the papers and the authors' GitHub.

## Known, not confirmed
- **BIMCV-COVID19+ (Spanish):** from memory, it includes Spanish radiology reports alongside CXR/CT. I couldn't check because the BIMCV site was down.
- **CANDID (the larger New Zealand set, 22k reports):** it is probably under the same restriction that closed CANDID-PTX, but I didn't check.

## Not recommended, and why
- **MIMIC-CXR-JPG:** images and labels only. The reports are in MIMIC-CXR.
- **BRAX (Brazil):** the page says "Free-text reports are not yet provided in the current version."
- **CANDID-PTX:** has English reports, but since Feb 2024 it isn't available outside Health New Zealand ([DigitalNZ](https://digitalnz.org/records/45567577)).
- **CheXpert (original), NIH ChestX-ray14, VinDr-CXR:** labels or boxes only, no reports.
- **FMCEB-CXR (Nigeria):** a 42 KB file of labels only, no images or report text.

## What I could not find
- No public CXR + report set in German, Japanese, Korean or Chinese. Chinese sets such as CX-CHR appear to be private.
- [PARROT](https://github.com/mk-runner/Awesome-Radiology-Report-Generation) is multilingual, but I believe it is reports without images; I didn't check.

## Next step
Apply for MIMIC-CXR credentials and the PadChest-GR request today, since both take time. Meanwhile, download ReXGradient-160K and IU X-ray and build your pipeline on them.

I've also made an interactive version of the shortlist with filters and an export of the access steps: `/private/tmp/e-za8iiV/home/cwd/dataset-shortlist.html`

Sources: [PadChest-GR arXiv](https://arxiv.org/html/2411.05085), [CASIA-CXR paper](https://www.sciencedirect.com/science/article/abs/pii/S0925231224012499), [CASIA-CXR downloads](https://casia-cxr.net/downloads.html), [Awesome-RRG list](https://github.com/mk-runner/Awesome-Radiology-Report-Generation), [ReXGradient paper](https://arxiv.org/abs/2505.00228), [CANDID-PTX Figshare](https://auckland.figshare.com/articles/dataset/CANDID-PTX/14173982), [CANDID-PTX RSNA](https://pubs.rsna.org/doi/10.1148/ryai.2021210136), [CheXpert Plus arXiv](https://arxiv.org/pdf/2405.19538), [CheXpert Plus AIMI](https://aimi.stanford.edu/datasets/chexpert-plus), [PadChest arXiv](https://arxiv.org/abs/1901.07441), [PadChest GitHub](https://github.com/auriml/Rx-thorax-automatic-captioning), [Open-i FAQ](https://openi.nlm.nih.gov/faq), [RRG review](https://arxiv.org/pdf/2405.10842)