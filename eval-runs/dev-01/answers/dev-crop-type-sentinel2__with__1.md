## What I assumed you need
- **R1:** specific crop-type labels (wheat, maize, rapeseed and so on) per field or pixel.
- **R2:** paired multi-temporal Sentinel-2 data.
- **R3:** a licence that lets you publish results and share trained models.
- **R4:** ready to use, with no download or preprocessing pipeline of your own.
- **Assumption:** you want open downloads you can start on today. All seven below are direct downloads with no account, and each took only a registry-record check.

## Shortlist
Registry records were checked on 2026-11-11.

| # | Dataset | Access | Licence | Size | Fit |
|---|---|---|---|---|---|
| 1 | TimeSen2Crop | Direct download, minutes | CC-BY-4.0 | 28 GB | Strong |
| 2 | EuroCropsML | Direct download, minutes | CC-BY-SA-4.0 | 4.8 GB | Strong |
| 3 | BreizhCrops | Direct download, minutes | CC-BY-4.0 | 7.7 GB | Strong |
| 4 | AgriSen-COG | Direct download, minutes | CC-BY-4.0 | 28 GB | Strong, with a caveat |
| 5 | PASTIS | Direct download, minutes | CC-BY-4.0 | 29 GB | Strong, for segmentation |
| 6 | S2-Agri (Pixel-Set) | Direct download, minutes | CC-BY-4.0 | 11 GB | Partial |
| 7 | CropHarvest | Direct download, minutes | CC-BY-SA-4.0 | 28 GB | Partial |

## Details
1. **TimeSen2Crop.** Download: https://doi.org/10.5281/zenodo.18681321
   - It has about 1.1 million pixel-level Sentinel-2 series with 16 crop types, one agronomic year, atmospherically corrected, with cloud and snow flags.
   - It covers one region (Austria).
   - It's the simplest fit for per-pixel classification. A Hugging Face copy exists (`monster-monash/TimeSen2Crop`).
   - Paper: Weikmann et al. 2021, doi:10.1109/jstars.2021.3073965.
2. **EuroCropsML.** Download: https://doi.org/10.5281/zenodo.15095445
   - It has 706,683 parcel-level samples across 176 crop classes, as median Sentinel-2 series for Latvia, Portugal and Estonia in 2021.
   - It was built for few-shot, transnational classification.
   - The CC-BY-SA licence means you should release derived data under the same terms. Ask your supervisor whether that also applies to shared model weights.
   - Papers: doi:10.1038/s41597-025-04952-7 (dataset), doi:10.1016/j.ophoto.2026.100117 (baselines).
3. **BreizhCrops.** Download: https://zenodo.org/records/14585341
   - It has field-level series for Brittany, in both top-of-atmosphere and bottom-of-atmosphere versions.
   - The authors provide code and pretrained baselines at github.com/dl4sits/breizhcrops. I did not open the GitHub page.
   - It's well cited (117 citations in the tool's data), which gives you comparison points.
   - Paper: doi:10.5194/isprs-archives-xliii-b2-2020-1545-2020.
4. **AgriSen-COG.** Download: https://zenodo.org/records/7892012
   - It covers five countries (Austria, Belgium, Spain, Denmark and the Netherlands), with labels from farmers' declarations (LPIS).
   - **Caveat:** this Zenodo record holds the labels and rasterised tiles. I did not confirm where the Sentinel-2 imagery is hosted, so check the paper before committing.
   - Paper: doi:10.3390/rs15122980.
5. **PASTIS.** Download: https://doi.org/10.5281/zenodo.5012941
   - It has parcel-level crop segmentation of Sentinel-2 time series in France, with a companion GitHub repository.
   - It suits semantic or panoptic segmentation more than per-pixel-set classification.
6. **S2-Agri (Pixel-Set).** Download: https://doi.org/10.5281/zenodo.5815488
   - It is described as "parcel-based crop type classification", in pixel-set format. A patch version is at doi:10.5281/zenodo.5815523.
   - I did not read its class list, so check that before using it.
7. **CropHarvest.** Download: https://doi.org/10.5281/zenodo.10251170
   - It's global, but mostly crop versus non-crop. Only a subset has multi-class crop labels, and it's not Sentinel-2 only. I did not inspect it closely.

On licences, CC-BY-4.0 allows publishing results and sharing models with attribution. I read these from registry metadata, not from the underlying label sources (national LPIS data), so cite both.

## Not recommended, and why
- **ZueriCrop (Hugging Face copy):** it's CC-BY-NC-4.0, and I didn't check the original's terms. The non-commercial clause can complicate sharing models.
- **Germany national crop-type maps (Zenodo 5153047):** these are output maps, not labelled Sentinel-2 time series, and no licence is stated.

## What I could not find
- I verified only a Hugging Face repackaging of Sen4AgriNet (CC-BY-SA-4.0), not the original download.
- I did not find a primary record for DENETHOR.
- The Zenodo API returned invalid responses at times, so coverage may be incomplete.
- I didn't confirm per-dataset class lists, so check that wheat, maize and rapeseed are all present in your region of choice.

## Next step
Start with TimeSen2Crop or BreizhCrops. Both are single-region and well documented, and you can have either within minutes. If you need several countries, use EuroCropsML or AgriSen-COG. Check dataset licences again before publishing, since terms can change.

Interactive page: `dataset-shortlist.html` (in `/private/tmp/e-xF8d4Y/home/cwd`)