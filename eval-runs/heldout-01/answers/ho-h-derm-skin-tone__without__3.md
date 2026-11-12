Three public datasets fit your criteria, and a fourth is a common trap. The counts below are from memory and I haven't checked them against the current dataset pages, so confirm them before you plan your subgroup sizes.

**Good fits**

| Dataset | Type | Skin tone label | Diagnosis label | Dark-skin coverage |
|---|---|---|---|---|
| **Fitzpatrick 17k** (Groh et al., 2021) | Clinical photos, about 16.5k images, 114 conditions | Fitzpatrick I–VI per image, plus an "unknown" category | Condition name from the source atlases | The largest pool of V/VI images, roughly a few thousand. |
| **DDI, Diverse Dermatology Images** (Stanford, Daneshjou et al., 2022) | Clinical photos, about 650 images, about 570 patients | Fitzpatrick, grouped as I–II, III–IV, V–VI | Biopsy-confirmed, with a benign/malignant flag and disease name | Roughly a third of the images are V–VI. |
| **SCIN** (Google, 2024) | Clinical photos, 10k+ images from 5k+ volunteers in the US | Fitzpatrick and Monk, both self-reported and dermatologist-estimated | Dermatologist differential diagnoses, with weighted confidence | Broad skin-tone spread, and it's the only one here with Monk labels. |

- **Fitzpatrick 17k:** the labels were crowd-annotated, so they are noisy, often off by about one type. The images are scraped from two online atlases. The repo mostly distributes URLs plus a CSV, so some links may have rotted.
- **DDI:** it's the cleanest ground truth and was built for this kind of audit. It's too small for fine-grained per-disease analysis, and you must request access under a non-commercial research agreement.
- **SCIN:** the diagnoses are dermatologist opinions rather than biopsy results, and the images are patient-taken and varied in quality. It also skews toward common inflammatory conditions.

**Not suitable for V/VI**
- **PAD-UFES-20:** smartphone images with Fitzpatrick recorded, but almost all are types I–III.
- **HAM10000, ISIC 2019, ISIC 2020 and ISIC 2024:** dermoscopy with little or no skin tone metadata, and very few dark-skin images. Some papers have estimated tone with ITA (individual typology angle) to audit these. That's an estimate rather than a clinical label, so I wouldn't treat it as ground truth.

I don't know of a public dermoscopy dataset with both real Fitzpatrick labels and substantial V/VI representation. If you need dermoscopy specifically, expect to rely on ITA-derived labels or give it up.

**Suggested setup**
- Use DDI as your clean test set, since it has biopsy-proven labels and V–VI is well represented.
- Use Fitzpatrick 17k for statistical power, and treat its tone labels as noisy. You could report results with and without the "unknown" images.
- Use SCIN as an external check, and as your Monk-scale source.
- Check that the disease mix is similar across tone groups. In Fitzpatrick 17k especially, condition and tone are confounded, which can look like a fairness gap when it's a case-mix difference.

I can fetch the current dataset pages and pull exact per-type counts and license terms, if you'd like.