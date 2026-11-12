Download **Galaxy Zoo DECaLS** from Zenodo, take the volunteer vote files plus the PNG images, and leave out the model-prediction file. If you want a second dataset to compare against, add **Galaxy Zoo 2** (SDSS images plus its volunteer vote table). Both are free downloads with no account, under CC BY 4.0, and each covers well over 40k galaxies. I checked everything below on 2026-11-12.

## What I assumed you need
- **Must have:**
  - galaxy images, ideally in the same release as the labels;
  - labels for bars, spiral arms, bulge size and mergers;
  - labels made by people, not a model;
  - at least 40k galaxies;
  - free to download now.
- **Nice to have:** a licence that lets you publish the work (CC BY is fine for a thesis).

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Galaxy Zoo DECaLS | open download | CC BY 4.0 | 314k galaxies (~230k in the latest phase), ~104 GB of PNGs | strong | today |
| 2 | Galaxy Zoo 2 images + Hart et al. 2016 vote table | open download | CC BY 4.0 | 243k images, labels for 240k galaxies, 3.4 GB | strong | today |
| 3 | `galaxy-datasets` Python package | `pip install` | code is GPL-3; data keeps each release's licence | GZ2 ~210k, DECaLS ~230k, Hubble ~106k, CANDELS ~50k | strong | today |
| 4 | Kaggle Galaxy Zoo Challenge | free Kaggle account and accepting the competition rules | rules not read | 61,578 images, 1.9 GB | strong | today |
| 5 | Galaxy Zoo UKIDSS (near-infrared) | open download | CC BY 4.0 | 71k galaxies, 7.9 GB | partial | today |
| 6 | Galaxy Zoo: Cosmic Dawn (high redshift) | open download | CC BY 4.0 | just over 41k galaxies, ~5 GB | partial | today |

## Details
**1. Galaxy Zoo DECaLS** – https://zenodo.org/records/4573248
- **Images:** four PNG zips (~104 GB total) of the images volunteers were shown.
- **Labels:** the volunteer votes are in `gz_decals_volunteers_5.parquet` (and `_1_and_2`).
- **Avoid:** `gz_decals_auto_posteriors`. Those are CNN predictions, which your rule excludes.
- **Why it's the best fit:** the imaging is deeper than SDSS, so weak bars, spiral arms and tidal features show up better. The questions were designed to pick up mergers and weak bars. The question list (strong/weak bar, number and winding of arms, bulge size, merging) is from my memory of the paper; `schema.md` lists the columns.
- **Caveat:** many galaxies got only about 5 votes, and about 140k got 30 or more. Weight or filter by vote count.
- **Paper:** Walmsley et al. 2022, MNRAS, [10.1093/mnras/stab2093](https://doi.org/10.1093/mnras/stab2093).

**2. Galaxy Zoo 2**
- **Images:** https://zenodo.org/records/3565489. It contains `images_gz2.zip` plus `gz2_filename_mapping.csv`, which links each image (`asset_id`) to its SDSS object ID (`objid`).
- **Labels:** https://gz2hart.s3.amazonaws.com/gz2_hart16.csv.gz (this link is listed on data.galaxyzoo.org).
- **Joining:** match the mapping file's `objid` to the vote table, and `asset_id` to the image file name. Drop mapping rows that have no image.
- **Caveats:** SDSS images are shallower, so weak bars and faint tidal features are missed more often. Mergers appear only as one answer under "odd features", not as their own question.

**3. `galaxy-datasets`** – https://github.com/mwalmsley/galaxy-datasets
- **What it does:** `gz2(root=..., download=True)` downloads the images and label tables together, ready for training. It also covers Galaxy Zoo Hubble and CANDELS, whose official releases have labels but no images.
- **Caveats:**
  - Its `gz_desi` and `gz_euclid` datasets are model predictions, so skip them.
  - The README says some datasets can only be downloaded internally, so check the one you want before relying on it.

**4. Kaggle Galaxy Challenge** – https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge
- **Contents:** 424×424 GZ2 images in one zip, with 37 columns of volunteer vote fractions.
- **Why use it:** it's the most common benchmark, so it's the easiest way to compare against published CNNs.
- **Caveats:**
  - Only the training set has labels.
  - The vote fractions are weighted down the question tree rather than raw counts.
  - The IDs are random, so you can't match galaxies back to SDSS.
  - I didn't read the rules page, so check the terms for using the data after the competition.
- **Paper:** Dieleman et al. 2015, MNRAS, [10.1093/mnras/stv632](https://doi.org/10.1093/mnras/stv632).

**5. Galaxy Zoo UKIDSS** – https://zenodo.org/records/13357341
- 70,845 near-infrared JPGs plus volunteer votes, using the same questions as GZ2. Useful for a chapter on how your model handles a different wavelength band.

**6. Galaxy Zoo: Cosmic Dawn** – https://doi.org/10.5281/zenodo.17200992
- Volunteer votes plus images. It also includes separate Zoobot prediction files, which you should skip.
- The questions aren't listed on the record page; the notebook included in the record may describe them.
- It's barely over your 40k minimum, the galaxies are faint, and it's a 2026 release with little prior use.

## Known, not confirmed
- **Galaxy Zoo Hubble (113,705 galaxies) and CANDELS (49,555):** the volunteer vote tables are on data.galaxyzoo.org, but there is no image download there. The only image source I found is `galaxy-datasets`, and I didn't confirm that those downloads are public.

## Not recommended, and why
- **Galaxy Zoo DESI (8.7M galaxies) and the Euclid Q1 catalogue:** their labels are Zoobot model predictions. The human votes behind DESI are the DECaLS ones in #1.
- **Galaxy10 SDSS / DECaLS:** about 22k and 18k galaxies in 10 broad classes (sizes from memory). Too small and too coarse.
- **Nair & Abraham 2010:** 14,034 galaxies labelled by experts. Too small to train on, but a strong expert test set for checking your model's bar calls.
- **EFIGI:** about 4.5k galaxies (from memory). Far too small.
- **Galaxy Zoo 1:** only elliptical, spiral or merger. No bars, arms or bulge.
- **Hugging Face re-uploads of GZ2:** label tables only, no images. Use the official releases.

## What I could not find
No set of 40k or more galaxies labelled by experts exists; the expert sets I found are all under 15k. Zenodo's API kept failing to respond, so I read the file lists from the record pages instead.

## Next step
Get `gz_decals_volunteers_5.parquet` and `schema.md` from the DECaLS record now; they're small. Start the image download, and while it runs, prototype on Galaxy Zoo 2 (3.4 GB). Later, you could use the Nair & Abraham catalogue as an expert-labelled test set.

The interactive shortlist is at `/private/tmp/e-KrIpti/home/cwd/dataset-shortlist.html`.

Sources: [Kaggle data page](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data), [data.galaxyzoo.org](https://data.galaxyzoo.org/), [galaxy-datasets](https://github.com/mwalmsley/galaxy-datasets), and the Zenodo records linked above.