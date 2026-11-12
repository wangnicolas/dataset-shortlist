Five public datasets meet all three conditions (skin tone label, diagnosis, real type V/VI representation), and no single one is ideal: the large ones have noisier labels and the cleanly labelled one is small. I checked the counts below against project pages and papers where I could; the gaps are flagged.

| Dataset | Size and type | Skin tone label | Dark-skin representation | Diagnosis label | Access |
|---|---|---|---|---|---|
| **DDI** (Stanford) | 656 clinical images, 570 patients | Fitzpatrick, from the in-person visit plus review by two dermatologists; released in pairs (I–II, III–IV, V–VI) | About a third is V–VI (207 images, from memory), by design | Biopsy-confirmed, benign vs malignant plus specific disease | Stanford AIMI portal, research use agreement, non-commercial |
| **Fitzpatrick17k** | 16,577 clinical images, 114 conditions | Fitzpatrick I–VI per image, annotated from the photo by non-dermatologists | 1,533 type V and 635 type VI (about 13%) | Taken from atlas websites, not pathology-confirmed | GitHub; images are scraped from two online atlases |
| **SCIN** (Google) | 10,000+ images from 5,000+ contributions | Self-reported Fitzpatrick, dermatologist-estimated Fitzpatrick, and layperson-estimated Monk | Roughly 8.5% type V and 5.7% type VI, per a secondary source; few above Monk 8 | Dermatologist weighted differential from photos; no biopsy | Google Cloud bucket, SCIN Data Use License |
| **PASSION** | 4,901 clinical images, 1,653 patients, Sub-Saharan Africa | Fitzpatrick per patient | Essentially all IV–VI | Eczema, fungal infection, scabies, impetigo; mostly paediatric | Request form, non-commercial |
| **DermaCon-IN** | 5,450 clinical images, 3,002 patients, South India | Both Fitzpatrick and Monk, expert-rated with dermatologist verification | Types IV and V dominate; type VI is only 136 images; Monk centres on 6–7 | 245 dermatologist-assigned diagnoses | Harvard Dataverse, CC BY-NC-SA 4.0 |

Caveats that matter for an audit:

- **DDI:** It is the only one with both in-person skin tone and biopsy-proven diagnoses, so it is the cleanest test set. It is small, so confidence intervals will be wide, and you cannot separate V from VI.
- **Fitzpatrick17k:** Use the cleaned version (Fitzpatrick17k-C, 11,394 images). The original has thousands of near-duplicate pairs, many with conflicting diagnosis or skin type labels, and a 2025 audit estimated a substantial diagnosis label-error rate.
- **SCIN:** The three skin tone labels disagree with each other often enough that you should pick one in advance and report sensitivity to the choice. I could not confirm the V/VI percentages from the primary paper's supplement.
- **PASSION:** It has no light-skin group, so it only works as the dark-skin arm alongside another dataset, which confounds skin tone with site, camera and disease mix. I did not confirm its exact per-type split.
- **DermaCon-IN:** Good for type V and the Monk scale, weak for type VI.

Datasets that carry Fitzpatrick labels but fail your representation requirement: PAD-UFES-20 (very few V/VI, from memory), MIDAS (type VI is 2 patients) and the ISIC archive subsets, including MILK10k, which I believe are overwhelmingly light-skinned. HAM10000, Derm7pt and DermNet have no skin tone labels at all.

My recommendation is DDI as the primary test set for skin cancer, with Fitzpatrick17k-C and SCIN for general dermatology at larger scale, and PASSION or DermaCon-IN if you need more type V/VI volume.

Sources:
- [DDI project page](https://ddi-dataset.github.io/)
- [Fitzpatrick17k quality audit (Scientific Data 2025)](https://www.nature.com/articles/s41597-025-04382-5)
- [CleanPatrick benchmark](https://arxiv.org/html/2505.11034)
- [Fitzpatrick17k per-type counts](https://github.com/notjeffff/skin-tone-gap-fitzpatrick17k)
- [SCIN GitHub repo](https://github.com/google-research-datasets/scin)
- [SCIN paper (JAMA Network Open)](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2826506)
- [SCIN Fitzpatrick breakdown, secondary source](https://arxiv.org/html/2510.00055)
- [PASSION project page](https://passionderm.github.io/)
- [PASSION paper](https://www.arxiv.org/pdf/2411.04584)
- [DermaCon-IN paper](https://arxiv.org/html/2506.06099)
- [MIDAS paper (NEJM AI)](https://ai.nejm.org/doi/full/10.1056/AIdbp2400732)
- [Skin lesion dataset catalog](https://github.com/AxDante/skin-lesion-dataset-analysis)