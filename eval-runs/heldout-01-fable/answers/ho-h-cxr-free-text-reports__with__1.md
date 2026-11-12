Four English datasets and four non-English ones release the report text itself. Two of the English ones (ReXGradient-160K and IU X-Ray) you can download today, and MIMIC-CXR is the only one that needs a multi-day credentialing process. Everything below was checked on 11 November 2026 (UTC) unless marked "from memory".

## What I assumed you need
- **R1 (must):** the radiologist's free-text report is released, not only labels derived from it.
- **R2 (must):** chest radiographs are linked to the report at image or study level.
- **R3 (nice):** large enough to train, or at least evaluate, a generation model.
- **R4 (nice):** English; non-English is fine for the secondary experiment.
- **R5 (nice):** obtainable quickly.
- I assumed academic, non-commercial use; almost every licence below forbids commercial use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | MIMIC-CXR | Application: credentialing, training and signed agreement; days to ~2 weeks | PhysioNet Credentialed Health Data License 1.5.0 | 227,835 studies, 377,110 images | Strong, English | today (steps partly from memory) |
| 2 | CheXpert Plus | Account and research use agreement on Stanford's Redivis; probably same day | Stanford research use agreement, non-commercial | 187,711 studies, 223,462 pairs | Strong, English | today (approval mechanics not confirmed) |
| 3 | ReXGradient-160K | Hugging Face login, accept terms, automatic; minutes | Harvard non-commercial agreement | 160,000 studies, 273,004 images | Strong, English | today |
| 4 | IU X-Ray (Open-i) | Direct download, no login; minutes | CC BY-NC-ND 4.0 per secondary sources | ~4,000 reports, ~8,000 images | Strong but small, English | links today; licence not confirmed |
| 5 | CASIA-CXR | Request form and hand-signed agreement; weeks. Sample open now | Custom, academic only | 11,111 radiographs | Strong, French | today |
| 6 | PadChest-GR | Request form under research use agreement; days | PadChest research use agreement | 4,555 studies | Partial, Spanish and English sentences | today |
| 7 | BIMCV-COVID19+ | Request form, or IEEE DataPort login; days | BIMCV research use agreement | 21,342 CR and 34,829 DX studies | Partial, Spanish | today (report format from memory) |
| 8 | PadChest | Request form; days. 167 MB sample open | PadChest research use agreement | 160,000+ images | Partial, Spanish, stemmed text | today |
| 9 | REFLACX | PhysioNet login and agreement; images need MIMIC-CXR | PhysioNet Restricted Health Data License | ~3,000 reports (from memory) | Partial, English | today |

## Details

**1. [MIMIC-CXR](https://physionet.org/content/mimic-cxr/2.1.0/)** (v2.1.0)
- **Contents:** one free-text report per study, "stored in individual text files named using the anonymous study identifier", plus the DICOM images (5.1 TB).
- **Steps:**
  1. Create a PhysioNet account.
  2. Apply for credentialed access; from memory, this asks for a reference such as a supervisor.
  3. Complete the required training, "CITI Data or Specimens Only Research" (a few hours, from memory).
  4. Sign the Credentialed Health Data Use Agreement 1.5.0 on the project page.
  5. For JPG images, sign the same agreement on [MIMIC-CXR-JPG](https://physionet.org/content/mimic-cxr-jpg/2.1.0/) (612 GB).
- **Conditions:**
  - Access is personal, so each team member applies separately and the data cannot be shared.
  - The agreement requires that "any publication which makes use of the data will also make the relevant code available".
  - PhysioNet [forbids sending the data to online AI services](https://physionet.org/news/post/llm-responsible-use/) unless zero retention is verified, which matters if you plan LLM-based preprocessing or evaluation.
- **Used in:** [the data descriptor](https://doi.org/10.1038/s41597-019-0322-0) and [a warm-starting report generation baseline](https://doi.org/10.1016/j.artmed.2023.102633).

**2. [CheXpert Plus](https://aimi.stanford.edu/datasets/chexpert-plus)**
- **Contents:** "223,462 unique pairs of radiology reports and chest X-rays" from 64,725 Stanford patients, with reports split into 11 sections and images in DICOM. The Redivis record is 6.76 TB.
- **Steps:** follow "Download here" to [Stanford's Redivis page](https://doi.org/10.57761/fzna-pm76), sign in, and accept the Stanford University Dataset Research Use Agreement. I could not confirm whether approval is automatic.
- **Licence:** research only, no commercial use, no redistribution, and each colleague registers individually (from the [AIMI portal listing](https://stanfordaimi.azurewebsites.net/datasets/5158c524-d3ab-4e02-96e9-6ee9efc110a1) and the paper).
- **Caveat (from memory):** many reports have only an Impression section, with Findings present for a minority. Check section coverage before fixing your target text.
- **Used in:** [a small multimodal radiology model](https://doi.org/10.1038/s41467-025-58344-x) and [a dual-stage report generation framework](https://doi.org/10.1609/aaai.v40i40.40688).

**3. [ReXGradient-160K](https://huggingface.co/datasets/rajpurkarlab/ReXGradient-160K)**
- **Contents:** studies from "109,487 unique patients across 3 U.S. health systems (79 medical sites)", each report with Indication, Comparison, Findings and Impression. Splits are 140,000 train, 10,000 validation and 10,000 public test.
- **Steps:** log in to Hugging Face and accept the agreement on the dataset page; access is granted automatically. The download is 156 GB.
- **Conditions:**
  - Non-commercial research only, with no third-party sharing.
  - You may download only the portion your project needs.
  - Images are PNGs downsampled to 25% of original dimensions.
- **Caveat:** the card does not state the language; I assumed English from the US sites. It was released in 2025, so there are few published baselines.

**4. [IU X-Ray / Open-i](https://openi.nlm.nih.gov/faq)**
- **Contents:** XML reports with findings and impression; a paper found today counts 3,996 reports and 8,121 images.
- **Steps:** download [the reports archive](https://openi.nlm.nih.gov/imgs/collections/NLMCXR_reports.tgz) (1.1 MB) and [the PNG archive](https://openi.nlm.nih.gov/imgs/collections/NLMCXR_png.tgz) (1.36 GB). Both links answered today without a login.
- **Licence:** secondary sources report CC BY-NC-ND 4.0, but the official FAQ could not be read automatically, so confirm it in a browser.
- **Caveat:** de-identification replaced many words with "XXXX". It is too small to train on alone and best used as a second benchmark.

**5. [CASIA-CXR](https://www.casia-cxr.net/)** (French)
- **Contents:** "narrative reports originally written in French" with Indication, Comparison, Findings and Impression fields; 11,111 radiographs per the [dataset paper](https://doi.org/10.1016/j.neucom.2024.128478).
- **Steps:** download the ~80 MB sample from the [downloads page](https://casia-cxr.net/downloads.html), fill in the request form, then hand-sign the data use agreement. Turnaround is not stated.
- **Conditions:** academic researchers only and no redistribution. Also, "You may not translate the radiographic reports… to any other languages without prior written permission", which rules out translating to English for a pooled experiment unless you ask.
- **Caveat:** cases were sampled from five disease categories, so the mix is not a natural hospital distribution.

**6. [PadChest-GR](https://bimcv.cipf.es/bimcv-projects/padchest-gr/)** (Spanish and English)
- **Contents:** 4,555 studies with complete lists of positive and negative finding sentences in both languages, plus bounding boxes (46 GB).
- **Fit:** the sentences were extracted from the Spanish reports and translated with GPT-4, so this is not the verbatim report. It works well as a bilingual evaluation set.
- **Steps:** read the [research use agreement](https://bimcv.cipf.es/bimcv-projects/padchest/padchest-dataset-research-use-agreement/), then submit the request form on the project page.
- **Used in:** [the NEJM AI dataset paper](https://doi.org/10.1056/aidbp2401120).

**7. [BIMCV-COVID19+](https://bimcv.cipf.es/bimcv-projects/bimcv-covid19/)** (Spanish)
- **Contents:** the page says the data include "informes radiográficos". That they are verbatim free text is from memory, so check the data descriptor first.
- **Steps:** submit the request form for the release you want, or log in to [IEEE DataPort](https://doi.org/10.21227/w3aw-rv39). The two pages describe access differently; the BIMCV page is the owner's.
- **Caveat:** COVID-positive patients only, CT studies are mixed in, and the archives run to hundreds of GB.

**8. [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/)** (Spanish)
- **Fit:** the report field is "preprocessed, words are stemmed and tokenized" (for example "compar con estudi previ 2010 sin identific cambi signific"), per the [authors' repository](https://github.com/auriml/Rx-thorax-automatic-captioning). That makes it a poor target for readable report generation.
- **Steps:** same request form and agreement as PadChest-GR; the full set is 1.02 TB. Inspect the 167 MB sample first.

**9. [REFLACX](https://physionet.org/content/reflacx-xray-localization/1.0.0/)**
- **Contents:** reports that radiologists dictated afresh for MIMIC-CXR frontal images while eye-tracked. It is useful as a second reference report, not as training data.
- **Steps:** the reports need only a PhysioNet login and a signed agreement, but the images come from MIMIC-CXR, which needs credentialing.

## Known, not confirmed
- **[CANDID-PTX](https://doi.org/10.17608/k6.auckland.14173982.v2)** (New Zealand, English): 19,237 radiographs with anonymised free-text reports, per the [RSNA paper](https://pubs.rsna.org/doi/full/10.1148/ryai.2021210136).
  - The original route was an online ethics course plus a signed agreement emailed to the author.
  - One catalogue copy of the description says external users can no longer obtain it after New Zealand's 2024 data governance changes.
  - Figshare blocked automated reading, so open the record in a browser before planning around it.
- **[Naija-CXR](https://zenodo.org/records/21781842)** (Nigeria): an open 389 MB download listing "Free radiologist reports", but it gives no image or report counts and I did not inspect the contents. The record says CC BY 4.0 while the description says non-commercial only.
- **[Interpret-CXR](https://huggingface.co/datasets/StanfordAIMI/interpret-cxr-test-public)** (RRG24 challenge): the public test set exists behind an automatic Hugging Face gate. From memory, the training pool combines CheXpert Plus, PadChest, BIMCV-COVID19 and IU X-Ray, and you add MIMIC-CXR yourself; I did not confirm this.

## Not recommended, and why
- **CheXpert (original), NIH ChestX-ray14, VinDr-CXR:** labels or boxes only, no reports (the last two from memory).
- **[BRAX](https://physionet.org/content/brax/1.1.0/):** labels "derived from free-text radiology reports written in Brazilian Portuguese"; the reports are not released.
- **[CRADI](https://doi.org/10.5281/zenodo.5493595):** Chinese hospitals, labels extracted from reports, no report text.
- **[FMCEB-CXR](https://zenodo.org/records/20750284):** describes 5,517 Nigerian reports, but the record is a single 42 KB file of extracted labels with no images.
- **Open re-uploads of MIMIC-CXR or CheXpert Plus on Hugging Face:** a copy does not change the original terms, so use the official sources.

## What I could not find
- No public chest X-ray set with original reports in Chinese, Japanese, German, Korean, Portuguese or Vietnamese. Reviews list CX-CHR and CH-Xray (Chinese) as private.
- I searched DataCite, Hugging Face, OpenAIRE, PhysioNet, Zenodo, Europe PMC and the web. OpenAlex was unavailable and Hugging Face rate-limited one lookup, so coverage may be slightly incomplete.

## Next step
Accept the ReXGradient-160K terms and download IU X-Ray today, and start PhysioNet credentialing for MIMIC-CXR and the CheXpert Plus registration in parallel. For the secondary experiment, send the CASIA-CXR request now, since it depends on the authors replying.

The interactive shortlist is at `/private/tmp/e-75lO4W/home/cwd/dataset-shortlist.html`.