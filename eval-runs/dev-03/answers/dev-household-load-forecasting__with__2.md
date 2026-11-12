Several good datasets are free to download today, and one big one needs a short application. I found nothing at the scale and quality you want that is locked behind a long approval process.

I checked on 2026-11-12. Registry records and Zenodo pages are marked "confirmed". Access and licence details I recalled but couldn't read are marked "from memory". DataCite search and parts of the Zenodo and Hugging Face searches kept failing, so the list may be incomplete.

## What I assumed you need
- **R1:** consumption per household, not feeder or grid totals.
- **R2:** hundreds of households or more.
- **R3:** at least a year of history per household.
- **R4:** hourly or finer.
- Public data you can start on now. I'd count a short application as acceptable.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | GoiEner Smart Meter Dataset v7.1 (Spain) | Direct download from Zenodo | CC BY 4.0 | 28,900 customer series, hourly, about 9 GB | Strong | Today |
| 2 | Residential load profiles, Switzerland | Direct download from Zenodo | CC BY 4.0 | 2,447 installations, 15-minute, 2023–2024 | Strong | Today |
| 3 | London Households (UKPN Low Carbon London) | Download from London Datastore | Open Government Licence | 5,567 households, half-hourly, Nov 2011–Feb 2014 | Strong | Page exists, access and licence from memory |
| 4 | CER Irish Smart Metering Trial | Application plus Data Use Agreement through ISSDA, weeks | Custom data use terms | About 5,000 homes and small businesses, half-hourly, about 1.5 years | Strong | Application form and agreement confirmed today. Size and span from memory |
| 5 | CEEW India smart meter data | Direct download from Dataverse | CC0 | About 1,000 households, 3-minute, 2019–2021 | Partial | Today |
| 6 | IDEAL (Edinburgh, UK) | Download from DataShare | CC BY 4.0 (from memory) | 255 homes, about 23 months, plus appliance data | Partial | Page exists, details from memory |
| 7 | Smart-Grid Smart-City trial (Australia) | Download from data.gov.au | CC BY (from memory) | Tens of thousands of customers, half-hourly, 2010–2014 | Partial | Page exists, details from memory |
| 8 | Chinese households smart meter dataset | Direct download from figshare | CC BY 4.0 | 2,162 households, 24 or 96 readings per day | Partial | Today |

## Details
- **GoiEner** (https://zenodo.org/records/22313409)
  - **What it is:** a Basque and Navarre energy cooperative's customers, with an annual hourly matrix and reduced public metadata.
  - **Missing:** I couldn't confirm how long each customer's history is. Some customers have PV, and some may be businesses.
  - **Version:** use v7.1, not the 2022 record.
- **Switzerland** (https://doi.org/10.5281/zenodo.21398769)
  - **What it is:** apartments, single-family houses, heat pumps and common building areas, so not all are whole households. It is recent and includes PV and heat-pump effects, which makes forecasting harder.
- **London**
  - **Missing:** many households joined partway through, so only some have a full year.
  - **Copies:** Kaggle has a copy, but use the London Datastore.
  - **Access:** the Datastore page timed out when I read it, so access and licence are from memory.
  - **Related:** a 2013 time-of-use pricing trial (1,100 households) is held separately at the UK Data Service. Its access tier is unknown, so check it before relying on it.
- **CER Ireland**
  - **Access:** the page shows "Request Access" and a custom Data Use Agreement. Approval time is from memory (days to a couple of weeks).
  - **Missing:** the trial applied tariff and stimulus changes to some homes, which affects the baseline.
- **CEEW India**
  - **Missing:** there are many supply outages, so the series have gaps and zeros. It also has a different demand pattern from European homes.
  - **Access:** the landing page was blocked for the checker. The registry says open under CC0.
- **IDEAL, Smart-Grid Smart-City and the Chinese dataset:** these are smaller or less certain. The Chinese set reports net power, so PV export masks demand for its 620 prosumers. I couldn't confirm its time span.

## Known, not confirmed
- **Ausgrid Solar Home data** (from memory: 300 homes, 30-minute, 3 years, open). The address I tried returned 404, so find the current link on Ausgrid's site.
- **SERL Observatory** (UK, 13,000+ households, half-hourly). A paper I found describes it, but I didn't check its access. From memory it is safeguarded data from the UK Data Service, so expect registration or an application.
- **Pecan Street Dataport** (US). The site wouldn't load. From memory, it is free for university researchers after a signed agreement, and the free tier has far fewer homes.
- **Hugging Face "OpenSynth/TUDelft-Electricity-Consumption"** bundles several household sets, including London and Dutch Liander data. It is handy for quick tests, but I didn't confirm its contents or span.

## Not recommended, and why
- **UCI ElectricityLoadDiagrams** and its Hugging Face copies. From memory it has 370 Portuguese clients, many commercial. I couldn't load the page to confirm.
- **UCI household power consumption.** From memory it covers one household.
- **"AI-Ready" Zenodo versions of the London data.** The demand-forecasting one is an hourly total across households, so it fails R1. The anomaly-detection one is a feature-engineered copy, so use the original.

## What I could not find
Nothing public that is both open and large with long multi-year hourly history across many homes. GoiEner is the closest. I didn't confirm the per-customer history length there, so check it first.

## Next step
Download GoiEner and the Swiss set today. Apply to ISSDA for the Irish data in parallel, because it is the best-known forecasting benchmark. London is a good fallback for a comparison dataset.

Interactive page: `/private/tmp/e-2Ua2Ic/home/cwd/dataset-shortlist.html`