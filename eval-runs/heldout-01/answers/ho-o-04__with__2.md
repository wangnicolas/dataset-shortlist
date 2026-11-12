## What I assumed you need

- **Labels (must):** human labels from volunteer votes or experts, not model predictions.
- **Morphology (must):** bars, spiral arms, bulge size and mergers, not just broad classes.
- **Size (must):** at least 40k human-labelled galaxies.
- **Cost (must):** free.
- **Images (nice to have):** images bundled with the labels.
- **Assumption:** you are fine joining a vote table to an image folder yourself.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Galaxy Zoo DECaLS (GZD-1/2/5 volunteer catalogues) | Open download, minutes to days (large files) | CC-BY-4.0 | 314k galaxies in the record; the human-labelled count is not stated | Strong | Today |
| 2 | Galaxy Zoo 2, original-sample images (+ vote tables from data.galaxyzoo.org) | Open download | Images CC-BY-4.0; table terms not checked | ~240k galaxies (from memory) | Strong | Images today; tables from memory |
| 3 | Galaxy Zoo: Cosmic Dawn (Euclid Deep Field North) | Open download | CC-BY-4.0 | "Over 41,000" galaxies | Strong, but borderline on size | Today |
| 4 | Galaxy Zoo DESI, GZD-8 volunteer subset only | Open download | CC-BY-4.0 | 96k galaxies | Partial (no images) | Today |
| 5 | Galaxy10 DECaLS | Open download | CC-BY-4.0 | ~18k | Partial (too small) | Today |

## Details

**1. Galaxy Zoo DECaLS** — https://zenodo.org/records/4573248
- It has volunteer vote counts from the GZD-1/2 and GZD-5 campaigns. The GZD-5 schema was "designed to better detect mergers and weak bars".
- It also includes the GZD-5 images that volunteers saw.
- Use only the volunteer files (`gz_decals_volunteers_1_and_2` and `gz_decals_volunteers_5`). `gz_decals_auto_posteriors` is model output.
- Many GZD-5 galaxies have only about 5 votes, so filter on vote count.
- The full record is about 108 GB. The page says the large image files may be hosted at the University of Manchester while Zenodo upload is pending.
- Images for GZD-1/2 are not bundled. You would fetch them from the Legacy Survey.

**2. Galaxy Zoo 2** — images: https://zenodo.org/records/3565489 (3.4 GB)
- The images are the original GZ2 sample. The record's own example is a galaxy volunteers called "a barred spiral galaxy with a mild bulge and two tightly-wound arms".
- The vote tables are on data.galaxyzoo.org (Willett et al. 2013; debiased version in Hart et al. 2016). The tool could only reach that site's home page, so I haven't confirmed the table files or their terms. Your join key is the SDSS object ID.
- SDSS images are lower resolution than DECaLS.
- Rotation-invariant CNNs trained on GZ2 labels are well established (https://doi.org/10.1093/mnras/stv632).

**3. Galaxy Zoo: Cosmic Dawn** — https://doi.org/10.5281/zenodo.17200992
- This is the only one where images and volunteer labels sit in the same record (PNG/JPG images plus `gzcd_volunteer_classifications.parquet`).
- It also contains Zoobot predictions, so use only the volunteer file.
- 41k leaves little room once you cut by vote count.
- The galaxies are deeper and higher-redshift than SDSS, so the domain differs.

**4. Galaxy Zoo DESI, GZD-8 only** — https://zenodo.org/records/8360385
- Use only `gz_desi_gzd8_volunteer_core_catalog.parquet` and the extended catalogue. These hold votes for 96k galaxies.
- The 8.7M-galaxy catalogues are deep-learning predictions.
- No images are included. Cut out Legacy Survey images by position.

**5. Galaxy10 DECaLS** — https://zenodo.org/records/10845026 (also on Hugging Face as `mwalmsley/galaxy10_decals`)
- It is the only ready-to-use images-plus-labels bundle, and its labels come from volunteer votes.
- It has about 18k images in 10 broad classes, so it is under your minimum. Use it for a quick baseline.

**What I'd do:** combine #1 (GZD-5, which has bundled images) and #4 (GZD-8 volunteer votes, 96k galaxies, images from the Legacy Survey). Both use the same DECaLS imaging and the same question tree. That gives you well over 40k human-labelled galaxies with bars, arms, bulge and merger questions.

## Known, not confirmed

- **GZ2 vote tables at data.galaxyzoo.org.** I believe they are open, but I couldn't check the files or licence today.
- **Volunteer-labelled count in GZ DECaLS.** The record doesn't state it. Count the rows in the volunteer catalogues before relying on it.

## Not recommended, and why

- **Euclid Q1 visual morphology catalogue** (https://zenodo.org/records/15106473). It has images and a large catalogue, but the page says the measurements "were made by Zoobot foundation models". These are model predictions, which you ruled out.
- **Galaxy Zoo DESI main catalogues (8.7M).** These are predicted vote fractions.
- **Galaxy10 SDSS.** It has 21.8k images at 69×69 pixels, which is below your minimum and low resolution.

## What I could not find

- A single download that bundles images and human-only labels at 40k or more.
- I did not look at Hubble or CANDELS Galaxy Zoo, or Radio Galaxy Zoo, which may offer more.
- The "papers that used it" check returned only one clearly relevant paper.

## Next step

Download the GZD-8 volunteer catalogue (#4) and the GZD-5 volunteer catalogue (#1). Count galaxies with at least about 10 votes per question, then fetch images for those.

Checked on 2026-11-11. Access rules and licences can change.

Interactive page: `/private/tmp/e-NBkNNi/home/cwd/dataset-shortlist.html`