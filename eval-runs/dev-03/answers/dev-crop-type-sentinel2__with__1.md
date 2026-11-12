## What I assumed you need

- **R1 (must):** specific crop-type labels (wheat, maize, rapeseed and so on) at field or pixel level.
- **R2 (must):** multi-temporal Sentinel-2 data already paired with the labels.
- **R3 (must):** a licence that lets you publish results and share trained models.
- Downloadable today, no application.

## Shortlist

All rows were checked against the Zenodo or Hugging Face registry record on 2026-11-11, except the fit notes marked "recalled".

| # | Dataset | Access | Licence | Fit |
|---|---|---|---|---|
| 1 | EuroCropsML | Open download, minutes | CC-BY-SA-4.0 | Strong |
| 2 | BreizhCrops | Open download, minutes | CC-BY-4.0 | Strong |
| 3 | TimeSen2Crop | Open download, minutes | CC-BY-4.0 | Strong |
| 4 | PASTIS | Open download, minutes | CC-BY-4.0 | Strong |
| 5 | AgriSen-COG | Open download, minutes | CC-BY-4.0 | Strong |
| 6 | S2-Agri (Pixel-Set) | Open download, minutes | CC-BY-4.0 | Strong |
| 7 | Sen4AgriNet (Hugging Face copy) | Open download, minutes | CC-BY-SA-4.0 | Partial |
| 8 | CropHarvest | Open download, minutes | CC-BY-SA-4.0 | Partial |

## Details

- **EuroCropsML** (https://zenodo.org/records/15095445)
  - It has 706,683 parcels across 176 crop classes in Estonia, Latvia and Portugal.
  - Each parcel has a median Sentinel-2 L1C time series, and there are ready-made splits.
  - The data are parcel aggregates, not image patches.
  - Paper: Nature Scientific Data 2025, doi 10.1038/s41597-025-04952-7.
- **BreizhCrops** (https://zenodo.org/records/14585341)
  - Field-level labels for Brittany, France, with Sentinel-2 top-of-atmosphere and bottom-of-atmosphere time series.
  - A GitHub repository has baselines and pretrained weights.
  - The paper compares seven deep networks and a random forest: doi 10.5194/isprs-archives-xliii-b2-2020-1545-2020.
- **TimeSen2Crop** (https://zenodo.org/records/4715631)
  - It has over 1 million labelled pixel time series covering 16 crop types over one agronomic year.
  - Paper: doi 10.1109/jstars.2021.3073965.
  - It covers one region and one year.
- **PASTIS** (https://zenodo.org/records/5012942)
  - Parcel-level labels with Sentinel-2 patch time series over France, suited to segmentation.
  - Contents are from memory.
- **AgriSen-COG** (https://zenodo.org/records/7892012)
  - A multi-country benchmark (Austria, Belgium, Spain, Denmark, the Netherlands) with labels from farmers' parcel declarations (LPIS).
  - The Zenodo record title says "LPIS.GT", so it may hold only the labels. Check where the imagery is hosted.
  - Paper: doi 10.3390/rs15122980.
- **S2-Agri Pixel-Set** (https://zenodo.org/records/5815488): Sentinel-2 pixel sets with crop labels. A Patch version is at https://zenodo.org/records/5815523. Contents are from memory.
- **Sen4AgriNet** (https://huggingface.co/datasets/isp-uv-es/sen4agrinet-taco)
  - A multi-country benchmark with LPIS labels, repackaged by a third party.
  - Confirm it against the original release before citing it.
  - Original paper: doi 10.1109/jstars.2022.3164771.
- **CropHarvest** (https://doi.org/10.5281/zenodo.10251170): global, with pre-computed time series. Most labels are crop versus non-crop, so it only partly meets R1.

**Licences and sharing models (R3):** CC-BY lets you publish results and share models with attribution. For the CC-BY-SA datasets (EuroCropsML, Sen4AgriNet copy, CropHarvest), share-alike clearly applies to redistributed data. Whether it applies to trained weights is unsettled, so check it with your supervisor if you plan to release models. CC-BY (BreizhCrops, TimeSen2Crop, PASTIS, AgriSen-COG, S2-Agri) avoids that question.

## Known, not confirmed

- **S4A-CyL** (Sentinel-2 time series from Castilla y León, https://doi.org/10.71486/q4yz-p373): the DOI resolves, but the registry didn't state the licence or access tier. Read the landing page first.
- **Peru Andes crop-type time series** (https://zenodo.org/records/19949051): the Zenodo record is open under CC-BY-4.0, but I didn't check its labels or crop classes.

## Not recommended, and why

- **ZueriCrop** has a CC-BY-NC-4.0 licence, so non-commercial only. That is a risk for sharing models.
- **EuroCrops** is the harmonised parcel labels without Sentinel-2 series. EuroCropsML is its paired version.

## What I could not find

Zenodo and DataCite returned truncated responses on some queries, so the list may be incomplete. I didn't read the PASTIS, AgriSen-COG or S2-Agri pages, so their contents and size are recalled. I didn't look for baseline papers for most datasets.

## Next step

Start with BreizhCrops or EuroCropsML. Both are open, small enough to try this week, and have published baselines to compare against.

Interactive page: `/private/tmp/e-IjqjAD/home/cwd/dataset-shortlist.html`