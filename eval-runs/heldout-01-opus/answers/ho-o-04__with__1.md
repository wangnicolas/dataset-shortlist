## Recommendation

Use **Galaxy Zoo DECaLS/DESI volunteer votes with bundled images: `mwalmsley/gz_desi` on Hugging Face**. It has about 400k rows (319,530 train and 79,883 test) and loads with one line of Python. Use **`mwalmsley/gz2`** (about 191k rows of SDSS images) as a second dataset or for comparison with published work. Both have the labels you named, the labels are human volunteer votes, and you can download them today with no account.

## What I assumed you need
- **R1 (must):** at least 40,000 labelled galaxies.
- **R2 (must):** detailed labels for bars, spiral arms, bulge size and mergers, not just a few coarse classes.
- **R3 (must):** labels come from people (volunteers or experts), not from model predictions.
- **R4 (nice to have):** images come with the labels.
- **R5 (must):** free, and use in a master's thesis is allowed.

## Shortlist (checked 2026-11-12)
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | `mwalmsley/gz_desi` (DECaLS images + GZ DECaLS/DESI votes) | Open download | CC BY-NC-SA 4.0 | 319,530 + 79,883 rows, ~17.5 GB | Strong | today |
| 2 | `mwalmsley/gz2` (SDSS images + GZ2 votes) | Open download | CC BY-NC-SA 4.0 | 172,377 + 18,797, ~2.6 GB | Strong | today |
| 3 | `mwalmsley/gz_evo` (all campaigns combined) | Open download | CC BY-NC-SA 4.0 | 664,219 + 141,760, ~18 GB | Strong | today |
| 4 | `mwalmsley/gz_hubble` | Open download | CC BY-NC-SA 4.0 | 77,158 + 19,291, ~6.4 GB | Strong (distant galaxies) | today |
| 5 | `mwalmsley/gz_ukidss` (near-infrared) | Open download | CC BY-NC-SA 4.0 | 56,676 + 14,169 | Partial | today |
| 6 | `mwalmsley/gz_euclid` | Open download | no licence stated | 169,899 + 2,378 | Partial | today |
| 7 | `mwalmsley/gz_candels` | Open download | CC BY-NC-SA 4.0 | ~48k total | Partial (just over 40k) | today |
| 8 | Kaggle "Galaxy Zoo – The Galaxy Challenge" | Free Kaggle account, accept the rules | Competition rules | 61,578 training images | Partial | from memory |

## Details
- **How the labels look (checked today in `gz_desi`'s feature list):** each answer has a vote-count column, for example `bar-dr5_strong`, `bar-dr5_weak`, `bulge-size-dr5_small`. Each also has a `_fraction` column, and each question has a `*_total-votes` column. The dataset card describes the data as "galaxy images and volunteer labels" and lists the annotation source as `crowdsourced`. Today the Hugging Face API reports `gated=false` for all seven datasets.
- **Steps (minutes):**
  1. `pip install datasets`
  2. `load_dataset('mwalmsley/gz_desi', split='train')`. Try `name='tiny'` first; it is about 1% of the data.
  3. Alternatively, the `galaxy-datasets` package (github.com/mwalmsley/galaxy-datasets) downloads the images plus a pandas catalogue: `gz2`, `gz_decals_5` (~230k), `gz_hubble`, `gz_candels`, `gz_rings`.
- **Licence condition:** the licence is non-commercial and share-alike, which is fine for a thesis. The dataset cards add one condition: **"all models trained on these datasets [must] be released as source code by publication."** Plan to publish your code.
- **Caveats:**
  - In `gz_desi`, votes from different campaigns (dr5, dr8, dr12) use slightly different question trees, so many columns are empty for any one galaxy. You will need to mask the missing answers in your loss.
  - GZ2 images come from SDSS, which is shallower than DECaLS, so faint bars and tidal features are less visible.
- **Papers that used these data:**
  - Walmsley et al. 2022, *Galaxy Zoo DECaLS*, MNRAS, doi:10.1093/mnras/stab2093. It reports 7.5M volunteer classifications of 314k galaxies.
  - Dieleman et al. 2015, *Rotation-invariant CNNs*, doi:10.1093/mnras/stv632. This is the winning Kaggle solution on GZ2 vote fractions.
  - Domínguez Sánchez et al. 2018, doi:10.1093/mnras/sty338. CNNs trained on GZ2 labels and the Nair & Abraham expert labels.

## Known, not fully confirmed
- **The original Zenodo releases:**
  - GZ DECaLS catalogues with separate volunteer and model-prediction tables: zenodo.org/records/4573248 (CC BY 4.0).
  - GZ2 images (Hart et al. sample): zenodo.org/records/3565489 (CC BY 4.0).

  I confirmed both through their DOI records. Zenodo did not respond from here, so I could not check the file lists. If you use these, take the `gz_decals_volunteers_*` tables, not the automated ones.
- **Kaggle challenge:** the access terms and the 61,578 figure are from memory, because the page could not be read. Its test labels were never released, and `gz2` is a larger superset of it.
- **`gz_euclid`:** the columns look like volunteer vote counts, but the dataset card has no description or licence. The Euclid Q1 catalogue also contains Zoobot model predictions. Confirm with the Galaxy Zoo team which rows are volunteer-labelled before using it.

## Not recommended, and why
- **The 8.7M-galaxy GZ DESI catalogue (Zenodo 8360385)** is deep-learning predictions, so it fails your human-labels requirement. Only its volunteer-vote tables qualify, and those are what `gz_desi` contains.
- **Euclid Q1 visual morphology catalogue (Zenodo 15106473):** its main columns are model predictions too.
- **Galaxy10 DECaLS / Galaxy10 SDSS:** about 18–22k images and only 10 coarse classes.
- **Galaxy Zoo 1:** very large, but it has only elliptical/spiral/merger votes, with no bars, arm counts or bulge size.
- **Nair & Abraham 2010 (~14k) and EFIGI (~4.5k):** expert labels but too small. They would work well as an expert-labelled test set.

## What I could not find
No expert-labelled set of 40k or more galaxies with bar, arm and bulge labels exists as far as I know. Every large human-labelled set I found is Galaxy Zoo volunteer votes. The file lists of the Zenodo records are unchecked because Zenodo timed out.

## Next step
Load `mwalmsley/gz_desi` with `name='tiny'` and check the vote columns for the questions you need. Then train on the full set, using the vote fractions or counts as targets (a Dirichlet-multinomial loss is what Zoobot uses). If you want a second survey for cross-survey tests, add `gz2`.

The interactive page with all of this is at `/private/tmp/e-6ivpD5/home/cwd/dataset-shortlist.html`.