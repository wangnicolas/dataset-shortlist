Download **`mwalmsley/gz_desi`** from Hugging Face: about 399k galaxies, images bundled with volunteer vote counts, and separate strong-bar, weak-bar and graded-merger labels. If you want something smaller to start with, `mwalmsley/gz2` (191k SDSS galaxies, 2.6 GB) has the same format. Everything below was checked on 2026-11-12 unless marked "from memory".

## What I assumed you need
- **R1 (must):** at least 40,000 galaxies.
- **R2 (must):** labels from humans (volunteer votes or experts), not model output.
- **R3 (must):** detailed features: bars, spiral arms, bulge size, mergers.
- **R4 (nice):** images bundled with the labels.
- **R5 (must):** free and downloadable now. I assumed non-commercial thesis use and that you can publish your code.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | GZ DESI (`mwalmsley/gz_desi`) | Open download; card asks for a free HF login | CC BY-NC-SA 4.0 + release your model code | 399,413 images, 17.5 GB | Strong | today |
| 2 | Galaxy Zoo 2 (`mwalmsley/gz2`) | Same | Same | 191,174 images, 2.6 GB | Strong | today |
| 3 | GZ Evo (`mwalmsley/gz_evo`) | Same | Same | 805,979 images, 18 GB | Strong | today |
| 4 | Galaxy Zoo DECaLS (Zenodo) | Direct download | CC BY 4.0 | 314k galaxies, 108 GB | Strong | today |
| 5 | Galaxy Zoo 2 images (Zenodo) + vote table | Direct download, two sources | CC BY 4.0 (images) | 243,434 images, 3.4 GB | Strong | today |
| 6 | GZ Euclid (`mwalmsley/gz_euclid`) | Open download | None stated | 172,277 images, 0.5 GB | Partial | today |
| 7 | Galaxy Zoo UKIDSS (Zenodo) | Direct download | CC BY 4.0 | 71,052 galaxies, 7.9 GB | Partial | today |
| 8 | GZ Hubble (`mwalmsley/gz_hubble`) | Open download; HF login | CC BY-NC-SA 4.0 + code release | 96,449 images, 6.4 GB | Partial | today |
| 9 | Galaxy Zoo Cosmic Dawn (Zenodo) | Direct download | CC BY 4.0 | about 45.7k images, 5.1 GB | Partial | today |
| 10 | Kaggle Galaxy Zoo challenge | Free account + accept rules | Competition rules | 61,578 training images | Partial | page exists today; terms and size from memory |

## Details

**1. GZ DESI** — https://huggingface.co/datasets/mwalmsley/gz_desi
- **Contents:** 424×424 images plus one column per answer; the card says "The values are the count of volunteers who selected each answer."
- **Why it fits:** columns include `bar-dr5_strong/weak/no`, `merging-dr5_merger/major-disturbance/minor-disturbance/none`, bulge size, spiral arm count and winding.
- **Access:** `pip install datasets`, then `load_dataset('mwalmsley/gz_desi', split='train')`. Try `name='tiny'` first.
- **Catches:** there are three campaigns (dr12, dr5, dr8) with slightly different questions. Many DR5/DR8 galaxies have only about five votes, so filter on the `*_total-votes` columns.
- **Licence:** non-commercial, share-alike, and the card requires "all models trained on these datasets to be released as source code by publication".

**2. Galaxy Zoo 2** — https://huggingface.co/datasets/mwalmsley/gz2
- **Contents:** SDSS images with vote counts for bar (yes/no), bulge size (four levels), spiral arm count and winding.
- **Catches:** bars are yes/no only, and mergers sit under the "odd feature" question (from memory). It is the most heavily used set in this field.
- **Paper:** Willett et al. 2013, https://doi.org/10.1093/mnras/stt1458.

**3. GZ Evo** — https://huggingface.co/datasets/mwalmsley/gz_evo
- **Contents:** GZ2, DESI, CANDELS, Hubble and UKIDSS combined and pre-shuffled.
- **Catch:** each galaxy only has votes for its own campaign's questions, so you need a masked or multi-head loss. This is more than a master's thesis usually needs.

**4. Galaxy Zoo DECaLS** — https://zenodo.org/records/4573248
- **Why consider it:** this is the original release behind most of #1, under plain CC BY 4.0 with no code-release condition.
- **Access:** download `gz_decals_volunteers_5.parquet`, `gz_decals_volunteers_1_and_2.parquet` and the four PNG zips (21–33 GB each), then join on `iauname`.
- **Catch:** ignore `gz_decals_auto_posteriors.*`, which are model predictions. Not every image has volunteer labels.

**5. Galaxy Zoo 2 images** — https://zenodo.org/records/3565489
- **Access:** download `images_gz2.zip` and `gz2_filename_mapping.csv`. The labels are the "GZ2 – Table 1 – Normal-depth sample with new debiasing method" CSV at https://data.galaxyzoo.org/, joined through the mapping file.
- **Catch:** the licence of the tables on data.galaxyzoo.org was not stated on the page I read.

**6. GZ Euclid** — https://huggingface.co/datasets/mwalmsley/gz_euclid
- **Contents:** Euclid space-telescope cutouts with the newest schema: strong/weak bar, five bulge sizes, graded mergers, clumps.
- **Catches:** the card is empty and states no licence. The columns are vote counts and `total-votes`, which indicates volunteer labels, but nothing on the card confirms it. Ask the maintainer before relying on it.

**7. Galaxy Zoo UKIDSS** — https://zenodo.org/records/13357341
- **Contents:** near-infrared images of GZ2 galaxies; "The catalog contains volunteer vote counts", using the same question tree as GZ2.
- **Catch:** spiral structure is weaker in the infrared, and the galaxies overlap with GZ2.

**8. GZ Hubble** — https://huggingface.co/datasets/mwalmsley/gz_hubble
- **Contents:** HST galaxies with volunteer vote counts.
- **Catch:** these are distant, small, noisy galaxies; only useful if your thesis covers higher redshift.

**9. Galaxy Zoo Cosmic Dawn** — https://zenodo.org/records/17200992
- **Contents:** two image zips (15,745 + 29,997) plus `gzcd_volunteer_classifications.parquet`.
- **Catches:** skip the `gzcd_zoobot_*` files, which are predictions. It barely clears 40k, the galaxies are faint, and I did not inspect the question schema.

**10. Kaggle Galaxy Zoo challenge** — https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge
- **Contents (from memory):** 61,578 training JPGs with 37 GZ2 vote-fraction columns.
- **Access (from memory):** free account, then accept the competition rules.
- **Catch:** the IDs are anonymised and it is a subset of GZ2, so #2 or #5 is the better choice.

## Known, not confirmed
- **Kaggle terms and counts (#10):** the page exists but is drawn by JavaScript, so I could not read it. Check the Data and Rules tabs.
- **Galaxy Zoo GAMA-KiDS (about 49k, from memory):** I did not find a standalone release in the registries; look on data.galaxyzoo.org.
- **GZ CANDELS:** the Hugging Face copy (`mwalmsley/gz_candels`, 48,098 images) passed the existence check, but I did not check its fit beyond size; it is high-redshift HST imaging.

## Not recommended, and why
- **Galaxy Zoo DESI 8.7M catalogue** (https://zenodo.org/records/8360385): "created by training deep learning models on Galaxy Zoo volunteer responses". These are predictions with no images.
- **Euclid Q1 morphology catalogue** (https://zenodo.org/records/15106473): "measurements were made by Zoobot foundation models".
- **Galaxy10 DECaLS and Galaxy10 SDSS:** roughly 18k and 22k images in 10 coarse classes (sizes from memory), so too small and no per-feature labels.
- **Galaxy Zoo 1:** human votes, but only elliptical/spiral/merger and no images.
- **GZ2 catalogue record on Zenodo** (https://zenodo.org/records/3566991): "files are restricted"; use data.galaxyzoo.org instead.
- **`mwalmsley/gz_jwst_cosmos`:** gated and no licence stated.
- **Third-party Galaxy Zoo re-uploads on Hugging Face:** unverified provenance.

## What I could not find
- **Expert-labelled sets:** none with detailed features reaches 40k. The largest I know are Nair & Abraham 2010 (about 14k) and EFIGI (about 4.5k), both from memory. They could work as a small expert test set.
- **Recent CNN papers per release:** the paper search returned none tied to these specific releases (one index did not answer). The Willett paper above comes from the dataset card.
- **CDS/VizieR copies** of the catalogues were not checked.

## Next step
Run `load_dataset('mwalmsley/gz2', name='tiny')` to see the format, then move to `gz_desi` for the thesis. If the code-release condition or the non-commercial licence is a problem, use the Zenodo releases (#4 or #5) instead.

Interactive shortlist: `/private/tmp/e-1qtRfq/home/cwd/dataset-shortlist.html`