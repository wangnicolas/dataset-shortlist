I'm answering from memory and haven't checked the live pages. Licences and hosting change, and some licences are stated differently on the paper, the repo and the data host. Check each licence on the data page before you rely on it.

## Best fits

| Dataset | Region / scale | What you get | Licence (as I recall) | Where |
|---|---|---|---|---|
| **PASTIS / PASTIS-R** | France, 2,433 patches of 128×128 px, about 124k parcels | S2 time series (10 bands, about 35–70 dates per patch in 2019). PASTIS-R adds S1. 18 crop classes plus background. Gives parcel instance masks, so it works for semantic or panoptic tasks. | CC-BY 4.0 | Zenodo ("PASTIS"), `VSainteuf/pastis-benchmark` on GitHub |
| **EuroCropsML** | Estonia, Latvia and Portugal, about 700k parcels | Parcel-level S2 time series already matched to EuroCrops labels, with a few-shot and transfer-learning setup. Many classes, from the HCAT taxonomy. | CC-BY 4.0 | Zenodo, `dida-do/eurocropsml` on GitHub |
| **BreizhCrops** | Brittany, France, about 600k parcels | Pixel-averaged S2 time series per field (L1C and L2A) with crop labels. A good fit for parcel-level time-series models like Transformers and LSTMs. | Check Zenodo and the repo | `dbuscombe-usgs/breizhcrops` successor at `dl4sits/BreizhCrops`, Zenodo |
| **ZueriCrop** | Canton of Zurich, Switzerland, about 116k parcels | S2 time series with a hierarchical crop taxonomy (48 classes). Used for instance segmentation. | Check the repo | `0zgur0/ms-convSTAR` on GitHub |
| **Sen4AgriNet** | Catalonia and France, 2019–2020 | S2 time series built from CAP declarations. Many classes in a hierarchy, with patch-level and parcel-level labels. | Check the repo | `Orion-AI-Lab/S4A` on GitHub |
| **CropHarvest** | Global, about 90k points | Labelled points, each paired with S2, S1, weather and elevation. It has a binary crop/non-crop label and a multiclass crop type label. The label coverage is uneven. | Labels come from many sources and are mostly CC-BY-SA 4.0 | Zenodo, `nasaharvest/cropharvest` on GitHub |

## If you want other regions or smallholder settings
- **AgriFieldNet (India)** has multi-temporal S2 with field-level labels. **Western Cape / South Africa crop type** and the Kenya, Ghana, Zambia and Tanzania sets are also relevant. Most were on Radiant MLHub, which has moved to Source Cooperative (source.coop), so search both. Several are CC-BY 4.0, but licences differ by dataset.
- **GEO-Bench** (`m-SA-crop-type`, `m-cashew-plant`) is a ready-made benchmark with standard splits and comparable baselines.
- **PANGAEA** bundles PASTIS and other crop sets behind one loader.

## Notes on licences
- **CC-BY 4.0** is the safest option. You can publish results and share trained models as long as you cite the dataset.
- **CC-BY-SA** (CropHarvest labels, and some EuroCrops-derived data) is more awkward. Whether a trained model counts as an "adaptation" is legally unsettled. Ask your supervisor or your university's data office before releasing weights trained on SA data.
- **Labels from official sources** (the CAP/LPIS parcel data behind EuroCrops, BreizhCrops and Sen4AgriNet) come from open-government data, but the dataset packagers set the licence you actually inherit. Read the dataset's own licence statement.
- **Sentinel-2 imagery** itself is free and open under Copernicus terms, so it doesn't restrict you.

## Recommendation
Start with **PASTIS-R**. It has a clean licence, strong published baselines (U-TAE, TSViT and others), and a patch format that works for both pixel-wise and parcel-wise classification. Add **EuroCropsML** or **BreizhCrops** if you need a larger parcel-level time-series set, or a second region to test generalisation.

I can browse the dataset pages and confirm the exact licence text for your shortlist if you'd like.