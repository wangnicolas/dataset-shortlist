**Download Galaxy Zoo 2 from Hugging Face (`mwalmsley/gz2`)**: it meets every requirement except a merger label, which needs one extra join or the alternative dataset below.

- **Size:** about 191k SDSS galaxies (172,377 train / 18,797 test), a 2.6 GB download.
- **Bundling:** images and labels are together in Parquet, so there is no cross-matching to do.
- **Labels:** raw volunteer vote counts, totals and fractions for each question, not model output.
- **Questions covered:** bar, spiral arms (presence, winding, arm count), bulge size, bulge shape, edge-on, roundedness and "something odd".
- **License:** CC BY-NC-SA 4.0, which is fine for a thesis; cite Willett et al. 2013 and SDSS.

```python
from datasets import load_dataset
ds = load_dataset("mwalmsley/gz2")
```

**The merger gap:** this version has no merger column, only "something odd" yes/no. In the original GZ2 survey, merger was a follow-up answer to that question. The original GZ2 vote tables on data.galaxyzoo.org should carry it and can be joined by galaxy ID, but I did not check those tables.

**If mergers are central to the thesis, use Galaxy Zoo DECaLS instead** (Zenodo record 4573248, CC BY 4.0, Walmsley et al. 2022):

- **Merger question:** from memory, it has a dedicated one (none / minor disturbance / major disturbance / merger) and splits bars into strong and weak; I did not open the schema to confirm.
- **Images:** deeper than SDSS, so faint features are more visible.
- **Download size:** the image zips total about 104 GB.
- **Lighter route:** the `galaxy-datasets` Python package (`from galaxy_datasets import gz_decals_5`) offers the GZD-5 subset of about 230k galaxies with volunteer labels; I did not check its download size.
- **Vote depth:** many GZD-5 galaxies have only about 5 votes, so filter on total votes or use a loss that accounts for vote counts.

**What to avoid given your human-labels rule:**

- **`gz_decals_auto_posteriors`** in the same Zenodo record: these are CNN predictions. Use only the `gz_decals_volunteers_*` files.
- **Galaxy Zoo DESI** (8.7M galaxies): from memory, the labels are overwhelmingly model predictions.
- **Debiased GZ2 fractions:** they are still volunteer-derived, but the redshift correction is a statistical adjustment, so train on raw counts if you want pure votes.

Whichever you pick, use the vote fractions as soft targets or threshold them yourself. Later questions such as bar were only asked of volunteers who answered "featured" earlier, so check the per-question vote totals before trusting a fraction.

Sources:
- [mwalmsley/gz2 on Hugging Face](https://huggingface.co/datasets/mwalmsley/gz2)
- [Galaxy Zoo DECaLS on Zenodo](https://zenodo.org/records/4573248)
- [galaxy-datasets on GitHub](https://github.com/mwalmsley/galaxy-datasets)