Five datasets fit. All have real crop-type labels (not just cropland versus non-cropland) paired with Sentinel-2 time series, and all have licences that allow publishing results and sharing models. I confirmed each one exists. I could only confirm some of the licence and access details directly. The rest come from search summaries, and I've marked which.

## Recommended

**1. EuroCropsML (parcel-level time series, the easiest to start with)**
- It has 706,683 parcels in 176 crop classes, from Latvia, Portugal and Estonia in 2021. Each parcel is a time series of median Sentinel-2 L1C reflectance, with labels from farmer declarations (EuroCrops v9).
- Get it from Zenodo (concept DOI 10.5281/zenodo.10629609; versions such as [10683255](https://zenodo.org/records/10683255)), or with `pip install eurocropsml` followed by `eurocropsml-cli datasets eurocrops download`.
- Licence: the paper is CC BY 4.0 and the code is MIT. I did not read the licence on the Zenodo record itself, so check it before you publish. EuroCrops is built from national sources with differing terms.
- It is built for few-shot and transfer experiments (pretrain on Latvia and Portugal, fine-tune on Estonia). It also works as a plain classification benchmark.
- A "2.0" version with more countries is mentioned in a recent paper. I did not verify it.

**2. PASTIS / PASTIS-R (parcel segmentation of France)**
- It has 2,433 patches of 128×128 pixels at 10 m, with 18 crop types plus background and void. The labels are per parcel, and the patches are Sentinel-2 time series. PASTIS-R adds Sentinel-1.
- I confirmed that the [PASTIS Zenodo record](https://zenodo.org/records/5012942) exists. It is a single 28.8 GB file, licensed CC BY 4.0.
- PASTIS-R is at zenodo.org/record/5735646. I only saw that link on a secondary summary page, so open it to confirm. There is also a [Hugging Face TACO copy](https://huggingface.co/datasets/isp-uv-es/pastis-r-taco) under CC-BY-4.0.
- The Zenodo page doesn't describe the labels or mention Sentinel-2 itself. That comes from the paper and the secondary sources.

**3. BreizhCrops (Brittany, France, 2017)**
- It has about 610k–768k field-level time series, depending on the processing level, with top- and bottom-of-atmosphere versions. Labels come from the French RPG. The class count is reported as nine in one source. I couldn't confirm that.
- Install with `pip install breizhcrops`, then `breizhcrops.BreizhCrops("frh04")`. The data is also on [Zenodo](https://zenodo.org/records/14585341).
- Licence: the Zenodo record and arXiv listing say CC BY 4.0. The code repository ([dl4sits/BreizhCrops](https://github.com/dl4sits/BreizhCrops)) is GPL-3.0, which applies to the code, not the data. The paper only says the RPG labels are under an "open license".
- It is small and simple, so it works well for quick baselines.

**4. AgriSen-COG (Austria, Belgium, Catalonia, Denmark and the Netherlands, 2019–2020)**
- The labels are parcel-level from the LPIS (the EU's parcel registry). The data is Sentinel-2 in cloud-optimised GeoTIFFs, built for segmentation and classification.
- The [Zenodo record](https://zenodo.org/records/7892012) is CC BY 4.0. Its files (parcel info, original LPIS, ground-truth patches) were listed. I did not check whether the Sentinel-2 imagery is on Zenodo or comes from the [GitHub repo](https://github.com/tselea/agrisen-cog), so read the repo's instructions.
- The paper says the LPIS data is under the Open Data Commons Attribution Licence, which allows publishing.

**5. Sen4AgriNet (Catalonia and France, 2016–2020)**
- It has about 225,000 multi-year patches (about 10 TB), with a parcel-aggregated version and a patch version. Labels are from the LPIS.
- The Hugging Face copy is [isp-uv-es/sen4agrinet-taco](https://huggingface.co/datasets/isp-uv-es/sen4agrinet-taco). The experiment code is in [Orion-AI-Lab/S4A-Models](https://github.com/Orion-AI-Lab/S4A-Models) (MIT).
- The licence is inconsistent. The journal version says CC BY 4.0, while arXiv and Hugging Face say CC BY-SA 4.0. Under share-alike, anything you share that is derived from the data may have to carry the same licence. That could matter for sharing models, so ask your supervisor or check the official release.
- At 10 TB it is probably too big for a master's project unless you use a subset.

## Not recommended for your case
- **CropHarvest:** it is global but mostly binary crop versus non-crop labels, so it doesn't meet your requirement.
- **EuroCrops:** it is labels only, with no Sentinel-2 data. Use EuroCropsML instead.
- **ZueriCrop and TimeMatch:** I did not verify their licences or access, so I'm not recommending them.

## Suggested path
Start with **BreizhCrops** or **EuroCropsML** for a quick time-series classification baseline. Use **PASTIS-R** if you want image-level or segmentation models. Add **AgriSen-COG** if you need more countries.

Some pages were blocked or incomplete (Nature, PMC, ResearchGate, and the arXiv PDF text). So the EuroCropsML and Sen4AgriNet details rest on search summaries. Before you publish, read each Zenodo or Hugging Face licence field, and cite the original papers.

Sources:
- [EuroCropsML (Nature Sci. Data)](https://www.nature.com/articles/s41597-025-04952-7)
- [EuroCropsML (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12009327/)
- [EuroCropsML on GitHub](https://github.com/dida-do/eurocropsml)
- [eurocropsml on PyPI](https://pypi.org/project/eurocropsml/)
- [PASTIS on Zenodo](https://zenodo.org/records/5012942)
- [PASTIS-R summary](https://www.emergentmind.com/topics/pastis-r-benchmark)
- [BreizhCrops on arXiv](https://arxiv.org/abs/1905.11893)
- [BreizhCrops on Zenodo](https://zenodo.org/records/14585341)
- [AgriSen-COG paper](https://doi.org/10.3390/rs15122980)
- [Sen4AgriNet paper (arXiv)](https://arxiv.org/html/2204.00951v2)
- [EuroCrops (Nature Sci. Data)](https://www.nature.com/articles/s41597-023-02517-0)