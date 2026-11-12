## What I assumed you need
- **R1 (must):** specific crop-type labels (wheat, maize, rapeseed and so on) per parcel or pixel.
- **R2 (must):** Sentinel-2 time series already paired with the labels.
- **R3 (must):** a licence that lets you publish results and share trained models.
- I assumed you want direct downloads you can start on today, with no application process.

## Shortlist
Everything below is a direct download with no account. Registry records for access and licence were checked on 2026-11-11. Class lists and region details are from my memory of the papers unless noted.

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [PASTIS-R](https://zenodo.org/records/5735646) (also S2-only PASTIS, France) | Open download | CC-BY-4.0 | 54 GB | Strong | Registry today; contents from memory |
| 2 | [BreizhCrops](https://zenodo.org/records/14585341) (Brittany, France) | Open download | CC-BY-4.0 | 7.7 GB | Strong | Registry and paper abstract today |
| 3 | [S2-Agri Pixel-Set](https://zenodo.org/records/5815488) and [Patch](https://zenodo.org/records/5815523) | Open download | CC-BY-4.0 | 11 GB each | Strong | Registry today |
| 4 | [EuroCropsML](https://zenodo.org/records/15095445) (Estonia, Latvia, Portugal, 2021) | Open download | CC-BY-SA-4.0 | 4.8 GB | Strong | Registry and paper today |
| 5 | [AgriSen-COG](https://zenodo.org/records/7892012) | Open download | CC-BY-4.0 | 28 GB | Strong (see caveat) | Registry today |
| 6 | [PixelSet-Slovakia](https://doi.org/10.5281/zenodo.21885996) (2020–2025) | Open download | CC-BY-4.0 | 31 GB | Partial | Registry today |
| 7 | [CropHarvest](https://zenodo.org/records/10251170) (global) | Open download | CC-BY-SA-4.0 | 28 GB | Partial | Registry today |
| 8 | [Sen4AgriNet (TACO copy)](https://huggingface.co/datasets/isp-uv-es/sen4agrinet-taco) | Open download | CC-BY-SA-4.0 | 10K–100K samples | Partial | Registry today |

## Details
- **PASTIS-R** is the standard benchmark, with the most published baselines to compare against.
  - It has parcel-level labels for about 18 crop classes (from memory) on S2 time-series patches, plus Sentinel-1.
  - Cite: [Garnot & Landrieu, ICCV 2021](https://doi.org/10.1109/iccv48922.2021.00483).
- **BreizhCrops** has one time series per parcel, so it suits sequence models (LSTM, Transformer, TempCNN) and a master's timeline.
  - It has both top-of-atmosphere and surface-reflectance S2 data, according to the paper abstract.
  - It covers a single region and year, so expect weak generalisation claims.
  - Cite: [Rußwurm et al., 2020](https://doi.org/10.5194/isprs-archives-xliii-b2-2020-1545-2020).
- **S2-Agri** is parcel-based, from one S2 tile in France. It's the dataset behind the Pixel-Set Encoder and Temporal Attention Encoder papers.
- **EuroCropsML** is built for few-shot and transfer experiments across three countries.
  - It uses the EuroCrops harmonised crop taxonomy.
  - Cite: [Reuss et al., Scientific Data 2025](https://doi.org/10.1038/s41597-025-04952-7).
  - **Licence:** CC-BY-SA requires derived *datasets* to stay share-alike. Whether that extends to trained models is unsettled, so ask your supervisor or library before you release weights.
- **AgriSen-COG** is large and covers several countries.
  - The registry text confirms rasterised parcel labels. I did not confirm how the S2 imagery is packaged, so read the linked paper first.
- **PixelSet-Slovakia** is new, with 75k parcel-years across six years, so it's good for cross-year domain adaptation. It has little published baseline work.
- **CropHarvest** is mostly crop vs non-crop. Only a subset has multi-class labels, and the satellite data is pre-extracted features rather than raw pixels.
- **Sen4AgriNet** is a third-party repackaging. Check the original release's terms before relying on the licence shown here.

## Known, not confirmed
- **ZueriCrop** (Switzerland) fits well, but the only copy I found declares CC-BY-NC-4.0. That's a redistribution, so check the original authors' repository before sharing models.
- **Datasets I recalled but could not find in the registries:** DENETHOR (Germany), TimeMatch, Munich480/MTLCC, SICKLE, and the African crop-type sets formerly on Radiant MLHub. Check their project pages before using them. I can't vouch for their access or licence.

## Not recommended, and why
- **[IBM-NASA multi-temporal crop classification](https://huggingface.co/datasets/ibm-nasa-geospatial/multi-temporal-crop-classification):** open, CC-BY-4.0 and well labelled (US CDL), but the imagery is HLS (Harmonized Landsat Sentinel-2), not pure Sentinel-2.
- **CropNet:** built for yield prediction, not crop-type labels.
- **German national crop-type maps (Zenodo):** these are output maps rather than training data paired with S2, and the registry lists them as restricted.

## What I could not find
- Zenodo, DataCite and HuggingFace returned some invalid responses during the searches, so the list may be incomplete.
- I did not read the dataset documentation pages to check class lists and sample counts. Confirm those in each paper.

## Next step
Start with **BreizhCrops** for a quick baseline, then use **PASTIS-R** or **EuroCropsML** for the main results. Before you pick a share-alike dataset, find out what your university requires for releasing model weights.

The interactive page is at `/private/tmp/e-OVwKax/home/cwd/dataset-shortlist.html`.