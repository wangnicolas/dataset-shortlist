Five public datasets meet all three criteria (skin tone label, diagnosis, non-trivial V/VI); most of the well-known skin datasets fail on the third. I counted the skin-tone distributions directly from the metadata files for Fitzpatrick17k, SCIN, DermaCon-IN and the ISIC Archive; the DDI and PASSION numbers are from their papers.

## Datasets that qualify

| Dataset | Images | Skin tone label | Type V / VI | Diagnosis | Access |
|---|---|---|---|---|---|
| **DDI** (Stanford) | 656 clinical, 570 patients | Fitzpatrick, grouped I–II / III–IV / V–VI | 207 images in V–VI (48 malignant) | 78 diseases plus benign/malignant; all malignancies biopsy-confirmed | Stanford AIMI, research use agreement |
| **Fitzpatrick17k** | 16,577 clinical | Fitzpatrick I–VI, assigned from the image by non-dermatologist annotators | 1,533 / 635 | 114 conditions from atlas captions, not biopsy | GitHub CSV of image URLs |
| **DermaCon-IN** (South India) | 5,450 clinical, ~3,000 patients | Fitzpatrick and Monk | Fitzpatrick 1,285 / 136; Monk 7–9: 2,059 | 245 diagnoses, dermatologist-labelled | Harvard Dataverse, CC BY-NC-SA 4.0 |
| **PASSION** (Madagascar, Guinea, Malawi, Tanzania) | 4,901 clinical, 1,653 patients | Fitzpatrick III–VI | 341 / 88 in the 20% test split, so roughly 1,700 / 440 overall (my extrapolation) | Eczema, fungal, scabies, other, plus an impetigo flag | passionderm.github.io, own licence |
| **SCIN** (Google) | 10,407 consumer photos, 5,033 cases | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and Monk from lay raters | Dermatologist-estimated 359 / 69 cases; self-reported 214 / 143; Monk 7–10 (US raters): 207 | Dermatologist differential diagnoses, weighted, not biopsy | GitHub and public Google Cloud bucket |

## How I would use them

- **DDI as the headline test set.** It is the only one built for this audit: light and dark groups are matched on diagnosis category, age and sex, and the labels are pathology-backed. It is small, so confidence intervals will be wide.
- **Fitzpatrick17k for breadth.** It has the most V/VI images, but both the skin type and diagnosis labels are noisy, and only 89 of the 114 conditions have any type VI examples. The atlas images may also overlap with the training data of the classifiers you are auditing.
- **DermaCon-IN and PASSION for real clinic populations.** Both skew to inflammatory and infectious disease rather than cancer, and neither has lighter types (I–II) for a within-dataset comparison.
- **SCIN if the classifier targets consumer phone photos or you want Monk labels.** Type VI is thin and half the cases have no self-reported Fitzpatrick type.

Disease mix differs by skin tone in all of these, so compare within diagnosis, or a tone gap will partly be a case-mix gap.

## Near misses

- **MSKCC Skin Tone Labeling Dataset (ISIC Archive):** 4,879 images from 64 patients, balanced across Fitzpatrick I–VI (813 type V, 750 type VI), with Monk and colorimeter readings. Every lesion is labelled benign, so it only supports a false-positive-rate comparison.
- **PAD-UFES-20:** has a Fitzpatrick field, but only 10 type V and 1 type VI images.
- **MRA-MIDAS:** biopsy-proven paired clinical and dermoscopic images with Fitzpatrick type, but only 16.8% of patients are type III or darker.
- **MILK10k:** 10,480 paired images with a six-level skin tone field (not Fitzpatrick). Its documentation says most patients sit in the middle of the scale; I did not get the per-level counts.
- **Other ISIC collections (including HAM10000):** no usable skin tone labels with V/VI. The MSKCC set and PAD-UFES-20 are the only two collections in the archive with any type V or VI label.

Sources:
- [Fitzpatrick17k paper](https://arxiv.org/abs/2104.09957) and [metadata CSV](https://github.com/mattgroh/fitzpatrick17k)
- [DDI paper](https://arxiv.org/pdf/2203.08807) and [project page](https://ddi-dataset.github.io)
- [SCIN repository](https://github.com/google-research-datasets/scin) and [paper](https://arxiv.org/pdf/2402.18545)
- [PASSION paper](https://www.arxiv.org/pdf/2411.04584) and [dataset site](https://passionderm.github.io/)
- [DermaCon-IN paper](https://arxiv.org/html/2506.06099) and [Harvard Dataverse record](https://doi.org/10.7910/DVN/W7OUZM)
- [MSKCC Skin Tone Labeling Dataset](https://api.isic-archive.com/collections/413/)
- [MRA-MIDAS dataset page](https://aimi.stanford.edu/datasets/mra-midas-Multimodal-Image-Dataset-for-AI-based-Skin-Cancer)
- [MILK10k dataset page](https://api.isic-archive.com/doi/milk10k/)