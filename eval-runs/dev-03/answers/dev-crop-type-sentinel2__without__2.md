These are the datasets I'd shortlist. I'm working from memory and haven't checked the live pages, so confirm the licence and format on each download page before you commit. Check especially anything marked "verify".

## Best fits (crop-type labels already paired with Sentinel-2 time series)

| Dataset | Region / labels | Unit | Licence | Where |
|---|---|---|---|---|
| **PASTIS / PASTIS-R** | France, 18 crop classes plus background, about 2,400 patches of 128×128 px, 30–60 S2 dates each. PASTIS-R adds Sentinel-1. | Parcel-level panoptic and semantic labels | CC BY 4.0 | Zenodo (search "PASTIS"); code and baselines (U-TAE) at `github.com/VSainteuf/pastis-benchmark` |
| **BreizhCrops** | Brittany, France, about 600k field parcels. S2 L1C and L2A time series, with 9 main crop classes in the standard setup. | Field-averaged time series (good for LSTM, transformer or TempCNN) | Verify. Labels come from the French LPIS, which is open (Etalab licence), and the code is MIT. | `github.com/dl4sits/BreizhCrops`, data on Zenodo, and a PyTorch loader that downloads it for you |
| **EuroCropsML** | Estonia, Latvia and Portugal, many crop classes from the EuroCrops HCAT taxonomy, with S2 time series ready to use | Parcel-level | Likely CC BY 4.0 (verify) | Zenodo, with a Python package |
| **ZueriCrop** | Zurich and Thurgau, Switzerland, about 48 crop classes, about 116k parcels, S2 time series | Parcel-level instance and semantic labels | Verify. Not all datasets in this area are CC BY. | `github.com/0zgur0/ms-convSTAR` (links to the data) |
| **Sen4AgriNet** | Catalonia and France, 2019–2020, hierarchical crop labels from CAP declarations, S2 time series | Parcel-level | Verify. I believe it is open. | GitHub and Zenodo (search "Sen4AgriNet") |

## Related, but less direct
- **CropHarvest** is global and multi-source, but mostly binary crop vs. non-crop. Only a subset has crop-type labels. It is CC BY-SA 4.0, which is share-alike. Check how that affects the models and data you release.
- **EuroCrops** has harmonised LPIS labels across the EU but no imagery. You would have to build the S2 pairing yourself, which is exactly what you want to avoid.
- **TimeMatch** is useful if you want to study domain shift across regions and years.
- **African crop-type datasets** (Kenya, Ghana, Tanzania, South Africa) have moved from Radiant MLHub to **Source Cooperative**. They are typically CC BY 4.0, but each one differs.

## Recommendation
1. **Start with PASTIS-R.** It is the most widely used benchmark, so your results are directly comparable with published numbers. It is CC BY 4.0, which allows publishing results and sharing trained models with attribution. Baselines and loaders are included.
2. **Add BreizhCrops or EuroCropsML** if you want a pixel- or parcel-level time-series setup, or a second region to test generalisation. Both are larger and simpler to load than PASTIS.

## Licence caveats
- **Attribution (CC BY):** you can publish results and release model weights. Cite the dataset and keep the credit.
- **Share-alike (CC BY-SA):** this applies to adapted datasets. Whether it extends to trained model weights is legally unsettled. If you want a clean release, prefer CC BY datasets.
- **Underlying label sources:** the LPIS and CAP data come from national agencies, and their terms are separate from the dataset's licence. Read the "licence" section of each Zenodo record.
- **Sentinel-2 imagery:** this is free and open under the Copernicus terms.

I can check the exact licences and download links on the live pages if you'd like.