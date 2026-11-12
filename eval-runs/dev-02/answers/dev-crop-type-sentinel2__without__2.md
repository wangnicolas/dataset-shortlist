I haven't checked these against the live download pages, so the details below come from memory. Licences are the part most likely to be wrong, so check each Zenodo or GitHub record before you commit to a dataset. Sentinel-2 itself is open under Copernicus terms, so the licence that matters is the one on the labels and the packaged product.

## Best fits (S2 time series already paired with crop-type labels)

| Dataset | Labels and coverage | Licence (as I recall) | Where |
|---|---|---|---|
| **PASTIS / PASTIS-R** | France, 2,433 patches of 128×128 px. Parcel-level labels for 18 crop classes. Full-year S2 series. PASTIS-R adds Sentinel-1. | CC BY 4.0 | Zenodo (search "PASTIS-R"). Code is in the GitHub repo `VSainteuf/pastis-benchmark`. |
| **BreizhCrops** | Brittany, France, 2017. About 600k parcels, with S2 L1C and L2A series and about 9 crop classes. It's the standard pixel- or parcel-level time-series benchmark. | Open data based on the French RPG (Licence Ouverte/Etalab), code under MIT. Check the record. | GitHub `dl4sits/BreizhCrops`, with a `pip install breizhcrops` loader. |
| **EuroCropsML** | Estonia, Latvia and Portugal. About 700k parcels with S2 time series, built from EuroCrops labels. It's designed for transfer and few-shot learning. | CC BY 4.0 | Zenodo, with a `eurocropsml` Python package. |
| **S2-Agri** | Île-de-France, 2018. About 190k parcels with S2 pixel sets and 20 classes. | Verify on Zenodo | Linked from `VSainteuf/lightweight-temporal-attention-pytorch`. |
| **Sen4AgriNet** | Catalonia and France, 2019–2020. Very large, with parcel-level labels derived from CAP declarations (EU farm subsidy records). | I believe CC BY 4.0, so verify. | GitHub `Orion-AI-Lab/S4A` |
| **ZueriCrop** | Switzerland, 2019. About 116k fields with a hierarchical label set of up to 48 classes. | Unclear, so check before relying on it. | GitHub `0zgur0/ms-convSTAR` |
| **CropHarvest** | Global point labels with multi-class crop types, plus preprocessed S2, S1 and ERA5 series. Multi-class labels cover a much smaller subset than the binary crop/non-crop labels. | Mostly CC BY-SA 4.0, mixed by sub-dataset | GitHub `nasaharvest/cropharvest`, data on Zenodo |

Outside Europe, look at the Kenya, Ghana, South Sudan and Western Cape (South Africa) crop-type sets that were on Radiant MLHub. They moved to Source Cooperative, and most were CC BY 4.0.

## What I'd pick
- **For segmentation or panoptic parcel work** (U-TAE, Transformers), use **PASTIS-R**. It has the cleanest licence and the most citations, so your results are easy to compare.
- **For pixel or parcel time-series classification** (LSTM, Transformer, TempCNN), use **BreizhCrops**. **EuroCropsML** is a good second dataset for cross-region generalisation.
- **For an added domain-shift or generalisation experiment**, use **CropHarvest** or one of the African sets.

## Licence caveats
- **CC BY** is fine for publishing results and sharing models.
- **CC BY-SA** (CropHarvest) is probably fine for sharing models, but it can oblige you to share derived datasets under the same licence. Check how it applies to your case.
- **EuroCrops** (the harmonised EU parcel labels) is labels only, with no imagery, and its per-country licences vary. Use EuroCropsML instead if you want imagery and labels together.

I can look up the actual licence text on each Zenodo record to confirm the ones I flagged.