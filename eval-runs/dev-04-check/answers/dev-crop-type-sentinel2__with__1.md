Several benchmarks fit, and the best ones are open downloads you can start on today. I confirmed each Zenodo and Hugging Face record against its registry on 2026-11-11. Anything marked "memory" is recalled and not confirmed.

## What I assumed you need
- **R1 (must):** specific crop-type labels, not cropland versus non-cropland.
- **R2 (must):** labels at field/parcel or pixel level.
- **R3 (must):** Sentinel-2 time series already paired with the labels.
- **R4 (must):** a licence that lets you publish results and share trained models.
- **R5 (nice to have):** downloadable now, with no application.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | **PASTIS** (and PASTIS-R, which adds Sentinel-1) | open download | CC-BY-4.0 | 28.8 GB (PASTIS-R: 53.7 GB) | strong | today |
| 2 | **EuroCropsML** | open download | CC-BY-SA-4.0 | 4.8 GB | strong | today |
| 3 | **BreizhCrops** | open download | CC-BY-4.0 | 7.7 GB | strong | today |
| 4 | **TimeSen2Crop** | open download | CC-BY-4.0 | 1.1 GB | strong | today |
| 5 | **AgriSen-COG** | open download | CC-BY-4.0 | 28 GB | strong, see caveat | today |
| 6 | **CropHarvest** | open download | CC-BY-SA-4.0 | 27.7 GB | partial | today |
| 7 | **Brazil-Crop** | open download | CC-BY-4.0 | 10.4 GB | partial, contents not checked | today |
| 8 | **Peru multi-annual crop types** | open download | CC-BY-4.0 | 7.2 GB | partial, one small district | today |

## Details
All eight are direct downloads from Zenodo with no account or application. The time to access is minutes.

1. **PASTIS** — https://zenodo.org/records/5012942. It has parcel-level crop labels with Sentinel-2 time series, packaged for panoptic and semantic segmentation. It is the most downloaded benchmark here (about 93,000 downloads). From memory, it covers four regions of France with 18 crop classes. PASTIS-R is at https://zenodo.org/records/5735646. Choose PASTIS-R if you want Sentinel-1 as well.
2. **EuroCropsML** — https://zenodo.org/records/15095445. It has 706,683 parcels across 176 crop classes, with 2021 Sentinel-2 reflectance time series for Latvia, Portugal and Estonia. It is built for few-shot and transnational classification. The values are per-parcel medians, so it suits sequence models but not image segmentation. Dataset paper: doi 10.1038/s41597-025-04952-7.
3. **BreizhCrops** — https://zenodo.org/records/14585341. This is a standard parcel-level time-series benchmark. From memory, it covers Brittany in a single year with a small number of crop groups. The Zenodo record has no description, so check the paper for the class list.
4. **TimeSen2Crop** — https://zenodo.org/records/4715631. It has more than 1 million pixel samples with 16 crop types, covering September 2017 to August 2018. It includes cloud and snow information. From memory, the region is Austria. It is small and quick to start with. Paper: doi 10.1109/jstars.2021.3073965.
5. **AgriSen-COG** — https://zenodo.org/records/7892012. It is a large multi-country crop-type dataset built from farmer-declared parcel records (LPIS). This record holds the parcel labels as rasters. I did not confirm that the Sentinel-2 imagery is in the same record, so check the dataset paper before you plan around it.
6. **CropHarvest** — https://zenodo.org/records/10251170. It is global, with pixel time series. Many of its tasks are crop versus non-crop, and the time series mix Sentinel-2 with other sources. It is best for transfer or few-shot work, not as your main multiclass benchmark.
7. **Brazil-Crop** (https://zenodo.org/records/18461147) and the **Peru dataset** (https://zenodo.org/records/19949051) are recent releases with little independent use so far. I only read their abstracts. They are useful as extra geographies for generalisation tests.

**Licence note for R4.** CC-BY-4.0 lets you publish results and share models with attribution. EuroCropsML and CropHarvest are CC-BY-SA, which is share-alike. Publishing results is fine. Whether the share-alike clause reaches trained model weights is legally unsettled, so ask your supervisor before releasing models trained on those two. If you want no ambiguity, use PASTIS, BreizhCrops or TimeSen2Crop.

## Known, not confirmed
- **Sen4AgriNet** (https://github.com/Orion-AI-Lab/S4A). The GitHub page describes a multi-year, multi-country Sentinel-2 crop benchmark. The files are hosted on Dropbox, Google Drive and Hugging Face. The page states no licence, so check the paper before relying on it.
- **ZueriCrop** (Switzerland). I could not find an official data record. The GitHub repo I tried is a model repository, not the dataset.
- **DENETHOR, TimeMatch, SICKLE** and similar datasets were not checked in this session.

## Not recommended, and why
- **EuroCrops** (https://zenodo.org/records/14094196). It has excellent parcel labels for 16 EU countries but no imagery. You would have to build the Sentinel-2 pipeline, which you want to avoid. EuroCropsML is the ready-made version.
- **IBM-NASA multi-temporal-crop-classification** (Hugging Face). It is open and CC-BY-4.0, but the imagery is Harmonized Landsat-Sentinel at 30 m over the US, not native Sentinel-2.
- **CROPSIGHT-US**. It contains ground-truth labels only, not a packaged time-series benchmark.

## What I could not find
There is no single open benchmark that combines many countries, many crop classes, and native Sentinel-2 patches with spatial context. PASTIS covers the patch-based case for France. EuroCropsML covers the transnational time-series case.

## Next step
For a first experiment, download TimeSen2Crop (1.1 GB). Then move to PASTIS or EuroCropsML for the main results. Use BreizhCrops for a second region.

The interactive comparison page is `/private/tmp/e-gJpNV8/home/cwd/dataset-shortlist.html`.