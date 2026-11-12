I'd go with **Galaxy Zoo 2 (GZ2)**, downloaded through Mike Walmsley's `galaxy-datasets` Python package. It's free, and the images and labels come together in one download. You get about 210k SDSS galaxies, all labelled by volunteer votes, so you're well past 40k.

### Why GZ2 fits
- **The labels cover what you listed.** The GZ2 decision tree asks about bars, whether there are spiral arms, how many arms and how tightly wound, how prominent the bulge is, edge-on discs and bulge shape, and odd features including mergers and tidal debris.
- **The labels are human.** Each question has vote counts and vote fractions from about 40–50 volunteers per galaxy. The underlying catalogue is Willett et al. 2013, with debiased fractions from Hart et al. 2016.
- **It's easy to load:**
  ```python
  pip install galaxy-datasets

  from galaxy_datasets import gz2
  catalog, label_cols = gz2(root='data/gz2', train=True, download=True)
  # catalog: pandas DataFrame with 'file_loc' (image path) + vote columns
  ```
  There's also a ready-made PyTorch `Dataset`: `from galaxy_datasets.pytorch import GZ2`. Using `train=True` or `train=False` still downloads everything; the flag only picks which split you get back.

### Alternatives in the same package
- **`gz_decals_5`**: about 230k galaxies with volunteer votes. The DECaLS images are deeper than SDSS and show faint features like tidal tails better, so it's the better choice if mergers matter a lot to you. The question tree is a bit different from GZ2's (for example, it has strong vs. weak bar answers and better merger questions).
- **`gz_hubble`** (~106k) and **`gz_candels`** (~50k) are volunteer-labelled too, but they're high-redshift HST galaxies. That's only relevant if your thesis is about distant galaxies.

### Things to avoid
- **GZ DESI (8.7M galaxies) and any table with "auto" or "posterior" in its name.** In the GZ DESI release paper (Walmsley et al. 2023), the 8.7M labels are Zoobot CNN predictions, not votes. That's exactly what you want to keep out of your training data. The package README lists `gz_desi` under "volunteer votes", which doesn't match how I understand that release, so if you ever touch it, check which columns are actual votes. The same goes for the DECaLS DR8 data, which includes automated predictions alongside volunteer votes.
- **Kaggle's "Galaxy Zoo – The Galaxy Challenge"** (about 61.5k GZ2 images with vote fractions). It technically meets your requirements, but the labels were post-processed into a particular cumulative-fraction format for the competition, and it's a subset of what the package gives you. It's only useful if you want to compare against the published competition baselines.
- **Galaxy10 DECaLS.** It has only about 17.7k images in 10 broad classes, so it's too small and too coarse for you.

### Practical tips
- Train on **vote fractions** with a soft or Dirichlet-multinomial loss rather than thresholding into hard classes. Also, only count answers to later questions (like bar or arm count) for galaxies where enough volunteers reached that question; the `*_total-votes` columns tell you this.
- You have to cite the GZ2 data release paper (Willett et al. 2013) and acknowledge SDSS. For DECaLS, cite Walmsley et al. 2022 and acknowledge the Legacy Surveys.

The ~210k count and the download code are from the current `galaxy-datasets` README. I haven't checked the exact column names, so look at `label_cols` after you download.

Sources:
- [galaxy-datasets on GitHub](https://github.com/mwalmsley/galaxy-datasets)