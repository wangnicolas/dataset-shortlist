**Download Galaxy Zoo Evo (`mwalmsley/gz_evo` on Hugging Face).** It has about 806k galaxy images with the raw volunteer vote counts for each answer, stored together in the same rows. It meets every requirement you gave. If you want a smaller, single-survey set, start with **GZ2** (`mwalmsley/gz2`, about 209k galaxies) or **GZ DECaLS** (about 314k).

The dataset-registry search tool couldn't connect from this sandbox, and Zenodo refused my page requests. So everything below was checked on 2026-11-12 by web search and by fetching the pages, except where I mark it otherwise.

## What I assumed you need
- **Must have:** free images; detailed labels (bar, spiral arms, bulge size, merger); labels from humans, not model predictions; at least 40k galaxies.
- **Nice to have:** images and labels in one package; a licence that allows academic use. I assumed you don't need commercial use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Galaxy Zoo Evo | free Hugging Face login, minutes | CC BY-NC-SA 4.0 | 805,979 images, about 18 GB | strong | today |
| 2 | GZ2 (`mwalmsley/gz2`) | free Hugging Face login, minutes | CC BY-NC-SA 4.0 | about 209k galaxies, about 2.3 GB | strong | today |
| 3 | GZ DECaLS (Walmsley+2022) | open download from Zenodo | not confirmed | 314k galaxies, about 100 GB of PNGs | strong | from the paper; Zenodo blocked |
| 4 | GZ Euclid (`mwalmsley/gz_euclid`) | Hugging Face, minutes | not stated on the card | about 170k galaxies | partial | today |
| 5 | GZ Hubble / GZ CANDELS | `galaxy-datasets` package | see #1 | about 96k / about 48k | partial | today |
| 6 | Kaggle Galaxy Challenge | Kaggle account and accept the competition rules | competition rules | 61,578 galaxies | partial | today |

## Details
**1. [Galaxy Zoo Evo](https://huggingface.co/datasets/mwalmsley/gz_evo)**
- **Contents:** 664k training and 142k test images (424×424 pixels) from GZ2/SDSS, GZ DESI/DECaLS, Hubble, CANDELS and UKIDSS.
- **Labels:** columns follow the pattern `question-campaign_answer`. Each holds the number of volunteers who chose that answer, alongside `_fraction` and `_total-votes` columns.
- **Load it:** `load_dataset('mwalmsley/gz_evo', split='train')`. A `tiny` config is available for quick tests.
- **Things to know:**
  - The questions differ between campaigns, so expect many empty (NaN) columns.
  - The number of votes differs from galaxy to galaxy and question to question. The paper recommends a multinomial loss, or a cut such as at least 30 total votes.
  - Two subsets that aren't published yet (`gz_h2o`, `gz_ukidss`) need an access request.
- **Licence:** the dataset card asks that **models trained on the data be released as source code by publication**. Check that this suits your thesis.
- **Paper:** [Galaxy Zoo Evo, arXiv 2512.23691](https://arxiv.org/abs/2512.23691).

**2. [GZ2](https://huggingface.co/datasets/mwalmsley/gz2)**
- One survey (SDSS) with about 170 votes per galaxy on average, so it is the cleanest single training set.
- Also available as `galaxy_datasets.gz2(root=..., download=True)` from [galaxy-datasets](https://github.com/mwalmsley/galaxy-datasets).
- The label release is Willett et al. 2013 (from memory).

**3. GZ DECaLS**
- Download from [Zenodo, DOI 10.5281/zenodo.4196266](https://doi.org/10.5281/zenodo.4196266), or use the `gz_decals_5` loader (about 230k galaxies). Paper: [MNRAS 509, 3966](https://academic.oup.com/mnras/article/509/3/3966/6378289).
- The imaging is deeper than SDSS, which helps with faint features such as tidal tails from mergers.
- **Use only the `gz_decals_volunteers_*.csv` files.** `gz_decals_auto_posteriors.csv` contains model predictions.
- About 140k galaxies have 30 or more votes; the rest have about 5 each.

**4. GZ Euclid:** 169,899 training galaxies, but each has only about 5 volunteer votes, so the labels are noisy.

**5. GZ Hubble / GZ CANDELS:** high-redshift galaxies imaged by Hubble. Useful for domain-shift experiments.

**6. [Kaggle Galaxy Challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data):** 61,578 GZ2 images with 37 vote-fraction outputs. It is the classic CNN baseline, but #2 is a larger version of the same data. I couldn't read the competition rules page.

## Known, not confirmed
- **Licence of the GZ DECaLS Zenodo record:** Zenodo refused my connections. Check the latest version of the record yourself.
- **Licence of `gz_euclid`:** the dataset card doesn't state one.

## Not recommended, and why
- **GZ DESI catalogue (8.7M) and GZ Euclid Q1 catalogue (378k)** on [data.galaxyzoo.org](https://data.galaxyzoo.org/): these labels are Zoobot predictions, not human votes. The volunteer-labelled part of GZ DESI is already in Galaxy Zoo Evo. The `galaxy-datasets` README wrongly lists the 8.7M as "volunteer votes".
- **[Galaxy10 DECaLS/SDSS](https://astronn.readthedocs.io/en/latest/galaxy10.html):** about 17.7k and 21.8k galaxies with 10 coarse classes. Too small and not detailed enough.
- **GZ1:** about 900k galaxies, but labelled only as elliptical, spiral or merger. No bars or bulge.
- **Nair & Abraham 2010 and EFIGI:** expert labels, but only about 14k and about 4.5k galaxies (from memory).

## What I could not find
I know of no expert-labelled set with 40k or more galaxies. Every human-labelled set at that scale comes from Galaxy Zoo volunteers.

## Next step
Run `load_dataset('mwalmsley/gz_evo', name='tiny')` to look at the columns. Then train on GZ2 alone, or on GZ2 plus the DECaLS campaigns from Evo, with a vote-count loss.

I also built an interactive page that lets you filter and compare these datasets: `/private/tmp/e-od8sHE/home/cwd/dataset-shortlist.html`