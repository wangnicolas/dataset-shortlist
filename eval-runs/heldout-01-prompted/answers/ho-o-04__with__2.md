Three options meet your requirements. For each one I checked that the page exists and how you get the data. I couldn't confirm every detail, and I mark those gaps below.

## Recommended: Galaxy Zoo 2 on Hugging Face (`mwalmsley/gz2`)
- **Size and images:** The page shows about 191k rows, split into about 172k train and 18.8k test. Each row has a 424×424 image, so images and labels come together. A ~1.9k-row `tiny` subset is useful for testing your pipeline.
- **Labels:** Labels are volunteer vote counts for each question in the Galaxy Zoo decision tree. For each answer you get a count and a fraction, and for each question a total-vote column. The questions cover smooth or featured, edge-on, bar, spiral arms, bulge size, merging or disturbed, and so on. The page cut off some question columns, so check the full column list yourself.
- **Access:** It's in parquet format and loads with `datasets.load_dataset("mwalmsley/gz2")`. The page showed no gating, but it gave no loading snippet, so the load call is my assumption.
- **License:** CC BY-NC-SA 4.0, which is fine for a thesis.
- **Caveat:** The galaxies are SDSS images, which are shallower than DECaLS. The vote counts are raw human votes. You'll want to filter on total votes so each label has enough volunteers behind it.

## Larger option: Galaxy Zoo Evo (`mwalmsley/gz_evo`)
- **Size:** About 1M labelled images: ~850k "core" images from four telescopes, plus ~150k in downstream subsets. The paper abstract (Galaxy Zoo Evo) says 104M crowdsourced labels for 823k images.
- **Access:** The GitHub page ([mwalmsley/gz-evo](https://github.com/mwalmsley/gz-evo)) loads it with `datasets.load_dataset("mwalmsley/gz_evo")`. The Hugging Face page lists the license as CC BY-NC-SA 4.0 and a size category of 100K–1M.
- **Caveat:** The page excerpt I got didn't state the exact subset contents or the label format, and I couldn't read the dataset card. It should be human votes, but check the card before relying on it. Also confirm there that the labels are volunteer votes and not model predictions, since the GZ DESI catalogue (below) mixes the two.

## Smaller curated option: Galaxy10 DECaLS
- **Size and labels:** It has 17,736 images (256×256) with 10 classes, taken from volunteer Galaxy Zoo labels. That's below your 40k minimum, so use it only as a quick benchmark. The classes include barred spiral, merging and disturbed, but there's no bulge-size label.
- **Access:** The data is on [Zenodo](https://zenodo.org/records/10845026) as a 2.7 GB HDF5 file. You can also use `astroNN.datasets.load_galaxy10`.
- **Caveat:** The classes are imbalanced and were chosen by a rule-based filter, so these are not the original vote counts.

## Be careful with
- **Galaxy Zoo DESI** ([Zenodo 8331338](https://zenodo.org/records/8331338)): the main catalogue covers 8.7M galaxies, but those are **deep-learning predictions**. That fails your human-labels requirement. The Zenodo record also releases raw volunteer votes (GZD-8), but it doesn't include images. You'd have to download cutouts from the Legacy Survey cutout service.
- **Galaxy Zoo DECaLS** (DOI 10.5281/zenodo.4196266): this release has both volunteer and model catalogues, and no images. Use the volunteer tables only.
- **`mwalmsley/gz_h2o`:** it's gated while unpublished, with 10K–100K rows, which is too small.

My suggestion is to start with `gz2` for the 40k+ with bundled images. If you need deeper imaging or more data, move to `gz_evo` after reading its dataset card. I didn't download any data, and I couldn't read the `gz_evo` card or the `gz2` loading instructions, so confirm those on the Hugging Face pages.

Sources:
- [Galaxy Zoo DESI paper](https://academic.oup.com/mnras/article/526/3/4768/7283169)
- [Galaxy Zoo DESI on Zenodo](https://zenodo.org/records/8331338)
- [Galaxy Zoo data hub](https://data.galaxyzoo.org/)
- [mwalmsley/gz2](https://huggingface.co/datasets/mwalmsley/gz2)
- [mwalmsley/gz_evo](https://huggingface.co/datasets/mwalmsley/gz_evo)
- [mwalmsley/gz_h2o](https://huggingface.co/datasets/mwalmsley/gz_h2o)
- [gz-evo on GitHub](https://github.com/mwalmsley/gz-evo)
- [Galaxy10 DECaLS on Zenodo](https://zenodo.org/records/10845026)
- [Galaxy10 on GitHub](https://github.com/henrysky/Galaxy10)
- [astroNN Galaxy10 docs](https://astronn.readthedocs.io/en/latest/galaxy10.html)