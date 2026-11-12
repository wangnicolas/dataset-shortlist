**Recommendation: Galaxy Zoo.** Its labels are volunteer votes, and the sets are large enough for your 40k minimum. I'm going from memory and haven't checked the repositories or licences, so confirm exact names and terms before you build on them.

## Best options

**1. Galaxy Zoo 2 (SDSS), about 240k–300k galaxies**
- **Labels:** the volunteers answered a decision tree covering bar (strong, weak or none), spiral arms (present, how many, how tightly wound), bulge size (none, just noticeable, obvious, dominant), edge-on or not, and odd features such as mergers, irregulars and disturbed galaxies. This matches the labels you listed.
- **Images with labels bundled:** the Kaggle "Galaxy Zoo – The Galaxy Challenge" set has 61,578 labelled 424×424 JPEGs. Each has 37 vote-fraction columns from GZ2. That clears 40k and is the quickest way to start.
- **Full catalogue:** the GZ2 data release (Willett et al. 2013) has the vote counts for the whole sample. You would match it to SDSS cutouts yourself.

**2. Galaxy Zoo DECaLS (DESI Legacy Surveys), about 300k galaxies**
- Its images are deeper and sharper than SDSS, and its question tree is similar. It adds finer merger and disturbance questions and tidal features.
- Releases from Walmsley et al. are mirrored on Hugging Face (look under the `mwalmsley` account, e.g. the `gz_*` datasets) with images and labels together. Check the exact repo names there.

## What to avoid
- **Galaxy10 DECaLS (~17.7k) and Galaxy10 SDSS (~21k):** both are built from volunteer votes, but they are too small. They also collapse the labels into 10 coarse classes, which loses the bar, bulge and arm detail you want.
- **Galaxy Zoo DESI and Euclid releases:** these catalogues mix raw volunteer votes with predictions from the Zoobot model for galaxies that were never classified. If you use them, keep only galaxies with real vote counts. Otherwise you break your human-labels-only rule.

## Practical caveats
- **Labels are vote fractions, not hard classes.** Filter on the number of votes and on a vote-fraction threshold, for example p > 0.8 with at least 10–20 votes on that question. Otherwise you train on noisy labels.
- **Classes are imbalanced.** Mergers and strong bars are rare, so plan for weighting or resampling.
- **Questions depend on earlier answers.** Bar and spiral-arm votes only apply if the galaxy was marked as featured and not edge-on. Apply those parent-question filters.
- **Check the licence and citation terms.** Kaggle competition data comes with its own rules and needs an account. Galaxy Zoo asks you to cite the relevant papers.

If you want one download, take the Kaggle GZ2 set. If you want better image quality and finer merger labels, take GZ DECaLS from Hugging Face.