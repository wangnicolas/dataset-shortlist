## What I assumed you need
- **R1 (must):** detailed morphology labels (bars, spiral arms, bulge, mergers).
- **R2 (must):** at least 40k galaxies.
- **R3 (must):** labels from human votes, not model predictions.
- **R4 (nice to have):** images bundled with the labels.

Everything below is from the registry records (Zenodo) and the Galaxy Zoo data page, checked 2026-11-12, unless I mark it "from memory". I did not open the papers describing these releases. The literature search returned almost nothing useful, so I list no usage papers.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Galaxy Zoo DECaLS (Zenodo 4573248) | Open download, minutes | CC-BY-4.0 | ~108 GB, including ~104 GB of images | Strong, with the label caveat below | Today |
| 2 | Galaxy Zoo 2 images (Zenodo 3565489) plus the GZ2 table from data.galaxyzoo.org | Open download, minutes | Images CC-BY-4.0; table licence not stated on the page I read | 3.4 GB of images | Strong (richest label set) | Today |
| 3 | Galaxy Zoo: Cosmic Dawn (Zenodo 17200992) | Open download | CC-BY-4.0 | 41k+ galaxies, 5.3 GB | Partial | Today |
| 4 | Galaxy Zoo: UKIDSS, near-infrared (Zenodo 13357341) | Open download | CC-BY-4.0 | 71,052 galaxies | Partial (images not checked) | Today |

## Details
**1. Galaxy Zoo DECaLS.** The record has separate volunteer catalogues (`gz_decals_volunteers_1_and_2` and `_5`) and the DECaLS images (`gz_decals_dr5_png_part1–4.zip`), joined on `iauname`. A `schema.md` file defines the columns.
- **Use only the `volunteers_*` files.** The record also has `gz_decals_auto_posteriors`, which holds CNN predictions for all 314k galaxies. Using those would break your human-labels rule.
- **Label count:** the "314,000 galaxies" in the title includes galaxies labelled only by the model. I did not confirm how many have volunteer votes, so count rows in the volunteer files before committing to 40k.
- **Vote noise:** the record says many GZD-5 galaxies have only about 5 volunteer responses. Filter on vote count.
- **Images:** the record describes the images as those shown to volunteers in the GZD-5 campaign. Images for the earlier GZD-1/2 galaxies may need a separate source.

**2. Galaxy Zoo 2.** The images (SDSS) are on Zenodo, and the data.galaxyzoo.org page says "The GZ2 images are available for download on Zenodo." The labels are not bundled, so you download the vote table separately and join them.
- **Labels:** GZ2 has 16M volunteer classifications of 304,122 galaxies. It has the deepest question tree: bars, spiral arm number and tightness, bulge prominence, mergers and odd features.
- **Image count:** the original-sample image count is about 240k, from memory.
- **Where to get the table:** the Zenodo table record (3566991) is marked `access_right=restricted`, with files restricted. Use data.galaxyzoo.org instead, which says its catalogue downloads are open.
- **Resolution:** SDSS images are low resolution, and deep sub-questions leave few galaxies per class.

**3. Galaxy Zoo: Cosmic Dawn.** This is above 40k, but only just, and fewer after vote-count cuts. Its page says the subjects were also classified by the deep-learning model Zoobot, so use the volunteer columns only.

**4. Galaxy Zoo: UKIDSS.** It has 71k galaxies with volunteer morphologies. I did not check whether images are in the record, so check the file list first. It would suit a second-survey or transfer experiment.

## Known, not confirmed
- **Galaxy Zoo: Hubble and CANDELS.** Both are on data.galaxyzoo.org (listed there), with volunteer labels. I did not check their sizes or whether images are included, so they may not reach 40k.
- **Galaxy Zoo: Mergers.** Also listed on data.galaxyzoo.org. It could be useful if mergers are your focus, but I did not check it.

## Not recommended, and why
- **Galaxy Zoo DESI (8.7M).** Its Zenodo record says the catalogues come from deep-learning models trained on volunteer responses. These are model predictions, so it fails your human-label rule.
- **Galaxy10 DECaLS, Galaxy10 SDSS and Galaxy MNIST.** Their labels derive from Galaxy Zoo, but they have only about 17–22k images (from memory) and 10 coarse classes.
- **Hugging Face copies of GZ2.** I did not check what labels they carry. Prefer the official sources above.
- **Euclid Q1 morphology catalogue.** I did not check whether it is volunteer-only.

## What I could not find
- No single download with images and detailed volunteer labels for 40k+ galaxies. You will join image folders to vote tables yourself.
- The volunteer-labelled subset size for GZ DECaLS (see above).

## Next step
Download the GZ DECaLS volunteer parquet files and `schema.md` (a few MB) and count galaxies with enough votes on the questions you care about. If that falls short of 40k, add GZ2 for more galaxies and a deeper question tree. Treat the vote fractions as noisy soft labels (train on them directly or filter by vote count) rather than hard classes.

The interactive page is at `/private/tmp/e-fGk0y2/home/cwd/dataset-shortlist.html`.