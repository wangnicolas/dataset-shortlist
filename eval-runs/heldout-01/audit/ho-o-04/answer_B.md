## What I assumed you need

- **R1 (must):** at least 40k galaxies.
- **R2 (must):** detailed morphology: bars, spiral arms, bulge size, mergers.
- **R3 (must):** labels from human votes, not model predictions.
- **R4 (nice to have):** images bundled with the labels.
- I assumed a free, direct download and that you'll train on the vote counts or fractions yourself.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Galaxy Zoo 2 (SDSS) images + volunteer table | Open download, minutes | Images CC-BY-4.0. Table terms not checked | 243,434 images (3.35 GB) | Strong | Images: today. Table: today (site text) |
| 2 | Galaxy Zoo DECaLS | Open download, days (~104 GB of images) | CC-BY-4.0 | 314k galaxies in total. Volunteer-labelled subset not counted | Strong | today |
| 3 | Galaxy Zoo UKIDSS (near-infrared) | Open download, minutes | CC-BY-4.0 | 71,052 galaxies (7.9 GB images) | Partial | today |

## Details

**1. Galaxy Zoo 2**
- **Links:** [images (Zenodo)](https://zenodo.org/records/3565489) and [labels (data.galaxyzoo.org)](https://data.galaxyzoo.org).
- **Contents:** the images come with `gz2_filename_mapping.csv`. The labels are volunteer votes from the GZ2 decision tree, covering bars, spiral arms, bulge prominence and mergers/odd features. They come from 16M classifications. Use the debiased Table 1 (Hart et al. 2016).
- **Why it's first:** it clears 40k comfortably, the labels are human, and the images are lower-resolution SDSS cutouts, a common setting for CNN work.
- **Caveat:** images and labels are two downloads that you join with the mapping file.
- **Zenodo catalogue:** a separate Zenodo copy of the GZ2 catalogue ([record 3566991](https://zenodo.org/records/3566991)) is flagged "restricted". I didn't resolve that. Use data.galaxyzoo.org instead.

**2. Galaxy Zoo DECaLS** ([Zenodo](https://zenodo.org/records/4573248))
- **Contents:** the record has volunteer-vote files for the GZD-1/2 and GZD-5 campaigns and a `schema.md`. It also has four DR5 PNG image zips, about 104 GB in total. The newer question schema targets mergers and weak bars. Images are higher quality than SDSS.
- **Caveat 1:** the file `gz_decals_auto_posteriors` is *model predictions*. Don't use it as labels. Use only the `gz_decals_volunteers_*` files.
- **Caveat 2:** many GZD-5 galaxies have only about 5 votes, so filter by vote count.
- **Caveat 3:** the record doesn't say how many galaxies have volunteer votes. Count the rows before relying on 40k.

**3. Galaxy Zoo UKIDSS** ([Zenodo](https://zenodo.org/records/13357341))
- **Contents:** catalogue and images in one record. The catalogue has vote counts and fractions (images are in `ukidss_images.zip`, 7.9 GB).
- **Caveat:** it's near-infrared, so it's less useful as a main training set. It works as a second domain to compare against.

## Known, not confirmed

- **Galaxy Zoo Hubble and CANDELS:** both are listed on data.galaxyzoo.org and have volunteer votes, but I didn't check sizes or whether images are bundled.
- **Euclid Q1 visual morphology catalogue** ([Zenodo](https://zenodo.org/records/15106473)): I didn't check whether its labels are human or model-derived, or its size.
- **Hugging Face copies** of GZ2 (for example `juliensimon/galaxy-zoo-2-morphology`): they show up as open, but I didn't check which columns they carry. They may be easier to load than the Zenodo zip.

## Not recommended, and why

- **Galaxy Zoo DESI (8.7M):** this is the famous one, but its main catalogue is deep-learning predicted vote fractions, which fails R3. The only human votes in it are about 96k galaxies from the GZD-8 campaign, and the images aren't bundled.
- **Galaxy10 DECaLS:** about 17.7k images (from memory), which is below your 40k, and only 10 coarse classes.
- **Galaxy MNIST:** about 10k images (from memory) and 4 coarse classes. Too small.

## What I could not find

The literature search returned almost nothing relevant, so I found no lesser-known alternatives. The ranking comes from registry searches and the Galaxy Zoo data portal.

## Next step

Download the GZ2 images and Table 1 and join them with the mapping file. Then decide whether the DECaLS vote count is enough to add a second, sharper-image set. This check was done on 2026-11-12, and access terms and versions can change.

