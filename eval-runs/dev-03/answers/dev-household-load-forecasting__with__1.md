Several good household-level datasets exist, and four of them you can download today with no application. I checked these on 2026-11-12. Some registry lookups timed out, so I mark which facts are confirmed and which are from memory.

## What I assumed you need
- Per-household meters, not feeder totals (must-have).
- Hourly or finer resolution (must-have).
- At least a year of history per home (must-have).
- Hundreds of homes or more (must-have).
- Research use. I did not assume commercial use.

## Shortlist
| # | Dataset | Access | Licence | Households | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | GoiEner smart meters (Spain) | Open download, minutes | CC-BY-4.0 | ~25k (v7.1 lists 28,900 profiles) | Strong | Today |
| 2 | London Smart Meters, Low Carbon London (UK) | Open download, minutes | CC-BY (from memory) | 5,567 | Strong | Page confirmed today; licence from memory |
| 3 | CER Irish Smart Metering trial | Signed request form to ISSDA, days | ISSDA data-use terms | ~5,000 homes and businesses | Strong | Page and process confirmed today |
| 4 | Smart-Grid Smart-City trial (Australia) | Open download, minutes | CC-BY-4.0 | Thousands (from memory) | Strong | Today |
| 5 | Pecan Street Dataport (US) | University account, ~3 business days | University licence | Hundreds or more (from memory) | Strong | Today |
| 6 | HEAPO (Switzerland) | Open download | CC-BY-4.0 | 1,408 | Partial | Today |
| 7 | iFlex (Norway) | Open download | CC-BY-4.0 | Several hundred (from memory) | Partial | Today |
| 8 | Ausgrid Solar Homes (Australia) | Open download | CC-BY-4.0 | 300 | Partial | Record registered today; contents from memory |

## Details
- **GoiEner:** Hourly kWh per customer, with processed files kept to series longer than a year. Download from Zenodo with no account, and prefer [v7.1](https://doi.org/10.5281/zenodo.22313409) over the [2022 release](https://doi.org/10.5281/zenodo.7362094). Customers are mostly in northern Spain and some have PV or are businesses, so check the metadata file.
- **London:** Half-hourly data, Nov 2011 to Feb 2014, from the [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d) (about 10 GB). Cleaned copies are on [Zenodo](https://zenodo.org/records/4656091). Start dates are staggered, so most homes have 1–2 years.
- **CER Ireland:** The [ISSDA record](https://doi.org/10.7929/ISSDA/BX59EU) has 30-minute data over about 18 months (from memory). To get it, sign the research request form and email it to issda@ucd.ie. Each student needs their own form, and the data includes businesses.
- **Smart-Grid Smart-City:** [data.gov.au](https://data.gov.au/data/dataset/smart-grid-smart-city-customer-trial-data) has half-hourly readings linked to demographics and tariffs, licensed CC BY 4.0. The trial ran 2010–14.
- **Pecan Street:** [Dataport](https://dataport.pecanstreet.org) requires a university email and proof of affiliation. The page says approval takes about 3 business days. Commercial use needs a paid licence. I could not see the free tier's coverage.
- **HEAPO and iFlex:** [HEAPO](https://zenodo.org/records/15056919) covers heat-pump homes only, so loads are atypical. [iFlex](https://zenodo.org/records/8248802) is hourly but comes from a pricing experiment lasting about a year, with treatment effects.
- **Ausgrid:** [This figshare record](https://doi.org/10.6084/m9.figshare.32975426.v1) is net demand for homes with rooftop PV, so gross load is hidden.

## Known, not confirmed
- Exact time spans and household counts for GoiEner, SGSC and Pecan Street are from memory.
- Ausgrid's original 300-home, 3-year release is also from memory.

## Not recommended
- **UCI ElectricityLoadDiagrams:** 370 clients, mostly commercial (from memory).
- **REFIT and UK-DALE:** Only 20 and 5 homes (from memory).

## What I could not find
I did not check a few other possible sources: Low Carbon London extras, Dutch or Nordic utility releases, and academic forecasting benchmarks. I also did not find papers that used these datasets, because I ran out of budget.

## Next step
Start with GoiEner and London today. They need no approval and together give you tens of thousands of homes. In parallel, send the CER form, since it is the classic benchmark for comparing against published results.

Companion page: `/private/tmp/e-JK1LHZ/home/cwd/dataset-shortlist.html`