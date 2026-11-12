**Download Galaxy Zoo 2 (GZ2) as your main dataset.** It meets every requirement: about 191k SDSS galaxies in the bundled version, labels that are purely volunteer votes, and images packaged with the labels.

I checked the sources below online today but did not download anything.

## Primary: Galaxy Zoo 2

- **Hugging Face `mwalmsley/gz2`** is the easiest route: about 191k galaxies (172k train / 18.8k test) as 424×424 images with per-question vote counts and fractions in the same parquet files. It should load with `datasets.load_dataset("mwalmsley/gz2")`, though I did not run this. The licence is CC-BY-NC-SA 4.0, which is fine for a thesis.
- **Labels:** the GZ2 decision tree covers smooth/featured, edge-on, bar, spiral arms (winding and arm count), bulge prominence, roundedness, and "odd features" (ring, lens, disturbed, irregular, merger, dust lane). The Hugging Face page preview was truncated, so I only saw the first few columns; the rest is from my knowledge of GZ2.
- **Manual alternative:** images from [Zenodo 3565489](https://zenodo.org/records/3565489) (243,434 JPGs, 3.4 GB, CC-BY 4.0, with a filename-mapping CSV) plus the Hart et al. (2016) vote table from [data.galaxyzoo.org](https://data.galaxyzoo.org/) (239,695 galaxies). That table is the one the Galaxy Zoo team recommends.

## If you want deeper images: Galaxy Zoo DECaLS

DECaLS imaging shows faint bars, arms and tidal features better than SDSS, and it has a dedicated merger question (none / minor disturbance / major disturbance / merger).

- **[Zenodo 4573248](https://zenodo.org/records/4573248)** (CC-BY 4.0) has the PNG images in four zips totalling about 104 GB, plus the volunteer tables.
- **Use only** `gz_decals_volunteers_5.parquet` (GZD-5, about 230k galaxies) and optionally `gz_decals_volunteers_1_and_2.parquet`.
- **Do not use** `gz_decals_auto_posteriors.*` in the same record: those are CNN predictions, which you have ruled out.
- **Easier download:** `pip install galaxy-datasets`, then `from galaxy_datasets import gz_decals_5` with `download=True` fetches images and the volunteer catalogue together. The same package also offers `gz2`, `gz_hubble` and `gz_candels`.

## What to avoid

- **Galaxy Zoo DESI (8.7M galaxies):** the headline catalogue is model predictions.
- **Galaxy10 DECaLS:** human-labelled but only about 18k galaxies and 10 coarse classes (figure from memory).

## Practical points for the thesis

- **Vote counts vary.** Questions deeper in the tree (bar, arm count) are only answered by volunteers who said "featured, not edge-on", so filter on the number of votes for each question before trusting a fraction.
- **Raw versus debiased.** The Hart table gives both raw and redshift-debiased fractions. Train on the raw ones, since they describe what is visible in the image; the debiased ones are for population statistics.
- **Loss function.** The standard approach is to predict vote counts with a Dirichlet-multinomial loss (Walmsley et al. 2022, the `zoobot` package), which handles the varying vote counts properly.