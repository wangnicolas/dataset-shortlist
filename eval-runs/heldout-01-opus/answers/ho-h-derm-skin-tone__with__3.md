Four public datasets clearly meet all three of your requirements (skin tone label, diagnosis label, real numbers of type V and VI): **DermaCon-IN, Fitzpatrick17k, PASSION and DDI**. **SCIN** works for type V but has very little type VI. All checks were done on 2026-11-12.

I counted the images per skin type myself from the released label files for DermaCon-IN, Fitzpatrick17k and SCIN. PASSION's numbers come from its paper. DDI's numbers are from memory.

## What I assumed you need
- **Must have:** a Fitzpatrick (FST) or Monk (MST) label on every image or patient; a diagnosis label; V and VI in the hundreds, not a handful; clinical or dermoscopy images, any disease.
- **Nice to have:** lighter types (I–II) in the same dataset so you can compare within it; available without an institutional agreement.
- **Assumption:** this is academic, non-commercial use. Nearly every candidate requires that.

## Shortlist
| # | Dataset | Access | Licence | Size | V / VI images | Checked |
|---|---|---|---|---|---|---|
| 1 | **DermaCon-IN** (South India) | Direct download | CC BY-NC-SA 4.0 | 5,450 images / 3,002 patients | **1,285 / 136**; MST 8–9: 375 | Today, counted |
| 2 | **Fitzpatrick17k** | Labels on GitHub; images fetched from URLs | CC BY-NC-SA 3.0 (labels) | 16,577 images, 114 conditions | **1,533 / 635** | Today, counted |
| 3 | **PASSION** (sub-Saharan Africa, mostly children) | Request form, probably a few days | PASSION licence, non-commercial | 4,901 images / 1,653 patients | Test set alone: **341 / 88** | Today, from the paper |
| 4 | **DDI** (Stanford, biopsy-proven) | Free registration and click-through agreement | Stanford research use, non-commercial | 656 images / 570 patients | About 207 in a combined V–VI group | Access today; counts from memory |
| 5 | **SCIN** (Google, US consumer photos) | Direct download, no login | SCIN Data Use License | 10,408 images / 5,033 cases | 468 / **42** images | Today, counted |

## Details
**1. DermaCon-IN** – https://doi.org/10.7910/DVN/W7OUZM
- **Contents:** Every image has a dermatologist-rated Fitzpatrick type and Monk tone, plus 245 fine-grained diagnoses (88 main classes). Body site and lesion descriptors are also included.
- **Type counts:** III 1,403, IV 2,620, V 1,285, VI 136.
- **Gap:** there are no type I–II images, so for a light-versus-dark comparison you need to pair it with a dataset that has them.
- **Access:** the dataset API shows all files unrestricted. Download the two image zips (about 3.6 GB) plus `Skin_Metadata.tab` and the train/test split files. Takes minutes.
- **Paper:** [arXiv 2506.06099](https://arxiv.org/abs/2506.06099).

**2. Fitzpatrick17k** – https://github.com/mattgroh/fitzpatrick17k
- **Contents:** all six types are covered (I 2,947 · II 4,808 · III 3,308 · IV 2,781 · V 1,533 · VI 635 · unknown 565). This is the most type VI images of any dataset here.
- **Caveats:**
  - Skin types were assigned by crowd annotators looking at the image.
  - The diagnosis labels are known to be noisy. The CleanPatrick dataset on Hugging Face flags problem images.
  - Images are hotlinks to two online atlases, so some links may be dead.
- **Papers:** [Groh et al., CVPRW 2021](https://doi.org/10.1109/cvprw53098.2021.00201) and [the skin-tone annotation reliability study](https://doi.org/10.1145/3555634).

**3. PASSION** – https://passionderm.github.io/
- **Contents:** FST III–VI only, from Madagascar, Guinea, Malawi and Tanzania. Four diagnosis groups (eczema, fungal, scabies, impetigo/other), ICD-coded by local dermatologists.
- **Type counts:** the paper only gives the held-out test set (III 303, IV 254, V 341, VI 88). By the 80/20 split the full dataset should have roughly 1,700 V and 440 VI, but that is my estimate.
- **Access:** submit the Google Form and accept the licence: no commercial use, and you may not repost the data or share the direct download link.
- **Paper:** [MICCAI 2024](https://papers.miccai.org/miccai-2024/590-Paper3722.html).

**4. DDI** – https://ddi-dataset.github.io/
- **Contents:** biopsy-confirmed, which makes it the cleanest ground truth here. Designed to be balanced across three skin-tone groups. From memory, the labels are those groups (I–II, III–IV, V–VI), so you can't separate V from VI.
- **Caveat:** it is small, so results per diagnosis will be uncertain.
- **Access:** register on Stanford AIMI and accept the Research Use Agreement. Each person on your team has to register separately.
- **Papers:** [Daneshjou et al., Science Advances 2022](https://doi.org/10.1126/sciadv.abq6147) and a [2026 audit of large language models by skin tone on DDI](https://doi.org/10.1111/ijd.70452).

**5. SCIN** – https://github.com/google-research-datasets/scin
- **Labels:** self-reported FST, FST estimated by up to three dermatologists, and two sets of Monk labels from trained laypeople.
- **Coverage gap:** only 3,061 cases have a dermatologist diagnosis (a weighted differential, not biopsy-confirmed). Among those, by the first dermatologist's skin-type estimate: V 229 cases / 468 images, VI 27 cases / 42 images. Monk 8 and above on the US labels: 30 cases.
- **Fit:** good for type V and for common inflammatory conditions. Not enough for type VI.

## Known, not confirmed
- **Zenodo 10570316, "Black skin lesions"** (UNICAMP): restricted acral melanoma images, 43.7 GB. The description mentions the Fitzpatrick scale, but I could not confirm that every image has a label or how many there are. To ask for access, log in to Zenodo and send a request from an institutional email.
- **DDI-2:** 665 biopsy-proven images from Asian patients at Stanford, with Fitzpatrick type taken from clinical notes. I did not count V/VI and they are probably few. Access is through a Stanford research-use agreement (https://doi.org/10.57761/pgwn-6b62).

## Not recommended, and why
- **PAD-UFES-20:** open and labelled, but almost entirely types I–III (from memory).
- **MILK10k and MRA-MIDAS:** both have a skin-tone field but come from mostly light-skinned skin-cancer populations (from memory).
- **HAM10000, ISIC, BCN20000, DermNet:** most images have no skin-tone label.
- **SkinCAP, CleanPatrick, FitzDerm-CF, Fitz Selected:** derived from Fitzpatrick17k and DDI, so they add no new dark-skin images.
- **Monk Skin Tone Examples:** no diagnoses.
- **electricsheepafrica/skin-diseases-dermatology:** simulated table data, not images.

## What I could not find
- No public **dermoscopy** dataset with substantial type V–VI.
- No dataset that combines hundreds of type VI images, a broad range of diagnoses and biopsy confirmation.
- Nothing licensed for commercial use.

## Next step
Download DermaCon-IN and Fitzpatrick17k today (both open) and request PASSION in parallel. A sensible audit design:
- Fitzpatrick17k for comparisons across all six types.
- DermaCon-IN and PASSION as large dark-skin test sets from outside the training sources.
- DDI as the biopsy-confirmed check.
- Report type VI with confidence intervals, because it is the thinnest group everywhere.

The interactive shortlist is at `/private/tmp/e-yCCFF8/home/cwd/dataset-shortlist.html`.

Sources: [PASSION arXiv](https://arxiv.org/html/2411.04584v1), [DermaCon-IN arXiv](https://arxiv.org/html/2506.06099), [DDI-2 GitHub](https://github.com/DaneshjouLab/ddi2-dataset), [SCIN GitHub](https://github.com/google-research-datasets/scin), [SCIN JAMA Netw Open](https://jamanetwork.com/journals/jamanetworkopen/articlepdf/2826506/ward_2024_oi_241322_1731448364.35384.pdf), [Stanford AIMI DDI](https://aimi.stanford.edu/datasets/ddi-diverse-dermatology-images)