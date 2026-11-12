I'd start with **Galaxy Zoo 2 (GZ2)**. It has human-vote labels for bars, spiral arms, bulge size, mergers and more, the images are free to download, and it's far above your 40k minimum.

## Primary recommendation: Galaxy Zoo 2 (SDSS)
- **Size:** 243,434 images. The catalogue covers nearly 300k galaxies.
- **Labels:** volunteer votes only. The [Galaxy Zoo data page](https://data.galaxyzoo.org/) recommends the Hart et al. 2016 debiased table (`gz2_hart16.csv`). It covers bars, spiral arms, bulge size and mergers/odd features.
- **Images:** the [Zenodo record](https://zenodo.org/records/3565489) has `images_gz2.zip` (3.4 GB) and `gz2_filename_mapping.csv`. It is CC BY 4.0. There's also a [Kaggle mirror](https://www.kaggle.com/datasets/jaimetrickz/galaxy-zoo-2-images) of the same images.
- **Bundling:** the labels and images are separate downloads. You join them with the mapping file, which links the image `asset_id` to the SDSS `objid`. That's a short pandas merge.

## Better image quality: Galaxy Zoo DECaLS
- **Size:** about 314k galaxies, from deeper and sharper DESI Legacy Survey imaging than SDSS.
- **Labels:** the release includes the volunteer votes. It also includes deep-learning predictions, so use only the volunteer columns.
- **Images:** about 100 GB on Zenodo, at [doi.org/10.5281/zenodo.4196266](https://doi.org/10.5281/zenodo.4196266).
- **Source:** [Walmsley et al. 2022](https://academic.oup.com/mnras/article/509/3/3966/6378289).
- **Catch:** it's a much larger download, and I didn't open the Zenodo file listing, so check it before you commit disk space.

## Other volunteer-labelled sets
Each of these is listed on the [Galaxy Zoo data page](https://data.galaxyzoo.org/):
- **Galaxy Zoo: UKIDSS** has 71,052 galaxies in near-infrared imaging. The page says the catalogue and about 70,845 images are on Zenodo.
- **Galaxy Zoo: Cosmic Dawn** has over 41k Euclid Deep Field North galaxies, at [Zenodo](https://doi.org/10.5281/zenodo.17200992) (5.1 GB, images included). It mixes volunteer votes with Zoobot predictions, and this release is the newest. It's just above your threshold, and I'd treat it as a harder, higher-redshift extra rather than your main set.
- **Galaxy Zoo: Hubble** has 113,705 galaxies, and **CANDELS** has 49,555 at redshifts of about 1 to 3. I didn't verify that images are bundled for these.

## Avoid for your requirement
- **Galaxy Zoo DESI** (8.7M galaxies) and **Galaxy Zoo Euclid Q1** (378k) are labelled by deep-learning models trained on volunteer votes. The [GZ DESI paper](https://academic.oup.com/mnras/article/526/3/4768/7283169) says volunteer votes for part of the sample (GZD-8) are separate. The images aren't included (about 1 TB).
- **Galaxy10 DECaLS** ([Zenodo](https://zenodo.org/records/10845026)) is the one set that is truly bundled, with images and labels in one HDF5 file. But it has only 17,736 images, which is under 40k. It's good for quick prototyping.

## Caveats
- GZ2 labels are vote fractions, not hard classes. Choose and justify thresholds, for example a minimum vote count and a fraction cut-off. That's a methods choice your thesis should state.
- GZ2 images are 243k of the ~300k catalogue rows, so filter the table to the galaxies that have images.
- I didn't download any files. The sizes and record contents above come from the web pages I fetched.

Sources:
- [Galaxy Zoo Data](https://data.galaxyzoo.org/)
- [GZ2 images on Zenodo](https://zenodo.org/records/3565489)
- [GZ2 images on Kaggle](https://www.kaggle.com/datasets/jaimetrickz/galaxy-zoo-2-images)
- [GZ DECaLS paper](https://academic.oup.com/mnras/article/509/3/3966/6378289)
- [GZ DESI paper](https://academic.oup.com/mnras/article/526/3/4768/7283169)
- [GZ DESI on Zenodo](https://zenodo.org/records/8331338)
- [Galaxy10 DECaLS](https://zenodo.org/records/10845026)
- [Galaxy Zoo: Cosmic Dawn](https://arxiv.org/html/2509.22311)