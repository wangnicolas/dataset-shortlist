Five public datasets meet your criteria: every image (or patient) has both a skin tone label and a diagnosis, and types V–VI make up a real share. In rough order of usefulness for your audit:

| Dataset | Images / patients | Skin tone label | Diagnosis label | Types V–VI | Access |
|---|---|---|---|---|---|
| **Fitzpatrick17k** | ~16.6k clinical photos | Fitzpatrick I–VI, judged from the photo by annotators | 114 conditions, taken from atlas captions (not biopsy-confirmed) | About 1.5k type V and 600+ type VI (from memory; check the CSV) | Public CSV of image URLs. Some links are now dead, so check how many images you can still download. |
| **DDI (Diverse Dermatology Images)**, Stanford | 656 images / 570 patients | Fitzpatrick, but only in **grouped bins**: I–II, III–IV, V–VI | **Biopsy-confirmed**: benign vs malignant plus specific diagnoses | About 200 images in V–VI. Built deliberately to compare light and dark skin on matched cases. | Free data use agreement through Stanford AIMI |
| **SCIN** (Google/Stanford) | 10,408 images / 5,033 cases | Fitzpatrick reported by the patient **and** estimated by dermatologists, plus **Monk 1–10** from two annotators (US and India) | Dermatologists' weighted differential diagnoses; some cases have no condition label | Spread across Fitzpatrick types, but **few cases above Monk 8** (the authors say so themselves) | Open on GitHub / GCS |
| **DermaCon-IN** (NeurIPS 2025) | 5,450 images / 3,002 patients, South India | **Fitzpatrick and Monk** for each image, rated on unaffected skin | 245 diagnoses set by dermatologists, in a hierarchical taxonomy | Concentrated in types IV–VI | Harvard Dataverse |
| **PASSION** (MICCAI 2024) | 4,901 images / 1,653 patients, children in Sub-Saharan Africa | Fitzpatrick | Common conditions such as eczema, fungal infections, scabies and impetigo, checked by dermatologists | Almost all IV–VI | Download after request at passionderm.github.io |

**How to use them together:**
- **Fitzpatrick17k** and **DDI** are the standard pair for a light-versus-dark comparison within one dataset. Fitzpatrick17k gives you sample size. DDI gives you biopsy-confirmed ground truth, but its V–VI bin is small, so report confidence intervals.
- **SCIN** is your main option if you want Monk labels from a US population. It has two sets of Fitzpatrick labels and two of Monk, so you can also show how much your results depend on who assigned the skin tone.
- **DermaCon-IN** and **PASSION** cover the darkest skin well, but they have almost no type I–II skin. That makes them good for stress-testing a model on dark skin, not for a within-dataset gap. Their mix of conditions (inflammatory and infectious, children in PASSION) also differs from skin-cancer benchmarks. Keep that confound separate from skin tone in your analysis.

**Ones that don't fit your criteria:**
- **HAM10000 / ISIC** have no per-image skin tone labels.
- **PAD-UFES-20** and **MIDAS** have Fitzpatrick labels, but very few type V–VI images.

**Two caveats for your write-up:**
1. In most of these datasets, Fitzpatrick is estimated from the photo rather than measured on the patient. SCIN's own data shows that patient-reported and expert-rated values disagree.
2. Fitzpatrick measures how skin reacts to UV, not its colour, which is why the newer datasets add Monk.

**What I checked:** I confirmed the details for SCIN, DermaCon-IN and PASSION in a web search just now. The Fitzpatrick17k and DDI figures are from memory, so check them against the papers. I also didn't find the exact per-type counts for SCIN or DermaCon-IN. They're in SCIN's supplementary tables (eTable 9–10) and DermaCon-IN's distribution figures, or you can count them from the label CSVs.

Sources:
- [PASSION paper (arXiv)](https://arxiv.org/html/2411.04584v1) · [MICCAI page](https://papers.miccai.org/miccai-2024/590-Paper3722.html) · [Global Atlas of Digital Dermatology](https://arxiv.org/pdf/2601.00840)
- [DermaCon-IN (arXiv)](https://arxiv.org/html/2506.06099) · [DermaCon-IN code](https://github.com/shan4035/DermaCon-IN-code) · [NeurIPS listing](https://mlanthology.org/neurips/2025/madarkar2025neurips-dermaconin/)
- [SCIN GitHub](https://github.com/google-research-datasets/scin) · [SCIN schema](https://github.com/google-research-datasets/scin/blob/main/dataset_schema.md) · [SCIN JAMA Netw Open paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11579799/) · [SCIN arXiv](https://arxiv.org/html/2402.18545)