Five public datasets fit your requirements, and none is clean on every axis, so a credible audit usually combines two or three. The counts below come from my recall of the papers plus a quick web check of summaries, not from downloading the data, so confirm them against the metadata files.

## Datasets that fit

| Dataset | Size | Skin tone label | Diagnosis label | Darker-skin (V–VI) representation | Access |
|---|---|---|---|---|---|
| **Fitzpatrick17k** | 16,577 clinical photos, 114 conditions | Fitzpatrick I–VI per image, by non-dermatologist annotators | Taken from the atlas sites, not biopsy-confirmed | About 1,530 type V and 635 type VI (13%) | GitHub; images scraped from two online atlases, non-commercial |
| **DDI (Diverse Dermatology Images)** | 656 clinical photos, 570 patients | Fitzpatrick per patient, only as groups I–II / III–IV / V–VI | Biopsy-proven, 78 diseases plus benign/malignant | 207 images in V–VI, balanced by design against 208 in I–II and 241 in III–IV | Stanford AIMI, research use agreement |
| **SCIN** | 10,000+ photos from 5,000+ US contributors | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and layperson-estimated Monk | Dermatologist differential diagnoses with confidence weights, no biopsy | Roughly 8.5% type V and 5.7% type VI per a secondary source; very few at Monk 8–10 | GitHub / Google Cloud bucket, open licence |
| **PASSION** | 4,901 phone photos, 1,653 patients, sub-Saharan Africa | Fitzpatrick per patient, IV–VI only | Common paediatric conditions (eczema, fungal, scabies, impetigo), dermatologist-checked | Essentially the whole dataset is dark skin | passionderm.github.io, own licence |
| **DermaCon-IN** | 5,450 clinical photos, about 3,000 patients, South India | Fitzpatrick and Monk per image, rated on unaffected skin | 245 dermatologist-assigned diagnoses in a hierarchy | Types IV and V dominate; type VI is thin | See the paper (NeurIPS 2025); I did not confirm the download location |

## What each is good for

- **DDI** is the cleanest test set: biopsy-proven and balanced, built for exactly this audit. It is small, and the grouped labels mean you cannot separate V from VI.
- **Fitzpatrick17k** gives the largest V–VI count across the most conditions. It has documented near-duplicates and label errors, so use the cleaned **Fitzpatrick17k-C** splits.
- **SCIN** is the only one with both scales, and it reflects consumer-style photos of mostly common inflammatory and infectious conditions. Its diagnoses are weighted differentials, so you need to decide how to score a "correct" answer.
- **PASSION** has no light-skin group, so it only works as the dark-skin arm of a comparison. Any gap against another dataset then mixes skin tone with site, camera and age (it is paediatric).
- **DermaCon-IN** fills the IV–V range well with dermatologist-rated tone on both scales, but adds little for type VI.

## Datasets that have the label but fail on representation

- **MIDAS** (Stanford, biopsy-proven, paired dermoscopy and clinical): Fitzpatrick is recorded, but only about 17% of patients are type III or above.
- **PAD-UFES-20** (Brazil, smartphone photos): Fitzpatrick is in the metadata for part of the set, with very few V–VI.
- **MILK10k** (ISIC, 5,240 lesions with clinical and dermoscopic pairs): it has its own six-level skin tone scale, deliberately not Fitzpatrick, and is mostly mid-range.
- **HAM10000, BCN20000, Derm7pt and most of the ISIC archive**: no skin tone label at all.

Dermoscopy is the weak spot: I know of no public dermoscopy set with substantial V–VI numbers, so in practice your audit will rest on clinical photos.

Sources:
- [SCIN GitHub repo](https://github.com/google-research-datasets/scin)
- [SCIN paper (arXiv 2402.18545)](https://arxiv.org/pdf/2402.18545)
- [Secondary source for SCIN Fitzpatrick breakdown (arXiv 2510.00055)](https://arxiv.org/html/2510.00055v2)
- [PASSION paper (arXiv 2411.04584)](https://arxiv.org/html/2411.04584v1)
- [DermaCon-IN paper (arXiv 2506.06099)](https://arxiv.org/html/2506.06099)
- [MIDAS paper (NEJM AI)](https://ai.nejm.org/doi/full/10.1056/AIdbp2400732)
- [MILK10k on the ISIC Archive](https://api.isic-archive.com/doi/milk10k/)
- [Fitzpatrick17k quality analysis and Fitzpatrick17k-C (arXiv 2401.14497)](https://arxiv.org/html/2401.14497)
- [CleanPatrick benchmark (arXiv 2505.11034)](https://arxiv.org/html/2505.11034v2)
- [Global Atlas of Digital Dermatology (arXiv 2601.00840)](https://arxiv.org/pdf/2601.00840)