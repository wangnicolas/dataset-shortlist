Download **Galaxy Zoo DECaLS (GZD-5)** using Mike Walmsley's `galaxy-datasets` Python package. It gives you images and volunteer vote labels together, and it meets all your requirements.

```bash
pip install galaxy-datasets
```
```python
from galaxy_datasets import gz_decals_5

catalog, label_cols = gz_decals_5(root='data/gz_decals_5', train=True, download=True)
# catalog['file_loc'] = path to each image; label_cols = per-answer volunteer vote counts
# train=False gives the official test split (the whole dataset downloads either way)
```

There's also a PyTorch `Dataset` version: `from galaxy_datasets.pytorch import ...`.

**Why this one:**
- **Size:** about 230k galaxies, far more than your 40k minimum.
- **Human labels:** the labels are counts of how many Galaxy Zoo volunteers gave each answer in the decision tree. They are not model outputs.
- **The features you listed:** the decision tree asks about strong, weak or no bar; whether there are spiral arms, how many, and how tightly wound; bulge size; edge-on bulge shape; and merger or tidal features.
- **Image quality:** the images come from DECaLS, which is deeper and sharper than SDSS, so faint arms and tidal features show up better.

**Pitfalls to avoid:**
- **Don't use GZ DESI.** It's listed next to the others, but its 8.7M labels are mostly predictions from Walmsley's Zoobot model, so they break your human-labels rule.
- **Don't take labels from the automated Zoobot catalogs on Zenodo.** The Galaxy Zoo DECaLS release there includes Zoobot prediction tables alongside the volunteer vote tables. If you ever download the catalogs directly instead of through the package, use only the volunteer vote tables.
- **Galaxy10 DECaLS is too small.** It has about 17.7k galaxies and only 10 coarse classes.

**Alternatives that also use human labels:**
- **Galaxy Zoo 2** (`gz2` in the same package): about 210k SDSS galaxies with a similar decision tree. It's the most cited, but the images are shallower. The debiased vote fractions from Hart et al. 2016 are a good fit for this one.
- **The 2014 Kaggle "Galaxy Zoo" challenge:** about 61k GZ2 images with vote fractions. It's simple, but the labels are weighted, cumulative fractions and the set is smaller.
- **Other surveys in the same package:** GZ Hubble (~106k), GZ CANDELS (~50k) and GZ UKIDSS (~71k), if you want a different survey or a high-redshift sample.

**Tips for training:**
- Use vote fractions or counts as your targets, not hard classes. The questions further down the tree, like bar type or number of arms, are only answered by volunteers who first said the galaxy has a disk. So you should mask or weight by how many volunteers answered each question. Otherwise galaxies with only two or three votes on a question will add noise.
- Zoobot's Dirichlet-multinomial loss on vote counts is the standard way to handle this. It's also a natural baseline to compare your CNN against.
- For your thesis, cite the data release paper (Walmsley et al. 2022, MNRAS 509, 3966 for GZ DECaLS) and acknowledge the Legacy Surveys / DECaLS for the images. The citation text for each dataset is at data.galaxyzoo.org.

I checked the package's GitHub README for the current dataset list and API. I couldn't open the Zenodo record (the connection was reset), so I haven't confirmed the image size or the exact download size. Make sure you have tens of GB of free disk space.

Sources:
- [mwalmsley/galaxy-datasets (GitHub)](https://github.com/mwalmsley/galaxy-datasets)
- [Mike Walmsley on Hugging Face](https://huggingface.co/mwalmsley)