**Download Galaxy Zoo DECaLS (GZD-5) through the `galaxy-datasets` Python package.** It gives you about 230k galaxies with images and labels together, and the labels are volunteer vote counts. Galaxy Zoo 2 is a good second option and comes through the same package.

```bash
pip install galaxy-datasets
```
```python
from galaxy_datasets import gz_decals_5   # or gz2

catalog, label_cols = gz_decals_5(root='data/gz_decals_5', train=True, download=True)
# catalog: pandas DataFrame with a 'file_loc' column (image path) + vote-count columns
```
The same package has a ready-made PyTorch dataset (`galaxy_datasets.pytorch`) and a Lightning DataModule.

## Why these two

| Dataset | Method | Galaxies | Images | Notes |
|---|---|---|---|---|
| **GZ DECaLS GZD-5** | `gz_decals_5` | ~230k | DECaLS (deeper than SDSS) | My first choice. The question tree covers your list: strong/weak/no bar, number of spiral arms and how tightly they wind, bulge size, and a merger/disturbance question. Deeper images make faint features like tidal tails easier to see. |
| **Galaxy Zoo 2** | `gz2` | ~210k (main sample) | SDSS | The most-cited benchmark, so your results are easy to compare with other work. The tree is similar (bar, arm count and winding, bulge prominence, "odd" features including mergers). |

Both are far above your 40k minimum.

## Watch out for model-generated labels

- **GZ DESI (`gz_desi`, 8.7M galaxies):** those labels are Zoobot model predictions, not human votes (Walmsley et al. 2023), so it fails your requirement. It's also about 500 GB.
- **The raw GZ DECaLS release on Zenodo / data.galaxyzoo.org** includes "automated posterior" files from Zoobot next to the volunteer catalogs. If you download from there instead of through the package, use only the volunteer vote files. I haven't checked which files the `gz_decals_5` loader pulls, so confirm the label columns are vote counts, not posteriors.
- Some other entries in the package (GZ Rings, GZ Euclid) may mix in model labels or use a different label process, so check their papers before using them. GZ Hubble (~106k) and GZ CANDELS (~50k) are volunteer-labelled, but they're high-redshift HST images and much harder for this kind of task.

## Tips for your thesis

- **Train on vote fractions, not hard labels.** Galaxy Zoo is a decision tree: a bar question is only asked if the volunteer first said the galaxy is featured and not edge-on. So many galaxies have few or no votes on detailed questions. Either filter by number of votes, or use a loss that weights by vote count (Zoobot uses a Dirichlet-multinomial loss).
- **Mergers are rare.** Expect heavy class imbalance on that question.
- **Licensing:** the code is GPL-3.0. The data is free for research, but you must cite the Galaxy Zoo data release paper (Walmsley et al. 2022 for DECaLS, Willett et al. 2013 for GZ2) and acknowledge the survey (DECaLS/Legacy Surveys or SDSS). data.galaxyzoo.org has the citation text.
- **Small alternatives:** Galaxy10 DECaLS (~17.7k, 10 classes) is too small for you. The Kaggle "Galaxy Zoo – The Galaxy Challenge" (~61k GZ2 images with 37 vote-fraction targets) is fine for a quick start, but the package version is larger and better documented.

The dataset list and counts come from the `galaxy-datasets` GitHub README as of today. The note that GZ DESI labels are model predictions comes from the GZ DESI paper, not the README.