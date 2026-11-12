**Download Galaxy Zoo DESI from Hugging Face (`mwalmsley/gz_desi`).** It meets every requirement: about 399k galaxies, images bundled with the labels, and the labels are raw volunteer vote counts per answer.

I checked the dataset listings and cards online today, but did not download or open the image files themselves.

| Dataset | Galaxies | Size | Labels |
|---|---|---|---|
| `mwalmsley/gz_desi` | 399,413 | ~17.5 GB | bar (none/weak/strong), spiral arms, bulge size (5 levels), merging (none/minor disturbance/major disturbance/merger), plus edge-on, arm count and winding |
| `mwalmsley/gz2` | 191,174 (172,377 train / 18,797 test) | ~2.6 GB | bar, spiral arms, arm count, winding, bulge size, roundedness, "something odd" — no merger column |

Pick `gz_desi` if mergers matter. If you want something lighter and can live without merger labels, `gz2` is the classic SDSS benchmark and a seventh of the download.

```python
from datasets import load_dataset
ds = load_dataset("mwalmsley/gz_desi", split="train")   # name="tiny" for a 1% subset to prototype
```

Both are ungated and free, with a fixed train/test split.

Things to know before you commit:

- **Licence:** CC-BY-NC-SA 4.0, and the curator additionally requires that models trained on the data be released as source code by publication. That is fine for a thesis, but you will need to publish your code.
- **Vote counts vary by question:** volunteers answer a decision tree, so "bar?" is only asked of those who said "featured, not edge-on". Filter on the `*_total-votes` columns or use a vote-count-aware loss rather than a plain argmax.
- **Three campaigns in DESI:** the columns are suffixed `dr12`, `dr5` and `dr8`, with slightly different answer sets (for example, bar is yes/no in `dr12` but none/weak/strong in `dr5` and `dr8`). Each galaxy only has votes from its own campaign; `dr5` and `dr8` have the richer schema.
- **Avoid lookalikes:** the Galaxy Zoo DESI and DECaLS catalogues on Zenodo also ship model-predicted morphologies for millions of galaxies, which would break your human-labels rule. The Hugging Face columns above are volunteer counts according to the dataset card.

Two others I ruled out: Galaxy10 DECaLS is only about 17.7k images with 10 coarse classes (figure from memory), and `mwalmsley/gz_evo` (806k galaxies, 540 label columns across five campaigns and telescopes) is more than a master's CNN needs.