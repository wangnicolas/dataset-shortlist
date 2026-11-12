## What I assumed you need

- **R1 (must):** Crop-specific labels (wheat, maize, rapeseed and so on) per parcel or pixel.
- **R2 (must):** Sentinel-2 time series already paired with the labels and ready to use.
- **R3 (must):** A licence that lets you publish results and share trained models.
- **R4 (nice to have):** An established benchmark with published baselines.

I assumed a European or global setting is fine. I checked on 12 Nov 2026.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | PASTIS | Open download, minutes | CC-BY-4.0 | 28.8 GB | Strong | Record today; class details from memory |
| 2 | BreizhCrops | Open download, minutes | CC-BY-4.0 | 7.7 GB | Strong | Today |
| 3 | EuroCropsML | Open download, minutes | CC-BY-SA-4.0 | 4.8 GB | Strong | Today |
| 4 | S2-Agri (Pixel-Set; Patch also available) | Open download, minutes | CC-BY-4.0 | 10.8 GB | Strong | Record today; contents from memory |
| 5 | Sen4AgriNet (Hugging Face) | Open download, minutes | CC-BY-SA-4.0 | Large, not stated | Strong | Record today; contents from memory |
| 6 | AgriSen-COG | Open download, minutes | CC-BY-4.0 | 28 GB | Partial | Today |
| 7 | CropHarvest | Open download, minutes | CC-BY-SA-4.0 | Not stated | Partial | Record today; contents from memory |

All seven records exist and their licences come from the registry records. "Today" means the registry record was read. "From memory" means I recalled the content details (classes, regions) and did not re-read them.

## Details

- **PASTIS** (https://zenodo.org/records/5012942):
  - It holds S2 time-series patches over French agricultural parcels with crop-type labels.
  - From memory, it has 18 classes.
  - It is the standard benchmark for parcel segmentation. You can derive per-parcel classification from it.
- **BreizhCrops** (https://zenodo.org/records/14585341):
  - It has per-parcel S2 time series (top-of-atmosphere and bottom-of-atmosphere) for Brittany.
  - The paper compares seven deep networks and a Random Forest baseline.
  - Loaders and pretrained weights are at github.com/dl4sits/breizhcrops, as named in the paper abstract.
  - It covers one region and one year.
  - Paper: doi 10.5194/isprs-archives-xliii-b2-2020-1545-2020.
- **EuroCropsML** (https://zenodo.org/records/15095445):
  - It has 706,683 labelled parcels over 176 crop classes in Latvia, Portugal and Estonia, with per-parcel median S2 L1C series for 2021.
  - It has the most classes of any option here.
  - Papers: doi 10.1038/s41597-025-04952-7 (dataset paper) and doi 10.1016/j.ophoto.2026.100117 (benchmark study).
- **S2-Agri** (https://zenodo.org/records/5815488; patch version https://zenodo.org/records/5815523):
  - It is parcel-based crop classification with S2 series.
  - The record text is brief. From memory it covers France and one season with about 20 classes, so read the related article first.
- **Sen4AgriNet** (https://huggingface.co/datasets/isp-uv-es/sen4agrinet-taco):
  - From memory, it is a very large multi-year dataset with about 168 declared-crop classes, covering Catalonia and France. Read the dataset card before downloading.
- **AgriSen-COG** (https://zenodo.org/records/7892012):
  - This record holds the rasterised LPIS ground-truth tiles.
  - I did not confirm whether the paired S2 imagery is in this record or a separate one.
- **CropHarvest** (DOI 10.5281/zenodo.10251170):
  - It has pre-extracted satellite time series, but most labels are crop versus non-crop. A smaller multi-class subset exists, from memory.
  - It is only a partial fit for your multi-class goal.

**Licences and your goal of publishing results and sharing models:**
- **CC-BY-4.0** (PASTIS, BreizhCrops, S2-Agri, AgriSen-COG): attribution only, so there are no problems.
- **CC-BY-SA-4.0** (EuroCropsML, Sen4AgriNet, CropHarvest): share-alike applies to the data and to datasets derived from it. Publishing results and models is normally fine. If you plan to release a derived dataset, it must carry the same licence. Check this with your supervisor.

## Known, not confirmed

- **TimeSen2Crop** (Austria, about 1M labelled S2 samples, 16 crop classes from memory):
  - The paper DOI resolves (10.1109/JSTARS.2021.3073965) and OpenAIRE lists CC-BY-4.0.
  - I did not find the data record itself, so check the paper's data link.
- **Peru, multi-annual S2 crop dataset** (https://zenodo.org/records/19949051): CC-BY-4.0 and verified, but a single district. It is only useful as a small extra test region.

## Not recommended, and why

- **ZueriCrop:** the Hugging Face copy is CC-BY-NC-4.0. I could not confirm the original terms, and the non-commercial clause may block sharing models.
- **IBM/NASA multi-temporal crop classification:** it uses Harmonized Landsat-Sentinel imagery with US CDL labels, not pure S2.
- **EuroCrops (labels only):** it has no imagery. EuroCropsML is the version with S2 attached.
- **National crop maps for Germany (Zenodo 6451848):** these are derived maps, access is by application, and no licence is stated.

## What I could not find

- TimeMatch, DENETHOR, Munich480, AI4Boundaries and SICKLE returned nothing usable from the registries, so I did not evaluate them.
- The Datacite and Zenodo searches failed intermittently, so the list may be incomplete.
- The literature lookup for PASTIS returned unrelated papers, so I list no paper for PASTIS, S2-Agri, Sen4AgriNet or CropHarvest.

## Next step

You can start today with **BreizhCrops** or **EuroCropsML**. Both are small, open, ready-made time series with baselines, and they suit a master's timeline. For a second benchmark with more spatial structure, add **PASTIS**.

The interactive page is at `/private/tmp/e-yrE7eT/home/cwd/dataset-shortlist.html`.