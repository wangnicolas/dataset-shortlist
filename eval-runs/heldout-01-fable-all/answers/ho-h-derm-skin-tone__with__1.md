Five public datasets have both a skin tone label and a diagnosis with real numbers in types V and VI; none is ideal alone, so a credible audit will combine two or three. All facts below were checked on 2026-11-12, and the V/VI counts marked "counted" are ones I tallied from each dataset's own metadata file.

## What I assumed you need
- **R1 (must):** a Fitzpatrick or Monk label per image or patient.
- **R2 (must):** a diagnosis per image or patient.
- **R3 (must):** types V and VI in the hundreds.
- **R4 (nice to have, my assumption):** lighter types in the same dataset, so the comparison isn't confounded by different sources.
- **R5:** clinical photos or dermoscopy, any condition.

## Shortlist
| # | Dataset | Access | Licence | Size | V / VI | Fit | Checked |
|---|---|---|---|---|---|---|---|
| 1 | Fitzpatrick17k | Labels: direct download. Images: fetch by URL, or request form | CC BY-NC-SA 3.0 | 16,577 images, 114 conditions | 1,533 / 635 (counted) | Strong | today |
| 2 | DermaCon-IN | Direct download | CC BY-NC-SA 4.0 | 5,450 images, 3,002 patients, 245 conditions | 1,285 / 136 (counted) | Strong, but no types I–II | today |
| 3 | SCIN | Direct download | Custom SCIN Data Use License | 5,033 cases, 10,000+ images | 229 / 27 among 3,061 cases with a diagnosis (counted) | Partial | today |
| 4 | DDI | Free registration and research use agreement | Stanford agreement, non-commercial | 656 images, 570 patients | 207 in V–VI combined | Partial (small) | today |
| 5 | PASSION | Request form, likely days | Custom, non-commercial | 4,901 images, 1,653 patients | 341 / 88 in the 986-image test split | Partial | today |
| 6 | MILK10k | Direct download | CC BY-NC 4.0 | 5,240 lesions, 10,480 images | 111 lesions in its two darkest classes (counted) | Weak | today |

## Details

**1. [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k)**
- **Contents:** clinical photos from two online atlases, with all six types (I 2,947; II 4,808; III 3,308; IV 2,781; V 1,533; VI 635; 565 unlabelled).
- **Why it fits:** it has the largest V–VI count and light types in the same set.
- **Weakness:** diagnoses are atlas captions and skin types come from non-dermatologist annotators; duplicates and mislabels are documented. Evaluate on a cleaned version such as [CleanPatrick](https://huggingface.co/datasets/Digital-Dermatology/CleanPatrick).
- **Access:** the label CSV is in the repo; images come from the URLs in the CSV (some are dead) or via the authors' form.
- **Used by:** [Groh et al. 2021](https://doi.org/10.1109/cvprw53098.2021.00201), [FairDisCo 2023](https://doi.org/10.1007/978-3-031-25069-9_13), [quality audit 2025](https://doi.org/10.1038/s41597-025-04382-5).

**2. [DermaCon-IN](https://doi.org/10.7910/DVN/W7OUZM)**
- **Contents:** outpatient photos from South India with dermatologist diagnoses, plus Fitzpatrick and Monk labels on every image.
- **Counts:** Fitzpatrick III 1,403; IV 2,620; V 1,285; VI 136. Monk 7–9 covers 2,059 images. The V–VI images come from 993 patients.
- **Weakness:** there are no type I–II images, and only 52 images are neoplasms; most are infectious or inflammatory.
- **Access:** download two zips (about 3.6 GB) and the metadata table from Harvard Dataverse.
- **Used by:** [describing paper](https://doi.org/10.52202/085713-3742).

**3. [SCIN](https://github.com/google-research-datasets/scin)**
- **Contents:** crowdsourced US smartphone photos with three tone labels per case: self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick and Monk.
- **Counts:** over all cases, the dermatologist estimate gives V 359 and VI 69. Only 3,061 cases have a condition label, which cuts this to 229 and 27.
- **Weakness:** the diagnosis is a weighted differential from photos, not a confirmed one. Self-reported and estimated type VI disagree (143 vs 69).
- **Access:** public Google Cloud bucket `dx-scin-public-data`. I did not confirm the licence's commercial-use terms.

**4. [DDI](https://ddi-dataset.github.io/)**
- **Contents:** pathology-confirmed lesions from Stanford, with 208 type I–II images matched to 207 type V–VI on diagnosis category, age, sex and date.
- **Why it fits:** it has the best label quality here and is built for exactly this audit.
- **Weakness:** it is small, and tone is given in three bins, so V and VI are not separable.
- **Access:** register individually on the Stanford AIMI portal and accept the agreement. No redistribution or sharing the link, and each team member registers separately.
- **Used by:** [Daneshjou et al. 2022](https://doi.org/10.1126/sciadv.abq6147).

**5. [PASSION](https://passionderm.github.io/)**
- **Contents:** mostly paediatric teledermatology photos from Madagascar, Guinea, Malawi and Tanzania, Fitzpatrick III–VI only.
- **Labels:** eczema, fungal, scabies, other, plus an impetigo flag.
- **Weakness:** there are no light types, and whole-dataset tone counts are not published; I only found the test split in the [paper](https://arxiv.org/abs/2411.04584).
- **Access:** Google Form request; approval time is not stated. Non-commercial, no reposting.

**6. [MILK10k](https://doi.org/10.7910/dvn/fsxraq)**
- **Contents:** paired clinical and dermoscopic images, 95.7% biopsy-confirmed. It is the only dermoscopy option with a tone label.
- **Weakness:** the tone scale is its own (0 very dark to 5 very light, deliberately not Fitzpatrick), and classes 0–1 hold only 6 and 105 lesions.

## Known, not confirmed
- **[DDI-2](https://doi.org/10.57761/pgwn-6b62):** the DOI resolves to Stanford Redivis; it covers self-identified Asian patients. I could not read the page or the paper, so tone labels and access terms are unconfirmed.
- **[Black skin lesions, UNICAMP](https://zenodo.org/records/10570316):** acral lesions assessed on the Fitzpatrick scale, CC BY-NC-SA 4.0. Files are restricted and need a request from an institutional email; size and V/VI counts are unconfirmed.
- **[MSKCC Skin Tone Labeling Dataset](https://doi.org/10.34970/962049):** CC BY 4.0, with Monk, Pantone and colorimeter tone measurements. I did not confirm whether diagnoses are included or how many dark-skin cases it has.

## Not recommended, and why
- **[PAD-UFES-20](https://doi.org/10.17632/zr7vgbcyr2.1):** has a Fitzpatrick column but only about 10 type V and 1 type VI images (from a [secondary source](https://pmc.ncbi.nlm.nih.gov/articles/PMC13459198/), not counted by me).
- **[MRA-MIDAS](https://doi.org/10.71718/15nz-jv40):** Fitzpatrick is recorded, but only 16.8% of patients are types III–VI combined.
- **HAM10000, ISIC challenge sets, Derm7pt, DermNet:** no skin tone label (from memory, not rechecked).
- **SkinCon, SkinCAP, FitzDerm-CF:** extra annotations on Fitzpatrick17k and DDI images, not new patients.
- **[Synthetic dermatology dataset on Mendeley](https://doi.org/10.17632/bb844rcjx5.1):** synthetic images are not audit evidence.

## What I could not find
- A dermoscopy dataset with Fitzpatrick labels and hundreds of V–VI lesions.
- A single dataset with confirmed diagnoses, all six types and more than about 200 V–VI images.
- Search coverage has small holes: Zenodo rate-limited one of six queries, and Stanford Redivis pages were unreadable.

## Next step
Start today with Fitzpatrick17k (cleaned) and SCIN for six-type comparisons, and register for DDI as the high-quality check. Add DermaCon-IN for volume in type V, and send the PASSION request now if your classifier covers common inflammatory and infectious conditions. Type VI is the thin spot everywhere (635, 136, 27, 88), so report V and VI separately where the data allows.

The interactive shortlist is at `/private/tmp/e-2tfNLK/home/cwd/dataset-shortlist.html`.