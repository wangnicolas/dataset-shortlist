## What I assumed you need
- **R1:** a skin tone label (Fitzpatrick or Monk) on every image or patient.
- **R2:** a diagnosis label.
- **R3:** Fitzpatrick V and VI represented in the hundreds or more.
- **R4:** downloadable for research now.

I assumed non-commercial research use is fine and that biopsy-confirmed diagnoses would be ideal but not required.

**Short answer:** three public datasets meet these requirements, and none is perfect. No public dataset I found has both biopsy-proven diagnoses and thousands of expert-labelled V/VI images.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [DDI, Diverse Dermatology Images (Stanford)](https://ddi-dataset.github.io/) | Free registration and signed Research Use Agreement; minutes | Non-commercial, no redistribution | 656 images, about 207 of them V–VI | Strong | Access terms today; V–VI count from a secondary summary |
| 2 | [SCIN (Google)](https://github.com/google-research-datasets/scin) | Open download from a public cloud bucket; minutes | SCIN Data Use Public License | 10,000+ images, about 5,000 cases | Strong for Monk, partial for V/VI | Today |
| 3 | [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k) | CSV open; images fetched from source atlases; days | CC BY-NC-SA 3.0 | 16,577 images, about 2,170 V–VI | Partial | Licence today; counts from a secondary summary |

## Details
**DDI** is the best fit for a rigorous audit.
- Diagnoses are biopsy-proven, with 78 disease labels plus malignant/benign.
- Every image has a Fitzpatrick type, and it was built to compare I–II against V–VI, matched on diagnostic category, age, sex and photo date.
- About 207 images are V–VI (159 benign, 48 malignant). One study reports no basal cell carcinoma in V–VI.
- To get it, register on the Stanford AIMI portal and accept the agreement. Don't share the download link or redistribute any images.
- Subgroup sizes are small, so expect wide confidence intervals.

**SCIN** is the only one with Monk labels.
- It has Monk tone from graders in the US and India, self-reported Fitzpatrick, and dermatologist-estimated Fitzpatrick.
- Per the [SCIN paper](https://arxiv.org/html/2402.18545v1), V/VI make up about 16% of cases by self-report, but only 5.3% (V) and 0.6% (VI) by dermatologist estimate. Monk 8–10 is about 1–1.5%.
- Diagnoses are weighted dermatologist differentials, not biopsy, and some cases are "not diagnosable."
- Skin tone isn't always gradable, and many self-reports are blank (`NONE_SELECTED`). For a V/VI audit, use self-reported Fitzpatrick (about 800 cases) and treat dermatologist-estimated V/VI as a small sample.
- The licence forbids re-identifying contributors. I didn't read it fully, so check it for other limits.

**Fitzpatrick17k** is the only large set.
- It has 114 conditions, and its V+VI share is about 13%.
- Skin tone labels came from crowd annotators (Scale AI, Centaur Labs), not dermatologists, so tone labels are noisy. Diagnoses come from the source atlases and aren't biopsy-confirmed.
- It has duplicates and mislabels. Use the cleaned [Fitzpatrick17k-C](https://zenodo.org/records/11101338) (Zenodo, CC BY-NC 4.0) and its [data-quality paper](https://www.nature.com/articles/s41597-025-04382-5).

A suggested design is to run the main audit on DDI, because its labels are the most trustworthy. Then replicate on Fitzpatrick17k-C for statistical power and on SCIN for the Monk scale.

## Known, not confirmed
- **DDI-2:** 665 images of self-identified Asian patients from Stanford. I didn't check its skin type labels or V–VI counts.
- **SkinCAP:** 4,000 images drawn from Fitzpatrick17k and DDI, with captions. It adds nothing new for labels.

## Not recommended, and why
- **PAD-UFES-20:** has Fitzpatrick labels, but only 10 type V and 1 type VI images out of 1,494 labelled.
- **MRA-MIDAS (Stanford):** biopsy-proven and Fitzpatrick-labelled, but only 16.8% are III–VI and the authors flag few IV–VI.
- **Pipsqueak:** all V–VI, but only about 16 original images (80 after augmentation), mostly taken from Fitzpatrick17k.
- **Acral lesions in Black patients (Zenodo):** access is restricted and I found no Fitzpatrick label.
- **HAM10000 and the standard ISIC release:** from memory, no skin tone labels and almost no V–VI. I didn't check this today.

## What I could not find
No large, open set pairs expert skin tone labels with pathology diagnoses and has thousands of V/VI cases. A 2025 [atlas of digital dermatology](https://www.medrxiv.org/content/10.64898/2025.12.27.25342585v1.full) reports that V–VI are only about 5.8% of images across datasets. The registry search mostly returned noise. Most of what's above came from the literature and web search.

## Next step
Register for DDI first, since approval is quick. Then pull the SCIN CSVs and Fitzpatrick17k-C and count V/VI per diagnosis class, so you can see which classes are too small to audit.

