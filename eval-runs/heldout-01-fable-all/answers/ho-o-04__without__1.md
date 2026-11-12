**Download Galaxy Zoo 2 (GZ2) through the `galaxy-datasets` Python package.** It gives you about 210k SDSS galaxies with volunteer vote counts, and the images and labels arrive together in one call. I checked the sources online but did not run the download myself.

```python
# pip install galaxy-datasets
from galaxy_datasets import gz2

catalog, label_cols = gz2(root='data/gz2', train=True, download=True)
```

`catalog` is a pandas table with one row per galaxy, including the image path, and `label_cols` names the vote-count columns. There is also a PyTorch wrapper (`from galaxy_datasets.pytorch import GZ2`) and a Hugging Face copy at `mwalmsley/gz2`, whose card I did not inspect.

Why it fits your requirements:

- **Human labels:** every label is the number of volunteers who gave each answer; from memory, each galaxy has roughly 40 or more classifications.
- **Detailed morphology:** from memory of the GZ2 decision tree, it covers bar, spiral arms (count and winding), bulge prominence, edge-on bulge shape, and odd features including rings, mergers, disturbed and dust lanes.
- **Size:** about 210k galaxies, and the image set is only about 3.4 GB of JPEGs.
- **Free:** the package is GPL-3.0 and the underlying Zenodo image release is CC BY 4.0. Cite Willett et al. 2013 and SDSS.

Two things to handle in training:

- **Conditional questions:** volunteers were only asked about bars or arms if they first answered "features or disk". Mask or down-weight questions with few responses rather than treating a 0 as "no bar".
- **Soft labels:** predict vote fractions or counts rather than hard classes; forcing a majority-vote class throws away the uncertainty information.

**Alternative: Galaxy Zoo DECaLS (GZD-5)**, about 230k galaxies, also in the package as `gz_decals_5`. The imaging is deeper, and as I recall the questions are better for your purposes: strong/weak/no bar, and merger versus major or minor disturbance. The catch is that many galaxies have only about five volunteer responses, so you would need to filter by vote count; I haven't checked how many pass a strict cut. If you take it from Zenodo (record 4573248, CC BY 4.0, about 108 GB) instead, use the `gz_decals_volunteers_5` file and not `gz_decals_auto_posteriors`, which is model predictions.

**Avoid for your purpose:**

- **GZ DESI (8.7M galaxies):** as I recall, its headline catalogue is mostly model predictions.
- **Galaxy10 DECaLS and GalaxyMNIST:** human-labelled but only about 18k and 10k galaxies with coarse classes.
- **`mwalmsley/gz_evo` on Hugging Face:** combines several Galaxy Zoo campaigns, but it is licensed CC BY-NC-SA and I couldn't confirm its contents.

Sources:
- [galaxy-datasets (GitHub)](https://github.com/mwalmsley/galaxy-datasets)
- [Galaxy Zoo 2 images (Zenodo 3565489)](https://zenodo.org/records/3565489)
- [Galaxy Zoo DECaLS (Zenodo 4573248)](https://zenodo.org/records/4573248)
- [mwalmsley/gz_evo (Hugging Face)](https://huggingface.co/datasets/mwalmsley/gz_evo)
- [mwalmsley datasets list (Hugging Face API)](https://huggingface.co/api/datasets?author=mwalmsley&limit=100)