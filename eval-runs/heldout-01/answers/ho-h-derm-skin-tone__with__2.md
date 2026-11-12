Three public datasets fit: SCIN, Fitzpatrick17k and DDI. Each covers different gaps, and you could use all three. I checked them on 2026-11-12. Where I rely on memory instead, I say so.

I did not build the interactive shortlist page. This answer is the complete result.

## What I assumed you need
- **R1 (must):** Images of skin, either clinical photos or dermoscopy.
- **R2 (must):** A skin tone label per image or patient, as Fitzpatrick or Monk.
- **R3 (must):** A diagnosis label per image.
- **R4 (must):** Fitzpatrick V and VI present in numbers large enough to give a stable subgroup metric.
- **R5 (nice):** Biopsy-confirmed diagnoses, many conditions, and a download you can start today.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | SCIN (Google) | Open download, no application | SCIN Data Use License | 10,000+ images | R1–R3 met. Only dataset here with both Fitzpatrick and Monk. V/VI count not checked. | Landing page today. Details from memory. |
| 2 | Fitzpatrick17k | Open, but images come from the original source sites | CC BY-NC-SA 3.0 | ~16.5k images, 114 conditions (from memory) | R1–R4 met. Tone labels are crowd-annotated. | Landing page today. Counts from memory. |
| 3 | DDI, Stanford | Free registration plus a research-use agreement | Non-commercial research only | 656 images (from memory) | R1–R5 met, with the strongest labels. | Terms today. Counts from memory. |

## Details
**SCIN** (https://github.com/google-research-datasets/scin)
- **Contents:** The page says it has "10,000+ images of dermatology conditions, crowdsourced with informed consent from US internet users" and includes "estimated Fitzpatrick skin type and Monk Skin Tone."
- **Diagnosis:** The diagnosis is a dermatologist differential, so it is not biopsy-proven. The paper says 89% of assignable cases were allergic, infectious or inflammatory conditions, so melanoma and other cancers are thin.
- **Skin tone:** The tone labels are estimated by raters (eFST, eMST), not measured. Users also self-reported Fitzpatrick type, which I recall but did not confirm.
- **Access:** The page points to a demo notebook for loading it. From memory, the data sits in a Google Cloud Storage bucket. Read the SCIN Data Use License before use, because I did not read its terms.
- **Paper:** https://doi.org/10.1001/jamanetworkopen.2024.46615

**Fitzpatrick17k** (https://github.com/mattgroh/fitzpatrick17k)
- **Contents:** It is a CSV of Fitzpatrick annotations plus the training script.
- **Access:** The README says you download the images from their original source, given in the `url` column. Links may have rotted since release, so check how many still resolve.
- **Licence:** "Creative Commons Attribution-NonCommercial-ShareAlike 3.0."
- **Skin tone:** From memory, the tone labels came from crowd annotators, not clinicians. The published literature questions their reliability, including a Zenodo record titled "Investigating the Quality of DermaMNIST and Fitzpatrick17k Dermatological Image Datasets" (https://zenodo.org/records/12739457). I have not read it.
- **Paper using it for a similar purpose:** https://doi.org/10.1038/s41591-023-02728-3

**DDI, Diverse Dermatology Images** (https://ddi-dataset.github.io/)
- **Contents:** Pathology-confirmed images. The page says it was designed to compare "FST I-II and FST V-VI by matching diagnostic category, age within 10 years, gender, and date of photograph within 3 years." That makes it a good fit for a fairness audit.
- **Counts:** From memory, there are 656 images and roughly 200 each in the I–II, III–IV and V–VI groups. I did not confirm this.
- **Access:** Register on the Stanford AIMI portal and accept the Research Use Agreement. The agreement says "personal, non-commercial research purposes only" and forbids redistribution and sharing the download link. Each person in your organization must register individually.
- **Paper:** https://doi.org/10.1126/sciadv.abq6147. It reports that AI models do worse on dark skin tones and uncommon diseases.

## Known, not confirmed
- **"Assessing the Generalizability of Deep Neural Networks-Based Models for Black Skin Lesions"** (https://zenodo.org/records/10570316).
  - **Access:** The record page says "files are restricted" and you must fill in a request form. The licence is CC BY-NC-SA 4.0.
  - **Contents:** I did not open it, so I don't know its skin tone labels or diagnosis classes. From the title, it is probably dark-skin only, which would make it unsuitable for comparing across tones.

## Not recommended, and why
- **PAD-UFES-20** (https://data.mendeley.com/datasets/zr7vgbcyr2/1) is open under CC BY-4.0 and has smartphone images with Fitzpatrick types. From memory, it is mostly Brazilian patients with Fitzpatrick I–III, so V/VI is too sparse. It could serve as a light-skin baseline.
- **HAM10000 and similar dermoscopy sets** are the usual benchmarks, but from memory they carry no per-image tone labels and have almost no V/VI.
- **The SCGAN skin-tone-balanced HAM10000 extension** (https://doi.org/10.1371/journal.pone.0331081) is synthetic. It would test the generator, not real-world performance.

## What I could not find
- No dermoscopy dataset with Fitzpatrick or Monk labels and substantial V/VI. All three picks are clinical photos.
- I did not count the V/VI images in SCIN or Fitzpatrick17k from the files. Do that first.
- I searched five registries, the literature and the web. Dataset hosting sites that block automated clients may hide other candidates.

## Next step
1. Download SCIN today, since it needs no application.
2. Tabulate V/VI counts per diagnosis in SCIN and Fitzpatrick17k, and decide which conditions have enough images per tone.
3. Register for DDI. Use it as the cleanest held-out test set, and use Fitzpatrick17k and SCIN for broader coverage.

I don't know of any dataset that pairs the pathology-confirmed labels of DDI with the volume of the other two. For a headline fairness claim, report results per dataset instead of pooling them, because the label quality differs.