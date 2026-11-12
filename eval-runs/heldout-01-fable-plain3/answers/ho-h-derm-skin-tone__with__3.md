Five public datasets meet your bar: a skin tone label and a diagnosis on every image or case, with real numbers in types V and VI. I checked these against the papers and dataset pages but did not download any of the data.

| Dataset | Size | Tone label | Dark-skin coverage | Diagnosis label | Access |
|---|---|---|---|---|---|
| **DDI** (Stanford) | 656 clinical images, 570 patients | Fitzpatrick, in three bins (I–II, III–IV, V–VI) | 207 images in V–VI, balanced by design against 208 and 241 | Biopsy-confirmed; 485 benign, 171 malignant | Stanford AIMI, research-use agreement |
| **Fitzpatrick17k** | 16,577 clinical images from two online atlases | Fitzpatrick I–VI per image (565 unlabelled) | About 1,533 type V and 635 type VI | 114 conditions from atlas captions, no histopathology | GitHub; images fetched by URL |
| **PASSION** | 4,901 clinical images, 1,653 patients, four sub-Saharan African countries | Fitzpatrick per patient | Nearly all III–VI; the test split alone has 341 type V and 88 type VI out of 986 | Eczema, fungal, scabies, other (mostly paediatric), plus an impetigo flag | passionderm.github.io, own licence |
| **DermaCon-IN** | 5,450 clinical images, about 3,000 patients, South India | Both Fitzpatrick and Monk | Types IV and V dominate; type VI has 136 images; Monk centres on 6–7 | 245 dermatologist-assigned diagnoses | Harvard Dataverse, CC BY-NC-SA, access verification |
| **SCIN** (Google) | 10,408 images, 5,033 cases, US crowdsourced | Dermatologist-estimated Fitzpatrick, self-reported Fitzpatrick, and Monk, per case | Thin: 5.3% type V and 0.6% type VI by dermatologist estimate; almost nothing at Monk 8+ | Dermatologist differential, usable for roughly 56% of cases | GitHub, SCIN data use licence |

- **Skin cancer classifier:** DDI is the one to use, because it is the only set with biopsy-confirmed labels and deliberate tone balance. Its limits are the small size and the three-bin tone label, so you cannot separate V from VI.
- **General skin-condition classifier:** Fitzpatrick17k gives the most type V and VI images. Its diagnoses are noisy (one audit estimated about 3.4% mislabelled), and as I recall the tone labels came from non-dermatologist annotators.
- **PASSION and DermaCon-IN:** These are the only two drawn from predominantly dark-skinned populations. Their disease mix is infectious and inflammatory, so they do not suit a cancer model.
- **SCIN:** It qualifies on labels, but its type VI count is likely only a few dozen cases, so treat it as a supplement.

In every one of these sets, skin tone is correlated with disease mix, image source, or both. Compare performance within a diagnosis where you can, or the tone gap will be confounded with case difficulty.

Three sets look like they qualify but don't:

- **MILK10k** (ISIC): 5,240 lesions with paired clinical and dermoscopic images, but its tone label is its own 0–5 scale, not Fitzpatrick or Monk, and it is mostly mid-range tones. It is the only dermoscopy option that comes close.
- **MRA-MIDAS** (Stanford): biopsy-confirmed with Fitzpatrick per patient, but only about 17% of patients are type III or darker.
- **PAD-UFES-20**: has Fitzpatrick labels for part of the data, but type VI is essentially absent.

Sources:
- [DDI paper (arXiv 2203.08807)](https://arxiv.org/pdf/2203.08807)
- [SkinCon paper, DDI counts](https://proceedings.nips.cc/paper_files/paper/2022/file/7318b51b52078e3af28197e725f5068a-Paper-Datasets_and_Benchmarks.pdf)
- [Fitzpatrick17k paper (CVPRW 2021)](https://openaccess.thecvf.com/content/CVPR2021W/ISIC/papers/Groh_Evaluating_Deep_Neural_Networks_Trained_on_Clinical_Images_in_Dermatology_CVPRW_2021_paper.pdf)
- [Skin Type Diversity in Skin Lesion Datasets: A Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11343783/)
- [Fitzpatrick17k quality audit (arXiv 2401.14497)](https://arxiv.org/pdf/2401.14497)
- [PASSION paper (arXiv 2411.04584)](https://arxiv.org/html/2411.04584)
- [PASSION project repository](https://github.com/Digital-Dermatology/PASSION_project)
- [DermaCon-IN paper (arXiv 2506.06099)](https://arxiv.org/html/2506.06099)
- [DermaCon-IN on Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/W7OUZM)
- [SCIN paper (arXiv 2402.18545)](https://arxiv.org/html/2402.18545v1)
- [SCIN repository](https://github.com/google-research-datasets/scin)
- [MILK10k on the ISIC Archive](https://api.isic-archive.com/doi/milk10k/)
- [MILK10k paper (JID)](https://www.jidonline.org/article/S0022-202X(25)02270-5/fulltext?rss=yes)
- [MRA-MIDAS at Stanford AIMI](https://aimi.stanford.edu/datasets/mra-midas-Multimodal-Image-Dataset-for-AI-based-Skin-Cancer)
- [MIDAS paper (NEJM AI)](https://ai.nejm.org/doi/full/10.1056/AIdbp2400732)