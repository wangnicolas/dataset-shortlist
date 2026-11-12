## What I assumed you need

- **R1 (must):** consumption per household from smart meters, not feeder or grid totals.
- **R2 (must):** hundreds of households or more.
- **R3 (must):** at least a year of history per household.
- **R4 (must):** hourly or finer resolution.
- **R5 (nice to have):** a direct download, with no application.

I assumed non-commercial research use and no particular country. Day-ahead forecasting also needs weather and calendar features, which none of these sets ship with.

## Shortlist

Yes, you can start today. Six datasets are open downloads with no application. Two more well-known ones need an application or give you too little data (see below). I checked the first six against their registry records on 2026-11-11/12.

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [LADPU Smart Meter Data](https://zenodo.org/records/4312086) (Los Alamos, USA) | Open download, minutes | CC0 | 1,757 homes, 15-min, about 6 years | Strong | Today |
| 2 | [Residential load profiles, Switzerland](https://zenodo.org/records/21398769) | Open download, minutes | CC-BY-4.0 | 2,447 installations, 15-min, 2023–24 | Strong, with a caveat | Today |
| 3 | [HEAPO](https://zenodo.org/records/15056919) (Zurich) | Open download, minutes | CC-BY-4.0 | 1,408 homes, 15-min, 2018–2024 | Strong for heat-pump homes only | Today (span from paper via web search) |
| 4 | [GoiEner v7.1](https://zenodo.org/records/22313409) (Spain) | Open download, minutes | CC-BY-4.0 | 28,900 hourly series, about 9 GB | Partial | Today |
| 5 | [London Smart Meters](https://zenodo.org/records/4656072) (Low Carbon London) | Open download, minutes | CC-BY-4.0 | 5,560 homes, half-hourly, Nov 2011 – Feb 2014 | Partial | Today |
| 6 | [iFlex](https://zenodo.org/records/8248802) (Norway) | Open download, minutes | CC-BY-4.0 | Several thousand homes, hourly, 2020–21 | Partial | Today |

## Details

**1. LADPU.** The Zenodo description says Landis+Gyr smart meters on 1,757 households, with most customers covered from 30 Jul 2013 to 30 Dec 2019. It has missing and duplicated readings. It has no weather or household metadata, so you would join your own weather data.

**2. Switzerland 2023–24.** It has active and reactive energy, including injection from PV. The installations include common building areas and heat-pump meters, so filter by installation type to get homes.

**3. HEAPO.** The households all have heat pumps, so demand is not typical of the general population. It comes with weather from 8 stations and 410 on-site inspection protocols. Not every home covers the full period.

**4. GoiEner.** It is the largest open set, but the customers are not all households. The paper says shops, offices and industry are included. One third-party analysis cut the original 25,559 points to 20,509 by dropping non-residential and self-consumption points. v7.1 differs from the original release (DOI 10.5281/zenodo.7362094), so check which version the papers you compare against used. The original paper is in [Scientific Data](https://www.nature.com/articles/s41597-023-02846-0).

**5. London.** About 1,100 homes were on dynamic time-of-use prices during 2013, and the price schedule is published. Treat those homes separately in a benchmark. Homes joined at different times, so keep only those with 12 or more months. The Zenodo copy is a reformatted subset. The original is on the [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d) (about 10 GB CSV, UK Power Networks).

**6. iFlex.** It has hourly data from a Norwegian pricing experiment, plus surveys and temperature. Household counts differ by phase in the sources I found: 772, 3,746 and 4,483. Households were on price experiments, so the data is shaped by treatment. I did not check how long each household's history is.

## Known, not confirmed

- **Irish CER Smart Metering Trial** (ISSDA study 0012-00, [DOI 10.7929/ISSDA/BX59EU](https://doi.org/10.7929/ISSDA/BX59EU)). A web search says 4,225 households, half-hourly, 536 days. You need to request access: download the request form from the dataset's Terms tab and email it to issda@ucd.ie. You sign as end user and someone signs for your organisation. Use is non-commercial research or teaching only. This comes from search snippets, because the ISSDA page returned HTTP 403 to me. The turnaround is unknown, so assume weeks. Check the [ISSDA data page](https://www.ucd.ie/issda/accessdata/issdadatasets/).
- **Ausgrid Solar Home Electricity Data** (Australia). It has 300 solar homes, 30-minute, July 2010 – June 2013, so it is small but covers three years. A search shows it on [data.gov.au](https://data.gov.au/data/dataset/nsw-solar-home-electricty-data). A May 2026 blog comment says Ausgrid's own site no longer hosts it. I did not test the download and could not open the data.gov.au page (HTTP 403). The licence is unknown.
- **CKW Smart Meter Data** (Switzerland). The Zenodo copy is only a 42 MB sample. The full set is on [ckw.ch/opendata](https://www.ckw.ch/opendata), which I could not read (HTTP 403), so size, terms and span are unknown.

## Not recommended, and why

- **Pecan Street Dataport.** The free university tier covers only about 75 homes (a July 2025 Pecan Street post found by web search), which fails R2. Paid licences start at $10,000.
- **UCI ElectricityLoadDiagrams and its Hugging Face copies.** It has 370 clients, mixed with businesses, so it isn't household-level at the scale you want.

## What I could not find

- I did not search Hugging Face copies of the large public sets for provenance. I also found no verified Hugging Face source that beats the Zenodo records above.
- I did not look up papers that use each dataset for day-ahead forecasting. The one literature query returned nothing relevant, so I can't give you baselines or citations yet.
- The registry search is noisy, and the DataCite query failed once. Other utility portals may be missing.

## Next step

I'd start with LADPU, the Swiss 2023–24 set and London. They give you three countries, different eras and open licences. London's dynamic-tariff homes and GoiEner's business customers need filtering. If you want a quick comparison with published work, send the Irish CER request form now, since it is the only slow step.

Interactive page: `/private/tmp/e-aIA742/home/cwd/dataset-shortlist.html`