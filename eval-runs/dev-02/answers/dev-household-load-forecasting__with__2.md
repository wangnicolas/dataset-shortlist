## What I assumed you need

- **R1 (must):** consumption per household, not feeder or grid totals.
- **R2 (must):** at least a year of history per household.
- **R3 (must):** hourly or finer resolution.
- **R4 (nice to have):** downloadable now, without an application.
- **Assumed:** non-commercial research use, and that a few thousand households counts as "hundreds or more".

## Shortlist

Short answer: you can download all of these now. None needs an application. Checked 2026-11-12.

| # | Dataset | Access | Licence | Households | Resolution / span | Checked |
|---|---|---|---|---|---|---|
| 1 | GoiEner (Spain) | Open download, Zenodo | CC BY 4.0 | 25,559 supply points | Hourly, about 3 years on average (2014–2022) | Registry record and page, today |
| 2 | Low Carbon London (UK Power Networks) | Open download, London Datastore | CC BY | 5,567 | 30 min, Nov 2011–Feb 2014 | Web search summary; the page itself is not machine-confirmed |
| 3 | ECD-UY (Uruguay) | Open download, figshare | CC0 | 110,953 | 15 min, about 1.8 years | Registry record; the page blocked scripts, so open it in a browser |
| 4 | Swiss residential load profiles | Open download, Zenodo | CC BY 4.0 | 2,447 | 15 min, 2023–2024 | Registry record and page, today |
| 5 | HEAPO (Zurich) | Open download, Zenodo | CC BY 4.0 | 1,408 | 15 min, Nov 2018–Mar 2024 | Registry record and page, today |
| 6 | iFlex (Norway) | Open download, Zenodo | CC BY 4.0 | About 3,700–4,500 (sources disagree) | Hourly, early 2020–spring 2021 | Registry record and page, today |
| 7 | Smart-Grid Smart-City (Australia) | Open download, data.gov.au | CC BY 3.0 AU | Unclear (about 8,000 to 78,000) | 30 min, 2010–2014 | Web search summary only |

## Details

- **GoiEner:** the [Zenodo record](https://zenodo.org/records/7362094) has raw data (15.1 GB) and imputed files for series longer than a year. It is a mix of customers. The `contracted_tariff` field lets you keep households, but the "2.X" tariff also includes small businesses. Zenodo also lists newer versions than the v1 I read. The dataset paper is [Sci. Data 2023](https://www.nature.com/articles/s41597-023-02846-0).
- **London:** the [London Datastore page](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d) offers a zip of about 765 MB. Households join and leave at different times, so filter for those with a full year. This is the most-used household benchmark, and one day-ahead study on it is [Benchmarking of Load Forecasting Methods Using Residential Smart Meter Data](https://doi.org/10.3390/app12199844). Use this official copy rather than the Kaggle or GitHub mirrors.
- **ECD-UY:** by far the largest. The [figshare record](https://doi.org/10.6084/m9.figshare.16965400) is CC0, and its paper is [Sci. Data 2022](https://doi.org/10.1038/s41597-022-01122-x). It is a southern-hemisphere climate with little weather metadata.
- **Swiss:** the [Zenodo record](https://zenodo.org/records/21398769) was published in July 2026. It covers apartments and houses, including homes with heat pumps, EVs and PV. It has two full years but few published baselines yet.
- **HEAPO:** the [Zenodo record](https://zenodo.org/records/15056919) has the longest history, but every home has a heat pump, so demand is strongly weather-driven and unrepresentative.
- **iFlex:** the [Zenodo record](https://zenodo.org/records/8248802) includes surveys. It comes from a price-response experiment during COVID, which distorts day-ahead patterns, and it spans only about a year. Check Table 1 of its paper for exact counts.
- **Smart-Grid Smart-City:** the [data.gov.au page](https://data.gov.au/data/dataset/smart-grid-smart-city-customer-trial-data) has half-hourly readings per household. The trial's tariffs and in-home displays may affect behaviour.

For your benchmark, I'd start with GoiEner, London and ECD-UY. They cover three different countries and climates.

## Known, not confirmed

- **Irish CER Smart Metering Trial (ISSDA, UCD):** about 5,000 homes and businesses at 30 min over 2009–2010, about 1.5 years. It is widely used in the literature.
  - **Access:** the search results (not the page) say you complete and sign a request form and email it to ISSDA. That is an application rather than a download. Time to access is unknown, probably days to weeks.
  - **What I tried:** the ISSDA site refused automated requests (HTTP 403), so I couldn't read the terms.
  - **What to check:** the [ISSDA dataset page](https://www.ucd.ie/issda/data/commissionforenergyregulationcer/) for the form and terms.

## Not recommended, and why

- **Pecan Street Dataport:** the free academic tier covers only 75 homes. More needs a paid licence (from web search).
- **Ausgrid Solar Home data:** 300 solar homes at 30 min over 3 years. It is small and PV-skewed, and a repo note says it may have been removed from Ausgrid's site. Public copies exist on [data.gov.au](https://www.data.gov.au/data/en/dataset/nsw-solar-home-electricty-data).
- **IDEAL Household Energy Dataset:** I recall roughly 255 homes, from memory and not confirmed. That is small for your threshold.
- **Kaggle, Hugging Face and Zenodo re-uploads of the London data:** these are third-party copies. Use the official source.

## What I could not find

- I did not check the documentation of every dataset for the share of households with a complete year. Do this yourself for London, iFlex and SGSC.
- Registry searches on DataCite and Hugging Face sometimes returned malformed responses, so the list may be incomplete. I searched Zenodo, OpenAIRE, DataCite, Hugging Face and PhysioNet, plus the web.
- The London and SGSC access and licence details come from a web search summary, not the registry record.

## Next step

Download GoiEner and London first and build your day-ahead baseline on them. Then validate on ECD-UY. If you want an Irish comparison, send the ISSDA request now, since it's the only one with a wait.

The interactive page is at `/private/tmp/e-qVHPie/home/cwd/dataset-shortlist.html`. I didn't commit anything.