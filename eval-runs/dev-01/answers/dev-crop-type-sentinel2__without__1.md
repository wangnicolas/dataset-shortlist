I'm working from memory and haven't checked the live pages. Confirm each licence on the dataset's own page before you commit to it, because some hosts have moved (Radiant MLHub, for example, migrated to Source Cooperative).

## Best fits

| Dataset | Coverage / labels | S2 pairing | Licence (as I recall) | Where |
|---|---|---|---|---|
| **PASTIS / PASTIS-R** | France, 2,433 patches of 128×128 px, with parcel-level semantic and panoptic labels for 18 crop classes plus background | Full-year S2 time series per patch (PASTIS-R adds S1) | CC-BY 4.0 | Zenodo (search "PASTIS"), github.com/VSainteuf/pastis-benchmark |
| **BreizhCrops** | Brittany, France, about 600k parcels with parcel-level labels (a few dozen classes in the raw data, with a smaller harmonised subset) | Per-parcel S2 time series (L1C and L2A) ready to load | Code is MIT. Labels derive from the French RPG, under Etalab Open Licence, which is CC-BY-compatible. | github.com/dl4sits/BreizhCrops (it has a pip package and a data downloader) |
| **EuroCropsML** | Estonia, Latvia and Portugal, with harmonised EuroCrops labels | Parcel-level S2 time series | CC-BY 4.0 | Zenodo (search "EuroCropsML") |
| **CropHarvest** | Global point labels, with crop-type labels for a subset | 12-month S2 time series, plus S1 and ERA5 | CC-BY-SA 4.0 on much of it | github.com/nasaharvest/cropharvest, Zenodo |

## Others worth checking

- **Sen4AgriNet** covers Catalonia and France, with parcel-level labels from LPIS data and S2 time series (github.com/Orion-AI-Lab/S4A). I believe it is CC-BY.
- **ZueriCrop** covers Switzerland, with about 48 crop classes and S2 time series, on the ETH Research Collection.
- **TimeMatch** covers several European regions, so it is useful for domain-shift and transfer experiments (Zenodo).
- **Munich480** covers Munich, with 27 classes, but the licence is unclear to me.
- **AgriFieldNet** (India), **South Africa Crop Type** and **DENETHOR** (Germany) were on Radiant MLHub, and I believe all three are CC-BY 4.0.

## Recommendations

- **Pixel- or parcel-sequence classification** (the standard time-series setup): use **BreizhCrops** first. It's the lightest to set up and widely benchmarked.
- **Spatial or semantic segmentation of fields**: use **PASTIS-R**. It has established baselines (U-TAE, for example), so you can compare against published numbers.
- **Generalisation across regions or years**: add **EuroCropsML** or **TimeMatch**. Use **CropHarvest** if you want a global, multi-region test.

## Licence notes

- CC-BY 4.0 lets you publish results and share trained models, as long as you give attribution. That covers PASTIS and EuroCropsML.
- CC-BY-SA (CropHarvest) requires share-alike on derivatives of the data. Whether that applies to model weights is legally unsettled, so if you want a simple position, use CC-BY datasets for the main experiments.
- Sentinel-2 imagery is free and open under Copernicus terms. The label source's licence is what matters in practice, and it is usually the national LPIS/RPG one.
- Some datasets cite or build on others. Check the licence of each source if you combine them.

I can look up the current licence text and download links for any of these if you tell me which ones you're leaning towards.