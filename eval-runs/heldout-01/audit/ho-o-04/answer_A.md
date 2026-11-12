I'd start with **Galaxy Zoo**. It's the main source of volunteer-labelled galaxy morphology. These are the options that fit your constraints (I'm going from memory, so check the exact sizes and URLs on the pages).

## Best fits

**1. Galaxy Zoo DECaLS (GZD-5, and GZD-8 in the later releases)**
- It has hundreds of thousands of galaxies (roughly 250k for GZD-5). The images are deeper and sharper than SDSS.
- The labels are volunteer vote counts for a decision tree. It covers bars, spiral arm count and tightness, bulge size, mergers and tidal features, edge-on discs, and more.
- Walmsley et al. 2022 describes it.
- The Zoobot project (Walmsley et al.) hosts the images and votes together on Hugging Face under the `mwalmsley` account, so you can load them with the `datasets` library. Search for the `gz_decals` and `gz_evo` datasets.

**2. Galaxy Zoo 2 (SDSS)**
- It has about 240k to 300k galaxies in the Willett et al. 2013 catalogue, with vote fractions on the same kind of questions: bar, spiral, bulge prominence (none, just noticeable, obvious, dominant), merger or odd features, and edge-on.
- The images are lower resolution than DECaLS. They are 424×424 JPEGs.
- The **Kaggle "Galaxy Zoo – The Galaxy Challenge"** download bundles about 61k training images with 37 vote-fraction columns. That is above your 40k minimum, and the images and labels come together. You need a free Kaggle account and have to accept the competition rules.
- The Hugging Face `gz2` dataset is another option.

## What to avoid

- **Galaxy10 DECaLS and Galaxy10 SDSS** are convenient, but they're too small (about 17k and 21k). They also reduce the votes to 10 coarse classes, so you'd lose bar, bulge and merger detail.
- **Galaxy Zoo DESI** and parts of **GZ Evo** mix volunteer votes with Zoobot model predictions. This matters because you need human-only labels. If you use them, take only the volunteer vote-count columns and ignore the model-posterior columns. For a clean thesis, GZD-5 or GZ2 is simpler to defend.

## Using the votes

- **Filter by vote count.** Keep galaxies where the relevant question has at least about 20 to 30 votes. Questions are conditional, so a bar vote only exists for galaxies that volunteers called "featured, not edge-on".
- **Train on vote fractions or counts** (soft labels or a Dirichlet/multinomial loss) rather than hard classes. Zoobot does this.
- **Check class balance.** Mergers and strong bars are rare, so you'll need weighting or oversampling.
- **Cite the papers** (Willett 2013, Walmsley 2022, and the Galaxy Zoo volunteers). Both data releases ask for this.

I'd go with GZD-5 from Hugging Face for the main run, and use the Kaggle GZ2 set as a second dataset to test generalisation across surveys. I can write the download and filtering script if you want.