Download **Galaxy Zoo Evo** (`mwalmsley/gz_evo` on Hugging Face) if you want images and labels in one package, or the **Galaxy Zoo DECaLS** Zenodo record if you want a plain CC-BY licence. Both are open today and carry volunteer vote counts for bars, spiral arms, bulge size and mergers. Everything below was checked on 2026-11-12 unless marked "from memory".

## What I assumed you need
- **R1** galaxy images usable for CNN training (must)
- **R2** detailed labels: bars, spiral arms, bulge size, mergers (must)
- **R3** at least 40,000 labelled galaxies (must)
- **R4** labels from humans, not model predictions (must)
- **R5** free and downloadable now (must)
- **R6** images bundled with the labels (nice to have)
- I assumed non-commercial academic use and that you can publish your code.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [Galaxy Zoo Evo](https://huggingface.co/datasets/mwalmsley/gz_evo) (HF) | Direct download, minutes | CC-BY-NC-SA-4.0 + code-release clause | 805,979 images, 18 GB | Strong | today |
| 2 | [GZ DESI volunteer subset](https://huggingface.co/datasets/mwalmsley/gz_desi) (HF) | Direct download | same as #1 | 399,413 images, 17.5 GB | Strong | today |
| 3 | [Galaxy Zoo DECaLS](https://zenodo.org/records/4573248) (Zenodo) | Direct download | CC-BY-4.0 | 314,000 galaxies, 104 GB of images | Strong | today |
| 4 | [Galaxy Zoo 2 images](https://zenodo.org/records/3565489) (Zenodo) + tables at [data.galaxyzoo.org](https://data.galaxyzoo.org/) | Direct download | CC-BY-4.0 (images) | 243,434 images, 3.4 GB | Strong; mergers weak | today |
| 5 | [Galaxy Zoo 2](https://huggingface.co/datasets/mwalmsley/gz2) (HF) | Direct download | same as #1 | 191,174 images, 2.7 GB | Strong; no merger column | today |
| 6 | [Galaxy Zoo UKIDSS](https://zenodo.org/records/13357341) (Zenodo) | Direct download | CC-BY-4.0 | 71,052 galaxies, 7.9 GB | Strong; near-infrared | today |
| 7 | [Galaxy Zoo Hubble](https://huggingface.co/datasets/mwalmsley/gz_hubble) (HF) | Direct download | same as #1 | 96,449 images | Partial | today |
| 8 | [Galaxy Zoo Cosmic Dawn](https://zenodo.org/records/17200992) (Zenodo) | Direct download | CC-BY-4.0 | about 45,700 images, 5 GB | Partial | today |
| 9 | [Galaxy Zoo CANDELS](https://huggingface.co/datasets/mwalmsley/gz_candels) (HF) | Direct download | same as #1 | 48,098 images | Partial | today |

## Details
**1. Galaxy Zoo Evo.**
- **Contents:** all Galaxy Zoo campaigns combined, with the image and the volunteer vote counts in the same row (for example `bar-gz2_yes`, `bulge-size-gz2_dominant`, `merging-dr12_tidal-debris`).
- **Access:** `pip install datasets`, then `load_dataset('mwalmsley/gz_evo', split='train')`. The card suggests logging in with a free Hugging Face account, but the dataset is not gated. A `tiny` config (6.6k images) exists for prototyping.
- **Licence:** non-commercial, share-alike, and the card requires "all models trained on these datasets to be released as source code by publication".
- **Catch:** each galaxy only has votes for its own campaign's questions, so the other columns are empty. Filter on the total-votes columns.

**2. GZ DESI volunteer subset.** This is the DECaLS/Legacy Survey part of #1 on its own, with 319,530 train and 79,883 test images. It has an explicit merging question. Access and licence are as for #1. Many galaxies from the fifth campaign have only about five votes.

**3. Galaxy Zoo DECaLS (Zenodo).**
- **Contents:** the official release, with the PNGs shown to volunteers in four zips.
- **Use only** `gz_decals_volunteers_1_and_2` and `gz_decals_volunteers_5`. The file `gz_decals_auto_posteriors` is model output and breaks your human-label rule.
- **Access:** download the catalogues and image zips, then join on `iauname`. Not every image has volunteer labels.
- **Paper:** [Walmsley et al. 2021, MNRAS](https://doi.org/10.1093/mnras/stab2093).

**4. Galaxy Zoo 2 (Zenodo).**
- **Contents:** the classic SDSS benchmark; bars, arm count and winding, and bulge size are all questions in the tree.
- **Access:** download `images_gz2.zip` and `gz2_filename_mapping.csv`, then get "GZ2 - Table 1 - Normal-depth sample with new debiasing method" from data.galaxyzoo.org.
- **Catch:** merger is only an answer under the "odd feature" question (from memory). The separate Zenodo record for the tables (3566991) has restricted files, so use data.galaxyzoo.org.
- **Paper:** [Willett et al. 2013](https://doi.org/10.1093/mnras/stt1458).

**5. Galaxy Zoo 2 (HF).** The same survey as #4, already joined. This packaging has no merger column.

**6. Galaxy Zoo UKIDSS.** Uses the same question tree as GZ2, with volunteer vote counts and 70,845 JPGs in the same record. The imaging is near-infrared and the galaxies overlap with GZ2.

**7–9. Hubble, Cosmic Dawn, CANDELS.** All have volunteer votes and bundled images, but the galaxies are distant, so bars and arms are harder to see.
- **Hubble:** no merger column in this packaging.
- **Cosmic Dawn:** exclude the `gzcd_zoobot_*` files, which are predictions. I did not read its question tree.
- **CANDELS:** has merger and tidal-debris votes.

## Known, not confirmed
- **[Galaxy Zoo Euclid](https://huggingface.co/datasets/mwalmsley/gz_euclid) (HF):** exists, is not gated, and has 172,277 rows with vote columns including merging. The card is empty, no licence is stated, and the download is only 0.3 GB, so I could not confirm that full images are included or that the labels are volunteer votes. Check the viewer and ask the author before relying on it.
- **[Kaggle Galaxy Zoo challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge):** the page exists but the tool could not read it. From memory: 61,578 training JPGs with 37 GZ2 vote fractions, behind a free Kaggle account and acceptance of the competition rules. It is a subset of GZ2, so #4 or #5 is the better choice.

## Not recommended, and why
- **[Galaxy Zoo DESI 8.7M catalogue](https://zenodo.org/records/8360385):** labels are predicted vote fractions from a model. Its volunteer-labelled part is #2.
- **[Euclid Q1 morphology catalogue](https://zenodo.org/records/15106473):** "measurements were made by Zoobot foundation models".
- **[Galaxy10 DECaLS](https://zenodo.org/records/10845026):** about 17.7k images in 10 coarse classes (size from memory).
- **[Galaxy Zoo 1](https://doi.org/10.6084/m9.figshare.90206.v1):** only elliptical / spiral / merger, and no images.
- **[Nair & Abraham 2010](https://doi.org/10.1088/0067-0049/186/2/427):** expert labels but only 14,034 galaxies and no bundled images. It could serve as an independent test set.
- **Third-party re-uploads on Hugging Face and Kaggle:** provenance and licence are unclear.

## What I could not find
- No expert-labelled set above 40k galaxies with detailed features turned up. At this scale the human labels are volunteer votes.
- The paper search indexes astronomy poorly, so I only have the describing papers as evidence of use. CDS/VizieR was not searched.

## Next step
Load the `tiny` config of `gz_evo` or `gz_desi` to get your pipeline running. Then choose between #2 (convenient, but you must release your model code) and #3 (CC-BY, but a 104 GB download and a manual join).

The interactive comparison page is at `/private/tmp/e-ZPkd3O/home/cwd/dataset-shortlist.html`.