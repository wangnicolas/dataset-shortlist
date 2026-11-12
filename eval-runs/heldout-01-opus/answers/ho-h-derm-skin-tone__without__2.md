Five public datasets meet your requirements: every image comes with a skin tone label and a diagnosis, and types V–VI are present in real numbers. They differ a lot in how many dark-skin images they have and in how reliable the diagnoses are.

## Datasets that meet your requirements

| Dataset | Images / patients | Skin tone label | Diagnosis label | Darker skin coverage | Access |
|---|---|---|---|---|---|
| **Fitzpatrick17k** (Groh et al., 2021) | ~16.6k clinical photos, 114 conditions | Fitzpatrick I–VI, crowd-annotated | Taken from atlas websites; not biopsy-confirmed | About 1.5k type V and about 600 type VI (from memory; check the CSV) | Public CSV with image URLs; some links no longer work |
| **DDI – Diverse Dermatology Images** (Stanford, Daneshjou et al., 2022) | 656 images / 570 patients | Fitzpatrick in **grouped bins only**: I–II, III–IV, V–VI | **All biopsy-proven**, benign vs. malignant plus specific diagnosis | About a third of images are V–VI. Small, but designed to be balanced | Stanford AIMI, research-use agreement |
| **SCIN** (Google, 2024) | 10,408 images / 5,033 contributors (US, crowdsourced) | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and Monk scale ratings from 2 non-clinical annotators (US and India) | Dermatologist differential diagnosis with confidence ratings; not biopsied | Skews more toward types III–VI than clinic-sourced sets; per-type counts are in the supplement | Open (GitHub / GCS) |
| **PASSION** (MICCAI 2024) | 4,901 images / 1,653 children (Madagascar, Guinea, Malawi, Tanzania) | Fitzpatrick IV–VI, **mostly type VI** | Common pediatric conditions in sub-Saharan Africa (eczema, fungal infections, scabies, impetigo), checked by dermatologists | Best available source of type V–VI images | passionderm.github.io (data-use agreement) |
| **DermaCon-IN** (2025) | 5,450 images / ~3,000 patients (South India, outpatient clinics) | **Both Fitzpatrick and Monk**, rated by dermatologists on unaffected skin | Hierarchical disease labels, diagnostic certainty, image gradability | Mostly types IV and V, then III; less type VI than PASSION | See the arXiv paper for the access route |

## How I'd combine them

- **For a headline comparison across skin tones, use Fitzpatrick17k.** It's the only one that's large and spans all of I–VI. Its skin type labels and diagnoses are noisy, so report that as a limitation.
- **For a cleaner confirmation, use DDI.** Its diagnoses are biopsy-proven, but you only get the coarse V–VI bin and a few hundred images.
- **For Monk scale analysis, use SCIN and DermaCon-IN.** They're the main public datasets with Monk labels.
- **For data from outside the US and Europe, use PASSION and DermaCon-IN.** PASSION is pediatric and covers a different set of diseases, so don't pool it naively with adult datasets.

## Datasets that don't fit

- **HAM10000, BCN20000 and most of the ISIC archive:** no Fitzpatrick labels, or skin tone metadata that's sparse and overwhelmingly light.
- **PAD-UFES-20:** has Fitzpatrick labels, but almost all patients are types I–III.
- **MIDAS (Stanford):** has Fitzpatrick labels and biopsy-proven diagnoses, but as I recall it skews toward lighter skin. Check its distribution before relying on it.

## Audit design pitfalls

1. **The mix of conditions differs by skin tone in every one of these datasets.** A raw accuracy gap between skin types can just reflect different diseases. Stratify by condition, or reweight, before you attribute a gap to skin tone.
2. **Skin tone labels estimated from photos are noisy.** SCIN shows self-reported and dermatologist-estimated types disagreeing, and the two Monk annotators differing. Consider a sensitivity analysis that merges adjacent types.
3. **The V–VI groups are small, especially in DDI.** Report confidence intervals (for example by bootstrap), not point estimates.

Sources:
- [PASSION (arXiv 2411.04584)](https://arxiv.org/html/2411.04584v1) · [MICCAI page](https://papers.miccai.org/miccai-2024/590-Paper3722.html) · [passionderm.github.io](https://passionderm.github.io/)
- [DermaCon-IN (arXiv 2506.06099)](https://arxiv.org/html/2506.06099)
- [SCIN GitHub](https://github.com/google-research-datasets/scin) · [SCIN schema](https://github.com/google-research-datasets/scin/blob/main/dataset_schema.md) · [Google Research blog](https://research.google/blog/scin-a-new-resource-for-representative-dermatology-images/) · [JAMA Netw Open paper](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2826506)
- [Global Atlas of Digital Dermatology (arXiv 2601.00840)](https://arxiv.org/html/2601.00840)

Fitzpatrick17k and DDI details are from my own knowledge, not this search. Check their exact counts against the original papers.