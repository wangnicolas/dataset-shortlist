Four public datasets meet all three of your requirements: a per-image skin tone label, a diagnosis, and hundreds of FST V–VI images. They are **Fitzpatrick17k, DermaCon-IN, PASSION and DDI**. SCIN has a lot of FST V but very little FST VI. Everything below was checked on 2026-11-12. I counted the skin tone figures for Fitzpatrick17k, SCIN and DermaCon-IN myself from their released metadata files.

## What I assumed you need
- **Must:** a Fitzpatrick or Monk label for every image or patient.
- **Must:** a diagnosis label.
- **Must:** hundreds of FST V–VI images, not a handful.
- **Nice to have:** obtainable by a single researcher without an institutional contract.
- I assumed non-commercial research use. Almost every dataset here is non-commercial only; SCIN is the exception.

## Shortlist
| # | Dataset | Access | Licence | Size | FST V / VI | Checked |
|---|---|---|---|---|---|---|
| 1 | Fitzpatrick17k | Open CSV; images from links or an author form | CC BY-NC-SA 3.0 | 16,577 images, 114 conditions | **1,533 / 635** | today |
| 2 | DermaCon-IN | Open download, Harvard Dataverse | CC BY-NC-SA 4.0 | 5,450 images, 3,002 patients, 245 diagnoses | **1,285 / 136** | today |
| 3 | PASSION | Request form, probably days | PASSION licence, non-commercial | 4,901 images, 1,653 patients | test split alone: **341 / 88** | today |
| 4 | DDI | Free registration + click-through agreement, minutes | Stanford research use, non-commercial | 656 images, 570 patients | **207** (V and VI combined) | today |
| 5 | SCIN | Open download | SCIN Data Use License (commercial use allowed) | 5,033 cases, 10,407 images | dermatologist-estimated, labelled cases: 229 / **27** | today |
| 6 | DDI-2 | Stanford Redivis, terms not read | ? | 665 images, Asian patients | not checked | partly |

## Details
**1. [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k)** — clinical photos from two dermatology atlases.
- The CSV has a `fitzpatrick_scale` column: 565 images are unknown (-1).
- Distribution: I 2,947, II 4,808, III 3,308, IV 2,781, V 1,533, VI 635.
- A second set of skin tone labels (`fitzpatrick_centaur`) lets you test how sensitive your results are to the labelling.
- **Caveats:**
  - The skin tone labels come from crowd annotators, not dermatologists.
  - Diagnoses are the atlas captions, not biopsy results.
  - Some image links are dead; the README has a form for a full image link.
- Papers: [Groh 2021](https://doi.org/10.1109/cvprw53098.2021.00201) (accuracy by skin type) and [Groh 2022](https://doi.org/10.1145/3555634) (how reliable the skin tone labels are).

**2. [DermaCon-IN](https://doi.org/10.7910/DVN/W7OUZM)** — dermatologist-annotated clinical photos from South India, 2025.
- Every image has both FST and Monk. FST: III 1,403, IV 2,620, V 1,285, VI 136. Monk 8–9: 375 images.
- No files on Dataverse are restricted, and I downloaded the metadata table without logging in. The paper mentions a background check before access, which contradicts that; the Dataverse terms are what currently apply.
- There is no FST I–II, so you would need a second dataset for a light-skin comparison group.
- Diagnoses are clinical, not biopsy-confirmed.

**3. [PASSION](https://passionderm.github.io/)** — mostly paediatric patients from Madagascar, Guinea, Malawi and Tanzania.
- The site says: "This dataset is provided under the PASSION data public license." You get it through the "Request Access to Dataset" form.
- It has only four coarse classes: eczema, fungal, scabies, other (44 conditions underneath), plus an impetigo flag. Labels were checked by board-certified dermatologists.
- FST III–VI only. Guinea is mostly FST VI. The ResNet-50 baseline scored 0.70 balanced accuracy on FST V and 0.73 on FST VI ([paper](https://arxiv.org/html/2411.04584v1)).
- You may not repost the data or share the direct download link.

**4. [DDI](https://ddi-dataset.github.io/)** — the best choice for a clean audit.
- Every diagnosis is biopsy-proven, and FST I–II and V–VI images were deliberately matched on diagnosis, age, gender and photo date.
- 207 images in FST V–VI (159 benign, 48 malignant), per the [AIMI page](https://aimi.stanford.edu/datasets/ddi-diverse-dermatology-images).
- **Caveat:** skin tone comes only as groups (I–II / III–IV / V–VI), so you cannot separate V from VI.
- Terms: "personal, non-commercial research purposes only". No redistribution, and every user registers individually.
- Paper: [Daneshjou 2022, Sci Adv](https://doi.org/10.1126/sciadv.abq6147), which showed state-of-the-art models performing worse on darker skin.

**5. [SCIN](https://github.com/google-research-datasets/scin)** — smartphone photos donated by US internet users.
- Skin tone comes three ways: self-reported FST, dermatologist-estimated FST, and Monk labels from US and India lay graders.
- Only 3,061 of the 5,033 cases have a dermatologist diagnosis. Among those:
  - dermatologist-estimated FST VI: 27
  - self-reported FST VI: 102
  - Monk 7–10 (US graders): 108
- The diagnosis is a weighted differential from dermatologists looking at the photos, not a confirmed diagnosis.
- The licence allows commercial use and redistribution but forbids re-identification.

## Known, not confirmed
- **[DDI-2](https://doi.org/10.57761/pgwn-6b62)** (Stanford, 2026): 665 biopsy-proven photos covering 169 diagnoses, from patients who self-identified as Asian. Each image has an FST label. The Redivis page would not render, so I couldn't read the terms or count V–VI. From memory, it likely uses the same AIMI registration as DDI. My guess is that it is mostly FST III–IV.
- **[UNICAMP acral lesions, Black skin](https://zenodo.org/records/10570316)**: palm, sole and nail lesions, CC BY-NC-SA 4.0. Access is by request on Zenodo with an institutional email. The page doesn't confirm per-image FST labels or give counts.

## Not recommended, and why
- **MRA-MIDAS:** biopsy-proven and has FST, but only 16.8% of patients are FST III–VI ([preprint](https://www.medrxiv.org/content/10.1101/2024.06.27.24309562v1.full)).
- **PAD-UFES-20:** has an FST field, but from memory almost everyone is FST I–III.
- **HAM10000 and the ISIC Archive:** almost no per-image FST, and overwhelmingly light skin.
- **CleanPatrick and SkinCon:** extra annotation layers on Fitzpatrick17k/DDI images, not new images. CleanPatrick's label-quality flags are still useful alongside Fitzpatrick17k.
- **[Africa-skin-cancer-images-EHR](https://huggingface.co/datasets/electricsheepafrica/Africa-skin-cancer-images-EHR):** HAM10000 images with estimated skin tones and synthetic patient records, not real darker-skin patients.

## What I could not find
- No large biopsy-proven dataset with hundreds of each of FST V and FST VI separately.
- Monk labels only exist in SCIN and DermaCon-IN, and both have very few images at Monk 9–10.

## Next step
DDI is the strongest benchmark. The others add volume to it:
1. **DDI** for the matched, biopsy-proven comparison.
2. **Fitzpatrick17k** for many conditions with separate V and VI groups.
3. **DermaCon-IN** and **PASSION** for real-world darker-skin data from India and Africa.

Fitzpatrick17k, DermaCon-IN, SCIN and DDI can all be downloaded today. PASSION needs a request, which probably takes a few days.

Because these datasets were labelled differently (crowd annotators, dermatologists, self-report), report results per dataset rather than pooling the skin tone groups.

Files are in `/private/tmp/e-kUtDGP/home/cwd`:
- `dataset-shortlist.html` — interactive shortlist page
- `dataset-scout/shortlist.json` — the data behind it