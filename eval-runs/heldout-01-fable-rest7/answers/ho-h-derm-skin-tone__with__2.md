Five public datasets meet your criteria to a useful degree; three fit well (Fitzpatrick17k, DDI, PASSION) and two fit partly (SCIN, DermaCon-IN). None is both large and biopsy-confirmed in types V and VI, so plan on combining two or three.

## What I assumed you need
- **R1 (must):** a Fitzpatrick or Monk label for every image or patient.
- **R2 (must):** a diagnosis for every image.
- **R3 (must):** types V and VI in the hundreds, not a handful.
- **R4 (nice to have):** obtainable by an outside researcher, sooner is better. I assumed non-commercial research use is acceptable, since nearly all of these forbid commercial use.

## Shortlist

| # | Dataset | Access | Licence | Size | Dark-skin representation | Fit | Checked |
|---|---|---|---|---|---|---|---|
| 1 | Fitzpatrick17k | Labels download directly; images via source links or a form to the maintainers | CC BY-NC-SA 3.0 | 16,577 clinical images, 114 conditions | V: 1,533; VI: 635 | Strong | Today (I counted the label file) |
| 2 | DDI (Stanford) | Free registration plus research-use agreement | Stanford agreement, non-commercial | 656 images, 570 patients, biopsy-proven | V–VI: 207 | Strong | Today (counts from the paper) |
| 3 | PASSION | Request form, owner approval, probably days | PASSION licence, non-commercial | 4,901 images, 1,653 patients | Test split of 986: V: 341; VI: 88 | Strong | Today |
| 4 | SCIN (Google) | Direct download | Custom SCIN Data Use License | 10,408 images, 5,033 cases | Dermatologist-estimated V: 359; VI: 69 | Partial | Today (I counted the label files) |
| 5 | DermaCon-IN | Listed as open on Harvard Dataverse; the paper mentions a verification step | CC BY-NC-SA 4.0 | 5,450 images, 3,002 patients, 245 diagnoses | IV and V most common; VI: 136 | Partial | Partly; page not readable today |

## Details

**1. [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k)**
- **Contents:** clinical photos from two online atlases, each with a Fitzpatrick label; 565 images are unlabelled.
- **Why it fits:** it is the only set with V and VI in the high hundreds each, reported separately.
- **Weaknesses:** skin type was judged from the photo by crowd annotators, diagnoses are atlas labels and not biopsy-confirmed, and label noise and duplicates are known. [CleanPatrick](https://huggingface.co/datasets/Digital-Dermatology/CleanPatrick) provides cleaning annotations.
- **Access:** download `fitzpatrick17k.csv`, then fetch images from its `url` column (some links are dead) or use the form in the README to ask for the full image set.
- **Used in:** [Groh et al. 2021](https://doi.org/10.1109/cvprw53098.2021.00201) and [FairDisCo 2023](https://doi.org/10.1007/978-3-031-25069-9_13).

**2. [DDI, Diverse Dermatology Images](https://ddi-dataset.github.io/)**
- **Contents:** pathology-confirmed lesions; the V–VI images (159 benign, 48 malignant) are matched to I–II images on diagnosis category, age, gender and date.
- **Why it fits:** it was designed for exactly this audit, and it has the best ground truth.
- **Weaknesses:** it is small. From memory, skin tone is recorded as pairs (I–II, III–IV, V–VI), so V and VI cannot be separated.
- **Access:** register individually and accept the agreement ("personal, non-commercial research purposes only"). A copy is also listed on [Stanford Redivis](https://stanford.redivis.com/datasets/3r16-5mby7gfer).
- **Used in:** [Daneshjou et al. 2022](https://doi.org/10.1126/sciadv.abq6147).

**3. [PASSION](https://passionderm.github.io/)**
- **Contents:** paediatric teledermatology photos from Madagascar, Guinea, Malawi and Tanzania, covering eczema, fungal infections, scabies and other conditions, plus an impetigo flag.
- **Why it fits:** it is the only set collected in sub-Saharan Africa, with about 43% V–VI in the test split.
- **Weaknesses:** there are no type I–II images, so it gives no light-versus-dark contrast by itself. It has no skin cancer, and the paper does not publish full-set counts per type.
- **Access:** fill in the Google Form on the project page; the download link may not be shared.
- **Used in:** [Gottfrois et al. 2024](https://doi.org/10.1007/978-3-031-72384-1_66).

**4. [SCIN](https://github.com/google-research-datasets/scin)**
- **Contents:** crowdsourced phone photos from US internet users, with self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick and Monk scale from two rater pools.
- **Why it fits:** it is the only open set with Monk labels and both self-reported and estimated tone.
- **Weaknesses:**
  - Tone labels are incomplete: the dermatologist estimate is missing for 731 cases and self-report is missing or unassigned for 2,858.
  - Dark tones are thin: self-report gives V: 214 and VI: 143, and only 207 cases are Monk 7–10 by the US raters.
  - Diagnoses are differential lists made from the photos, and only 3,049 cases were judged gradable.
- **Access:** follow `scin_demo.ipynb`, or fetch the files from the public bucket `dx-scin-public-data`. I did not read the licence's commercial-use terms.
- **Used in:** [one classification paper](https://doi.org/10.5267/j.ijdns.2024.11.003).

**5. [DermaCon-IN](https://doi.org/10.7910/DVN/W7OUZM)**
- **Contents:** outpatient clinical photos from South India with a diagnosis hierarchy, each labelled on both the Fitzpatrick and Monk scales by trained raters.
- **Why it fits:** it has complete dual-scale labels and many type IV–V images.
- **Weaknesses:** type VI is 136 images, the exact type V count is not in the paper text, and there are few I–II images.
- **Access:** open the Dataverse record in a browser. The registry lists it as open, but the paper says access "will be granted following a background verification process".
- **Paper:** [arXiv 2506.06099](https://arxiv.org/abs/2506.06099).

## Known, not confirmed
- **[DDI-2](https://doi.org/10.57761/pgwn-6b62):** Stanford's follow-up set of self-identified Asian patients. The record exists, but I could not read its contents or terms because the page renders by JavaScript. It is unlikely to add many V–VI images.
- **[Black skin lesions set, University of Campinas](https://zenodo.org/records/10570316):** acral lesions (palms, soles, nails) on Black skin, CC BY-NC-SA 4.0. Files are restricted behind a request from an institutional email. Whether each image carries a skin tone label, and how many images there are, is not stated.

## Not recommended, and why
- **[MILK10k](https://doi.org/10.7910/dvn/fsxraq):** has a six-level skin tone label per lesion, but the darkest levels are reportedly under 1% of 5,240 lesions (unofficial source, I did not count it).
- **[MRA-MIDAS](https://aimi.stanford.edu/datasets/mra-midas-Multimodal-Image-Dataset-for-AI-based-Skin-Cancer):** Fitzpatrick per patient and biopsy-proven, but only 16.8% of patients are types III–VI combined.
- **[PAD-UFES-20](https://doi.org/10.17632/zr7vgbcyr2.1):** open with a Fitzpatrick field, but from memory it is filled for only part of the images and V–VI are a handful.
- **[MSKCC Skin Tone Labeling Dataset](https://api.isic-archive.com/collections/413/):** 4,879 dermoscopic images balanced across all six types with Monk and colorimeter readings, but every lesion is assumed benign. It is usable only for a false-positive check.
- **HAM10000, BCN20000, ISIC challenge sets, Derm7pt:** no skin tone labels (from memory).
- **[electricsheepafrica/Africa-skin-cancer-images-EHR](https://huggingface.co/datasets/electricsheepafrica/Africa-skin-cancer-images-EHR):** appears to attach African metadata to existing HAM10000/ISIC image IDs, so it is probably synthetic.

## What I could not find
- A public dermoscopy dataset with hundreds of confirmed type V–VI malignant lesions; DDI's 48 malignant V–VI images are the best available.
- Monk-scale labels outside SCIN, DermaCon-IN and the benign-only MSKCC set.

I searched five registries, the literature and the web; Harvard Dataverse and medRxiv refused automated requests.

## Next step
Start today with Fitzpatrick17k for statistical power and SCIN for Monk labels, register for DDI as the biopsy-confirmed check, and send the PASSION request now since it needs approval. Because the diagnosis mix differs by skin type in all of these, compare within condition.

All facts were checked on 2026-11-12 unless marked as from memory. The interactive shortlist is at `/private/tmp/e-yIBc9C/home/cwd/dataset-shortlist.html`.