Yes, you can start today. The best-fitting datasets (GoiEner, London, Norwegian iFlex, Swiss HEAPO) are open downloads. The Irish CER trial needs a signed form, and the large UK SERL data needs months of accreditation.

I checked these on 2026-11-12 against Zenodo, the London Datastore, data.gov.au and the Pecan Street site. Three official pages (ISSDA, SERL, Ausgrid's own) blocked or failed my tool, so those access details come from web-search summaries and memory.

## What I assumed you need
- **R1 (must):** per-household smart-meter series, hundreds of households or more.
- **R2 (must):** at least a year of history per household.
- **R3 (must):** hourly or finer resolution.
- I assumed non-commercial research use, and that you'd rather start now than wait months.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [GoiEner](https://zenodo.org/records/7362094) (Spain) | Open download, minutes | CC BY (inconsistent, see below) | 25,559 raw series, hourly, 2014–2022 | Strong | Today |
| 2 | [Low Carbon London](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d) | Open download, minutes | Not stated in what I read | 5,567 households, half-hourly, 2011–14 | Strong | Today |
| 3 | [iFlex](https://zenodo.org/records/8248802) (Norway) | Open download, minutes | CC BY 4.0 | Hourly, 2020–21 | Partial | Today |
| 4 | [HEAPO](https://zenodo.org/records/15056919) (Switzerland) | Open download, minutes | CC BY 4.0 | 1,408 homes, 15-min, 2018–24 | Partial | Today |
| 5 | [Irish CER trial](https://www.ucd.ie/issda/data/commissionforenergyregulationcer/) | Signed request form, days | ISSDA terms | >5,000 homes and businesses, half-hourly | Strong | Web search and memory |
| 6 | [SERL Observatory](https://datacatalogue.ukdataservice.ac.uk/studies/study/8666) (UK) | Accredited-researcher application, months | UKDS secure agreement | ~13k homes, half-hourly, 2019–24 | Strong | Web search |
| 7 | [Smart-Grid Smart-City](https://data.gov.au/data/dataset/smart-grid-smart-city-customer-trial-data) (Australia) | Open download, minutes | CC BY 4.0 | Half-hourly, 2010–14 | Partial | Today |
| 8 | [Ausgrid Solar Home](https://data.gov.au/data/dataset/nsw-solar-home-electricty-data) | Open, but see caveat | Not checked | 300 homes, half-hourly, 3 years | Partial | Today |
| 9 | [Pecan Street Dataport](https://www.pecanstreet.org/dataport/) (US) | Free academic account, days | Non-commercial only | 75 homes in the free tier, 1-min | Partial | Today |

## Details
**GoiEner** (start here for scale)
- Hourly kWh for a Spanish energy cooperative's customers, 2014-11 to 2022-06.
- It comes as raw (2 GB) and imputed files (about 0.5–0.8 GB each), plus a metadata file. The imputed files only include series longer than a year, which covers your R2.
- It includes some small businesses, farms and industrial tariffs. Filter on the tariff column (2.X is households and small businesses).
- The Zenodo page says CC-BY-SA in the description but CC BY 4.0 in the rights field. Cite the WHY project.
- The 2020–21 pandemic period is in the data.

**Low Carbon London**
- This is the most-used UK benchmark: a representative sample, about 167 million rows and 10 GB unzipped.
- About 1,100 households were on dynamic time-of-use prices in 2013, with the price given a day ahead. Treat them as a confound for day-ahead forecasting, or exclude them.
- Many households have less than the full 2.3 years.
- A published day-ahead benchmark used 71 filtered households from it: [Benchmarking of Load Forecasting Methods Using Residential Smart Meter Data](https://doi.org/10.3390/app12199844) (2022).

**Irish CER trial**
- Download the Research Purposes request form from the ISSDA page, sign it and email it to issda@ucd.ie.
- It runs about 1.5 years (from memory) and mixes homes and businesses, so you'll need to filter to residential.
- Don't use unofficial mirrors. A ScienceDB copy turned up in the registry, and I didn't verify its permissions.

**SERL**
- You need Accredited Researcher status through the ONS accreditation service (every team member), the UKDS Secure Access agreement and approval from the SERL governance board.
- You can't download the data, and you must be in the UK when you access it.
- SERL's site quotes 4–6 weeks for review. The UKDS guidance says 3–4 months overall.
- There is also a [safeguarded SERL statistical dataset](https://doi.org/10.5255/ukda-sn-8963-1), but it is aggregated, so it doesn't meet your per-household requirement.

**Pecan Street**
- The free tier covers 75 homes (25 each in Austin, New York and California) for non-commercial academic use.
- Paid university tiers start at $10,000. That is too small for "hundreds of households" unless you pay.

## Known, not confirmed
- **Smart-Grid Smart-City:** the page confirms half-hourly data for the trial, but I haven't checked per-customer history. I recall about 13,000 customers, and many have partial coverage.
- **Ausgrid Solar Home:** all 300 homes have rooftop PV, so consumption and generation are separate channels. One user's quality screening kept only about 54 homes. Ausgrid's own page returned 404 to my tool. Check whether the data.gov.au link still serves the files.
- **iFlex:** it spans about two winters (early 2020 to spring 2021), so many households may have under a year. Check the lengths.

## Not recommended, and why
- **Electricity Load Diagrams (UCI, 370 clients):** Portuguese clients that are mostly commercial or industrial, not homes. It is a common forecasting benchmark, so it's easy to mistake for household data.
- **UK-DALE, REFIT, ECO:** these are household datasets, but they have only about 5 to 20 homes each (from memory).
- **Synthetic sets (ResStock-based, LPG-derived, OpenSynth):** simulated rather than measured.

## What I could not find
- I did not check per-household history length inside any dataset. For R2, count households with at least 365 days after you download.
- I found no other open household set at this scale with 1+ years of hourly data. The registry search also returned many small or country-specific sets that I did not review individually.

## Next step
Download GoiEner (filtered to household tariffs) and Low Carbon London (excluding the time-of-use group) now, and send the ISSDA form in parallel since it takes days. Only start the SERL accreditation if you need UK data from after 2014, because it takes months.

Interactive shortlist: `/private/tmp/e-N4S1wE/home/cwd/dataset-scout/dataset-shortlist.html`