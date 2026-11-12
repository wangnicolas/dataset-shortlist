**Start with `mwalmsley/gz2` on Hugging Face.** It's the best fit for your constraints: images and human labels in one place, well over 40k galaxies, and no scripting needed to join them.

## Recommended

**1. Galaxy Zoo 2 (`mwalmsley/gz2`)**
- I confirmed the page exists. The default subset has about 191k rows (172k train, 18.8k test) at 424×424 px, and there is a 1.9k-row "tiny" subset for testing code.
- The labels are volunteer vote counts, with derived fraction columns and total votes per question. The questions cover smooth vs featured, bar, spiral arms and winding, bulge size, edge-on, mergers and more. I only saw a truncated column list, so check the full schema.
- It's in Parquet, so the `datasets` library should load it. The page showed no code, so check the dataset card for the exact call.
- The license is **CC BY-NC-SA 4.0**, which is fine for a thesis but not for commercial use.
- The images are SDSS, and the labels are the Galaxy Zoo 2 project's decision tree (11 tasks, 37 answers).

**2. Galaxy Zoo Evo (`mwalmsley/gz_evo`)**
- I confirmed it exists. It's a combined set of about 823k images and 104M volunteer labels from four telescopes.
- The paper is [arXiv 2512.23691](https://arxiv.org/abs/2512.23691), and the code is at github.com/mwalmsley/gz-evo.
- The license is also CC BY-NC-SA 4.0.
- The page was truncated, so I could not confirm its columns or whether access is gated.
- The collection also lists per-campaign sets (`gz_desi`, `gz_ukidss`, `gz_candels`, `gz_hubble`, `gz_euclid` and others). I did not open those individually. Use these if you want DESI-quality imaging or a specific survey.

**3. Kaggle "Galaxy Zoo – The Galaxy Challenge"** ([data page](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data))
- This is the classic benchmark: 61,578 training JPGs at 424×424, with 37 columns of vote-derived probabilities from Galaxy Zoo 2.
- It's about 60k labelled galaxies, so it clears your 40k bar. The test set (79,975 images) has no public labels.
- The labels are transformed (cumulative, re-weighted), not raw votes. They are still human-derived.
- You need a Kaggle account and have to accept the competition rules. I did not check the license terms.

## Be careful with these

- **Galaxy Zoo DESI on Zenodo** ([record 8331338](https://zenodo.org/records/8331338)) is a catalogue only, with no images.
  - The big files (`gz_desi_deep_learning_catalog_*`) are **model predictions**, so they fail your human-labels requirement.
  - The human votes are in `gz_desi_gzd8_volunteer_core_catalog.parquet` and `gz_desi_gzd8_volunteer_extended_catalog.parquet`. They cover about 96k galaxies, and the license is CC BY 4.0. You would have to fetch the images separately from the DESI Legacy Surveys.
- **Galaxy Zoo DECaLS volunteer catalogues** ([Zenodo, doi 10.5281/zenodo.4196266](https://doi.org/10.5281/zenodo.4196266)) have human votes only, and the images are not bundled. The `gz_decals_volunteers_ab` file covers about 93k galaxies. The same record also carries deep-learning catalogues, so pick the files carefully.
- **Galaxy10 DECaLS** ([Zenodo 10845026](https://zenodo.org/records/10845026)) is bundled, but it has only 17,736 images and 10 coarse classes. It is too small for your 40k target and has no bar, bulge or merger detail.
- **GalaxyMNIST** has 10,000 images and 4 classes, so it is also too small.

## What I'd do

Use `gz2` as your main training set. Filter on the `_total-votes` columns, for example keeping galaxies with at least 20 or so votes on a given question. Then threshold the vote fractions (Willett et al. 2013 used thresholds like this) for the binary or multi-class targets you want. Treat the `gz_evo` per-survey sets as a second domain for testing how well your model generalises.

Raw vote data is noisy. For bars and mergers especially, plan to either train on the fractions directly or use confidence cuts.

Sources:
- [Galaxy Zoo DESI paper (MNRAS)](https://academic.oup.com/mnras/article/526/3/4768/7283169)
- [Galaxy Zoo DESI on Zenodo](https://zenodo.org/records/8331338)
- [Galaxy Zoo Data](https://data.galaxyzoo.org/)
- [Galaxy10 DECaLS on Zenodo](https://zenodo.org/records/10845026)
- [astroNN Galaxy10 docs](https://astronn.readthedocs.io/en/latest/galaxy10.html)
- [Kaggle Galaxy Zoo challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data)
- [Galaxy Zoo Evo paper](https://arxiv.org/abs/2512.23691)
- [HF `mwalmsley/gz_evo`](https://huggingface.co/datasets/mwalmsley/gz_evo)
- [HF `mwalmsley/gz2`](https://huggingface.co/datasets/mwalmsley/gz2)
- [HF Galaxy Zoo Evo collection](https://huggingface.co/collections/mwalmsley/galaxy-zoo-evo)
- [GalaxyMNIST](https://github.com/mwalmsley/galaxy_mnist)