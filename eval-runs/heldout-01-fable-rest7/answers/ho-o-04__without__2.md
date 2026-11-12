**Download Galaxy Zoo 2 (GZ2).** It meets every requirement and is the standard benchmark for this task. I'm answering from memory and didn't check the links live, so confirm the record IDs and counts before relying on them.

**Why GZ2**
- **Size:** about 240k SDSS galaxies, as 424×424 colour JPGs.
- **Human labels:** volunteer votes only, roughly 40+ per galaxy, so the vote fractions are fairly low-noise.
- **Morphology detail:** a decision tree covering smooth/featured/artifact, edge-on, bar, spiral arms (presence, tightness, count), bulge prominence, bulge shape, roundedness, and odd features (merger, ring, lens, disturbed, dust lane).
- **Citations:** Willett et al. 2013 for the catalogue, Hart et al. 2016 for the debiased vote fractions.

**Where to get images and labels together**
1. **`galaxy-datasets` Python package** (Mike Walmsley, Galaxy Zoo team): `pip install galaxy-datasets`, then `from galaxy_datasets import gz2`. This downloads images plus a label table with train/test splits, and has PyTorch helpers. The same data is on Hugging Face under `mwalmsley/gz2`.
2. **Zenodo record 3565489:** the full GZ2 image set plus a filename mapping to join with the Hart et al. 2016 vote table from data.galaxyzoo.org.
3. **Kaggle "Galaxy Zoo – The Galaxy Challenge":** 61,578 training images with 37 vote-fraction columns in one zip. It is the easiest start and still above your 40k, but it is a subset; the Kaggle test-set labels aren't public.

**Alternative: Galaxy Zoo DECaLS (GZD-5)**
- **What it adds:** about 250k galaxies with deeper imaging, so faint bars and tidal features show better, and a dedicated merger question (merger / major disturbance / minor disturbance / none).
- **Where:** Zenodo record 4573248, or `gz_decals_5` in the same package.
- **Watch for the label source:** use only the **volunteer** catalogues (`gz_decals_volunteers_5`), not `gz_decals_auto_posteriors`, which are CNN predictions.
- **Watch for vote counts:** many galaxies have only about 5 votes, with about 40 for a subset. Filter by vote count or use a loss that accounts for it.

**Sets that fail your requirements**
- **Galaxy Zoo DESI** (8.7M galaxies): the labels are mostly model predictions.
- **Galaxy10 DECaLS** (17.7k), **Nair & Abraham 2010** (14k, expert) and **EFIGI** (4.5k, expert): all are under 40k. The two expert sets are still useful as an independent test set.

**Training tips**
- Predict vote fractions or counts rather than hard classes.
- Mask questions that few volunteers reached; bar votes mean nothing for a galaxy most people called smooth.