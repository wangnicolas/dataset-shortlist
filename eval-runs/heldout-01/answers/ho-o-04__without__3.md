**Download Galaxy Zoo 2 (GZ2).** It's SDSS imaging with volunteer votes, and it covers everything you listed.

**Primary: Galaxy Zoo 2 (Willett et al. 2013, with Hart et al. 2016 debiased votes)**
- **Size:** about 240k galaxies with images. That's well above your 40k minimum.
- **Labels:** volunteer vote fractions and counts, not model output. The decision tree includes:
  - bulge prominence (none, just noticeable, obvious, dominant)
  - bar present or not
  - spiral arms, with arm count and tightness
  - merger/disturbed/irregular
  - edge-on, rounded, and odd features
- **Images:** about 243k JPEG cutouts (424×424), distributed on Zenodo as "Galaxy Zoo 2 images". The `gz2_filename_mapping.csv` file links image filenames to SDSS object IDs. The vote tables come from data.galaxyzoo.org. Use the `gz2_hart16` table for the debiased fractions.
- **Bundled option:** the Kaggle "Galaxy Zoo – The Galaxy Challenge" dataset has 61,578 training images with 37 GZ2 vote-fraction columns, all in one download. It needs a free Kaggle account. It's the easiest way to get images and labels together, and it's enough for your 40k target.

**Alternative: Galaxy Zoo DECaLS (Walmsley et al. 2022)**
- **Size:** about 300k galaxies.
- **Images:** deeper and sharper than SDSS, so faint features such as bars and mergers are easier to see.
- **Catalog:** use the volunteer vote tables only. The later DESI-era catalogs mix in Zoobot model predictions for many galaxies, which you need to avoid.
- **Downloads:** the images are fetched from the Legacy Survey cutout service or the provided Zenodo files, so they take more setup than GZ2.

**Skip these:**
- **Galaxy10 (DECaLS and SDSS):** the images and labels come bundled in one H5 file, but they're small (about 18k and 21k galaxies). The class labels are also thresholded from Galaxy Zoo votes, so you lose the detailed morphology.
- **Any "Zoobot" catalog columns:** these are model predictions.

**Practical tips:**
- Votes are noisy for galaxies with few classifications, so filter by `total_votes` or use the Hart debiased fractions.
- Build one training label per question from the vote fractions. For example, treat "bar" as present only when `p_bar > 0.5` and enough volunteers answered that question. Or train on the fractions directly with a Dirichlet or multinomial loss, as the Galaxy Zoo Challenge winners did.
- Split train and test by galaxy ID, and consider keeping a high-agreement subset for evaluation.

I haven't checked that the Zenodo and Kaggle links are live today. Search for "Galaxy Zoo 2 images Zenodo" and the Kaggle competition name, and cite Willett+2013 and Hart+2016 (or Walmsley+2022) in your thesis.