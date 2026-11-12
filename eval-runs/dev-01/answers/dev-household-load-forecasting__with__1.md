## What I assumed you need

- **R1 (must):** per-household meter data, hundreds of homes or more.
- **R2 (must):** at least a year of history per household.
- **R3 (must):** hourly or finer.
- **R4:** data you can get now, or via an application, with the licence stated.

I assumed no commercial-use constraint. Checked 2026-11-11. Hugging Face and part of the Zenodo search failed, so coverage is incomplete.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit |
|---|---|---|---|---|---|
| 1 | London Smart Meters (UK Power Networks) | Open download, no sign-in, minutes | CC BY 4.0 | 5,567 homes, half-hourly, 2011–14 | Strong |
| 2 | GoiEner Smart Meter Dataset v7.1 (Spain) | Open download on Zenodo, minutes | CC BY 4.0 | 28,900 hourly profiles, ~9 GB | Strong, with a caveat |
| 3 | CEEW Smart Meter Data (India) | Open per registry, minutes | CC0 | ~1,000 homes, 3-minute, 2019–21 | Partial |
| 4 | Ausgrid Solar Home (net demand) | Open per registry | CC BY 4.0 | Not confirmed | Partial |
| 5 | CER Irish trial (ISSDA) | **Not confirmed** | **Not confirmed** | Not confirmed | Unknown |
| 6 | Smart-Grid Smart-City (Australia) | **Not confirmed** | **Not confirmed** | Not confirmed | Unknown |
| 7 | Pecan Street Dataport | **Not confirmed** | **Not confirmed** | Not confirmed | Unknown |

## Details

**1. London Smart Meters.** The page is on the [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d).
- The data is half-hourly for 5,567 households, Nov 2011 to Feb 2014.
- The download is a ~760 MB ZIP holding one ~10 GB CSV of 167M rows. A split version of 168 CSVs is also offered.
- Households joined the trial at different times, so many have under 12 months. Filter by history length. I did not check how many have a full year.
- You need to add weather and holidays yourself.
- Used for day-ahead forecasting in [Benchmarking of Load Forecasting Methods Using Residential Smart Meter Data](https://doi.org/10.3390/app12199844) (2022), on 71 selected households.

**2. GoiEner v7.1.** The record is on [Zenodo](https://doi.org/10.5281/zenodo.22313409).
- It holds hourly profiles from a Spanish energy cooperative, with consumption, generation and import/export variables.
- The page doesn't state the years covered or how many customers have a full year. The annual matrix has a `full_year` flag you can filter on.
- The metadata carries a business-activity code (CNAE), so some customers may be businesses, not homes. Check this before benchmarking.

**3. CEEW India.** The record is [here](https://doi.org/10.71646/gexzrr).
- It has 3-minute readings from ~1,000 households in Mathura and Bareilly.
- The registry says open and CC0, but I couldn't open the landing page or the Dataverse copy, so confirm in a browser.
- The usage patterns are unlike European homes. Per-household history length is unchecked.

**4. Ausgrid Solar Home.** The record is [here](https://doi.org/10.6084/m9.figshare.32975426.v1).
- The registry says open and CC BY 4.0, but figshare blocked my page read, so I haven't seen the contents.
- From memory it is ~300 homes at half-hourly resolution, which I did not verify.
- It is net demand with rooftop solar, so the target mixes load and generation.

**5–7. CER, SGSC and Pecan Street.** All three exist as records, but I could not read their access pages.
- **CER:** the DOI is registered ([record](https://doi.org/10.7929/issda/bx59eu)). The ISSDA site returned errors. I recall an application form and agreement, and about 5,000 homes and businesses at half-hourly resolution over ~18 months. That is unconfirmed, so write to issda@ucd.ie.
- **SGSC:** the data.gov.au page exists, but I got only its metadata. Access and licence are unread.
- **Pecan Street:** the registry gives no access or licence. I recall academic access on application and paid commercial access, but I didn't verify that.

## Not recommended, and why

- **SERL (UK):** the open pages are aggregated statistics only. The household-level data appears to be safeguarded access via the UK Data Service. Its page was blocked, so this is unverified.
- **Synthetic profiles, appliance-level sets and feeder or commercial datasets** turned up in the search. They are synthetic, too small, or not household-level.

## What I could not find

- Confirmed access terms for CER, SGSC and Pecan Street.
- Confirmed counts of households with 12+ months of data in any dataset.

## Next step

Start with London and GoiEner, which are open today and large. Then count the households with 12+ months of history and drop non-household customers from GoiEner. Confirm CER's access terms with ISSDA if you want its trial data.

Interactive page: `/private/tmp/e-SXQ4TA/home/cwd/dataset-shortlist.html`