## What I assumed you need
- **R1 (must):** labels for specific crop types (wheat, maize, rapeseed and so on) per field or pixel.
- **R2 (must):** ready-made multi-temporal Sentinel-2 data already paired with those labels, so you don't build a pipeline.
- **R3 (must):** a licence that lets you publish results and share trained models.
- I assumed you want something you can download now, not something behind an application.

## Shortlist
Every dataset here is a direct download with no account or application. The registry record confirmed the licence on 2026-11-11, except where the table says otherwise.

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PASTIS (France, parcel patches) | Direct download, minutes | CC-BY-4.0 | 28.8 GB | Strong | Today |
| 2 | EuroCropsML (Europe, per-parcel series) | Direct download, minutes | CC-BY-SA-4.0 | Not recorded | Strong | Today |
| 3 | BreizhCrops (Brittany, about 600k parcels) | Direct download, minutes | CC-BY-4.0 | Not recorded | Strong | Partly: the registry lookup failed, so the licence comes from the search record |
| 4 | TimeSen2Crop (Austria, 16 crops, pixels) | Direct download, minutes | CC-BY-4.0 | about 1 GB | Strong | Today |
| 5 | AgriSen-COG (AT, BE, ES, DK, NL) | Direct download; check which parts are on Zenodo | CC-BY-4.0 | Large | Strong | Today (label part) |
| 6 | Sen4AgriNet, TACO repackaging (Catalonia and France) | Direct download from Hugging Face | CC-BY-SA-4.0 | 10,013 patches | Strong | Today |
| 7 | CropHarvest (global) | Direct download, minutes | CC-BY-SA-4.0 | Not recorded | Partial | Today |
| 8 | Brandenburg-S12-CropVal | Direct download, minutes | CC-BY-4.0 | Not recorded | Partial | Today |
| 9 | Peru multi-annual S2 crop dataset (2026) | Direct download, minutes | CC-BY-4.0 | Not recorded | Partial | Today |
| 10 | IBM/NASA multi-temporal crop classification (US) | Direct download, minutes | CC-BY-4.0 | Not recorded | Partial | Today |

## Details

**1. PASTIS** (https://zenodo.org/records/5012942)
- It has parcel-level Sentinel-2 time series patches for France, with crop-type semantic and instance labels. It's the most used benchmark of this kind, with about 93k Zenodo downloads.
- From memory, not confirmed: it has 18 crop classes, and a companion repository holds the code and splits.
- Download the 28.8 GB zip from the record page.
- It is in patch (segmentation) format rather than pixel tables, so you may need to convert it for pixel-wise or parcel-wise models.

**2. EuroCropsML** (https://zenodo.org/records/15095445)
- Per-parcel median Sentinel-2 L1C time series with 176 crop classes and 706,683 labelled points. Both figures come from the paper abstract. It was built for few-shot transfer across countries.
- It is CC-BY-SA, so derivatives must stay share-alike. Whether a trained model counts as a derivative is legally unsettled, so ask your supervisor or library.
- The data are per-parcel medians, so there is no spatial context.
- Papers that used it:
  - The dataset paper: https://doi.org/10.1038/s41597-025-04952-7
  - A 2026 baselines paper: https://doi.org/10.1016/j.ophoto.2026.100117

**3. BreizhCrops** (https://zenodo.org/records/14585341)
- Parcels in Brittany with both top-of-atmosphere and bottom-of-atmosphere Sentinel-2 series. The paper abstract says reference models, pretrained weights and a GitHub repository (dl4sits/breizhcrops) come with it.
- From memory: one region and one year (2017).
- The dataset paper compares seven deep networks and a random forest baseline, so you get ready comparisons: https://doi.org/10.5194/isprs-archives-xliii-b2-2020-1545-2020

**4. TimeSen2Crop** (https://zenodo.org/records/4715631)
- More than 1 million pixel samples for 16 crop types, September 2017 to August 2018. Atmospherically corrected, with cloud, snow and shadow flags.
- The download is about 1 GB, and it has about 2.8k Zenodo downloads. This is the easiest one to start with.
- From memory: the area is Austria.
- Paper: https://doi.org/10.1109/jstars.2021.3073965

**5. AgriSen-COG** (https://zenodo.org/records/7892012)
- It has Sentinel-2 cloud-optimised GeoTIFFs for five countries, labelled from farmer declarations (LPIS).
- The Zenodo record I verified holds the label part. Check the paper for where the imagery lives.
- Paper: https://doi.org/10.3390/rs15122980

**6. Sen4AgriNet, TACO repackaging** (https://huggingface.co/datasets/isp-uv-es/sen4agrinet-taco)
- It has 10,013 Sentinel-2 patches over Catalonia and France for 2019–2020, with 168 harmonised crop and land-cover classes.
- This is a third-party repackaging with a split the repackager constructed, not the original authors' release. The card says to follow the original licence, and I haven't checked that one.
- Original paper: https://doi.org/10.1109/jstars.2022.3164771

**7. CropHarvest** (https://doi.org/10.5281/zenodo.10251170)
- Global labels with time series. From memory, most labels are crop versus non-crop, with a multiclass subset. Check how many specific-crop labels you get before committing.

**8–10. Brandenburg-S12-CropVal, Peru, IBM/NASA**
- Brandenburg-S12-CropVal (https://zenodo.org/records/18632974):
  - It is a Sentinel-1/2 cropland segmentation set for cross-regional transfer.
  - I haven't read its class list, so I don't know whether the labels are specific crops.
- Peru (https://zenodo.org/records/19949051):
  - Multi-annual Sentinel-2 crop type data, new in 2026, with no papers using it yet.
  - I haven't read its class list.
- IBM/NASA (https://huggingface.co/datasets/ibm-nasa-geospatial/multi-temporal-crop-classification):
  - This is a US dataset built from HLS imagery, which is a 30 m Landsat–Sentinel-2 composite, not native 10 m Sentinel-2.
  - From memory, it has 13 classes.

**On licences (R3).** All the licences above allow publishing results. Plain CC-BY (PASTIS, BreizhCrops, TimeSen2Crop, AgriSen-COG, and the Brandenburg, Peru and IBM/NASA sets) is the safest for sharing trained models. The CC-BY-SA datasets (EuroCropsML, Sen4AgriNet, CropHarvest) are fine for results. For released models, check how your university treats share-alike. If you want no ambiguity, start with 1, 3 or 4.

## Known, not confirmed
- **ZueriCrop:** the Hugging Face copy (https://huggingface.co/datasets/isaaccorley/zuericrop) is CC-BY-NC-4.0. I didn't check the original release or licence. A non-commercial licence may complicate sharing models.
- **Original Sen4AgriNet release (GitHub):** I didn't check its home page or licence.
- **S2Agri / PixelSet:** Hugging Face copies exist under monster-monash (CC-BY-4.0), but I didn't check the original home or access terms.
- **DENETHOR (Germany):** I searched for it but didn't confirm a record, so I can't say where it lives now.

## Not recommended, and why
- **EuroCrops:** parcel labels only, with no imagery. EuroCropsML is the version paired with Sentinel-2.
- **CropNet:** county-level yield prediction, not field or pixel crop type.
- **Hugging Face ZueriCrop copy:** non-commercial licence, as noted above.

## What I could not find
- Zenodo and DataCite failed intermittently during the search, so coverage may be incomplete.
- I didn't confirm the sizes of several entries, and I didn't get class lists for the three partial-fit datasets.
- Everything marked "from memory" above was not confirmed today.

## Next step
Download TimeSen2Crop (about 1 GB) and BreizhCrops first and get a baseline running. Then add PASTIS or EuroCropsML if you want spatial context or cross-country transfer. Before you commit to a dataset, open the dataset page or paper to confirm the class list and licence, because these were checked on 2026-11-11 and can change.

The interactive page is at `/private/tmp/e-W4YHCE/home/cwd/dataset-shortlist.html`.