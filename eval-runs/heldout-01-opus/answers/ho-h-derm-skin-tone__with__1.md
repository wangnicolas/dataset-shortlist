Five public datasets have both a skin tone label and a diagnosis for every image, with Fitzpatrick V and VI present in real numbers (hundreds, not a handful). They are **Fitzpatrick17k, DDI, PASSION, DermaCon-IN and SCIN**. Each has a weakness, so for an audit you'd want two or three together. Checked on 12 Nov 2026.

## What I assumed you need
- **Must have:** a skin tone label per image or patient (Fitzpatrick or Monk); a diagnosis per image; Fitzpatrick V and VI in real numbers.
- **Nice to have:** obtainable without your institution signing a data agreement; biopsy- or expert-confirmed labels.
- **Assumed:** you only need research use, not commercial use. Almost all of these are non-commercial.

## Shortlist
| # | Dataset | Access | Licence | Size | Darker skin (V and VI) | Checked |
|---|---|---|---|---|---|---|
| 1 | **Fitzpatrick17k** | Labels file is open; images via source links or a request form, a few days | CC BY-NC-SA 3.0 | 16,577 images, 114 conditions | about 1,500 type V and 600 type VI | site today; counts from memory |
| 2 | **DDI** (Stanford) | Free account and research agreement, a few days | Stanford research use agreement (non-commercial, from memory) | 656 biopsy-proven images, 570 patients | **207 images of V–VI** (159 benign, 48 malignant) | today |
| 3 | **PASSION** (sub-Saharan Africa, children) | Request form, a few days | PASSION licence: non-commercial, no reposting | 4,901 images, 1,653 patients | types III–VI only; the test split alone has 341 type V and 88 type VI images | today |
| 4 | **DermaCon-IN** (South India) | Open download on Harvard Dataverse | CC BY-NC-SA 4.0 | 5,450 images, 3,002 patients, 245 diagnoses | mostly types III–V; number of type VI not confirmed | registry today; the download page blocked my automated check |
| 5 | **SCIN** (Google, US contributors) | Open download | SCIN licence (permissive; bans re-identification) | 10,000+ images, 5,000+ cases | depends on which label you use (see below) | today |

## Details
1. **[Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k)** is clinical photos from two online dermatology atlases, Atlas Dermatologico and DermaAmin. Each image has a single Fitzpatrick type (I–VI) and a diagnosis, so it has the most type V–VI images of anything here. The skin types were judged from the photos by crowd annotators, and the diagnosis labels are known to be noisy. The repo has the label file and image links, and some links are broken. For the full image set there is a request form. Reference: Groh et al. 2021.
2. **[DDI](https://aimi.stanford.edu/datasets/ddi-diverse-dermatology-images)** was built for exactly this kind of comparison. Its V–VI images are matched to I–II images by diagnosis, age, sex and photo date. All diagnoses are confirmed by biopsy. Skin type comes only in three groups (I–II, III–IV, V–VI), and it is small. Its authors found that commercial and published models did worse on V–VI ([arXiv 2203.08807](https://arxiv.org/pdf/2203.08807)), which gives you a ready baseline. To get it, register at Stanford AIMI, accept the agreement and download from the link on that page.
3. **[PASSION](https://passionderm.github.io/)** is phone photos of children in Madagascar, Guinea, Malawi and Tanzania. Labels are Fitzpatrick type, a diagnosis (eczema, fungal infection, scabies or "other", with ICD-10 and ICD-11 codes across 44 conditions), plus body site, age and sex. It has a fixed train/test split by patient. Since there are no type I–II patients, use it as an external darker-skin test set, not for a light-versus-dark comparison within the dataset. The authors' baseline scored a balanced accuracy of 0.70 on type V and 0.73 on type VI ([MICCAI 2024](https://arxiv.org/html/2411.04584v1)).
4. **[DermaCon-IN](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/W7OUZM)** is the only clinical dataset here with **both Fitzpatrick and Monk** labels on every image. Four dermatologists labelled the diagnoses; where two of them labelled the same images, they agreed well (kappa 0.84). The paper is inconsistent about which skin types it covers: in one place IV–VI, in another III–IV. Check the distribution after downloading ([paper](https://arxiv.org/html/2506.06099)).
5. **[SCIN](https://github.com/google-research-datasets/scin)** comes with three tone labels:
   - Self-reported: V is 9.8% and VI is 6.6%.
   - Dermatologist estimate: V is 5.3% and VI is only 0.6%.
   - Monk scale from two lay graders (one in the US, one in India): 8 and above is under 1%.

   Diagnoses are dermatologists' differentials from the photos, with no biopsy. It is useful mostly as a Monk-scale check, or if you're comfortable relying on self-reported type ([paper](https://arxiv.org/html/2402.18545)).

## Known, not confirmed
- **UNICAMP "Black skin lesions"** ([Zenodo 10570316](https://zenodo.org/records/10570316)) is acral lesions (palms, soles, nails) assessed against the Fitzpatrick scale. It's available on request with an institutional email, CC BY-NC-SA 4.0. I couldn't confirm the image count or the skin type spread.

## Not recommended, and why
- **MRA-MIDAS:** only about 2 type VI patients out of 796 ([NEJM AI](https://ai.nejm.org/doi/full/10.1056/AIdbp2400732)).
- **DDI-2:** patients who self-identified as Asian; a recent preprint reports no type V–VI cancers in it.
- **PAD-UFES-20:** has Fitzpatrick labels, but nearly all are types I–III.
- **HAM10000 and ISIC:** no consistent per-image skin type, and overwhelmingly light skin.
- **SkinCAP:** a captioned subset of Fitzpatrick17k and DDI, so no new images.

## What I could not find
No public skin-cancer dataset has many **biopsy-confirmed cancers on type V–VI skin**; DDI's 48 is the most. Darker-skin coverage elsewhere is mostly inflammatory and infectious conditions. The registry searches turned up mostly noise; the useful finds came from the literature and the web.

## Next step
For the audit, I'd use DDI as the biopsy-confirmed core, Fitzpatrick17k for statistical power across all six types, and PASSION and DermaCon-IN as external tests on darker skin. Add SCIN if you want the Monk scale. You can start on DermaCon-IN, SCIN and the Fitzpatrick17k labels today, and send the DDI and PASSION requests now.

Everything is in an interactive page you can filter and compare: `/private/tmp/e-do23Oy/home/cwd/dataset-shortlist.html`

Sources: [PASSION](https://passionderm.github.io/), [PASSION paper](https://arxiv.org/html/2411.04584v1), [DermaCon-IN paper](https://arxiv.org/html/2506.06099), [SCIN repo](https://github.com/google-research-datasets/scin), [SCIN paper](https://arxiv.org/html/2402.18545), [DDI](https://aimi.stanford.edu/datasets/ddi-diverse-dermatology-images), [DDI-2](https://github.com/DaneshjouLab/ddi2-dataset), [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k), [MIDAS](https://www.medrxiv.org/content/10.1101/2024.06.27.24309562v1.full), [Global Atlas of Digital Dermatology](https://arxiv.org/html/2601.00840)