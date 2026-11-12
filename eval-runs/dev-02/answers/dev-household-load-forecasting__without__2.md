Several public datasets meet your criteria. Some can be downloaded directly and some need an application. This is from memory and I haven't checked the links, so confirm current licences and download pages before you build on them.

## Direct download, no application

| Dataset | Households | Resolution | History | Notes |
|---|---|---|---|---|
| **GoiEner** (Spain, Basque Country and Navarre, on Zenodo) | ~25,000 | Hourly | Several years (roughly 2014–2022) | Largest and most recent open set. It has per-customer metadata such as tariff and location, which lets you pull weather. |
| **London Smart Meters** (UK Power Networks, London Datastore, mirrored on Kaggle) | ~5,500 | 30 min | Nov 2011 – Feb 2014 | Includes a weather file and ACORN demographic groups. Coverage varies by household, so filter for those with at least a year. |
| **Ausgrid Solar Home** (Australia) | 300 | 30 min | 3 years | All homes have rooftop PV, so it suits net-load forecasting more than plain demand. |
| **IDEAL** (UK, Edinburgh DataShare) | 255 | 1 s to 1 min | Up to ~2 years | Many homes have shorter series, and you'd have to aggregate to hourly. |
| **Smart-Grid Smart-City** (Australia, data.gov.au) | Thousands | 30 min | ~2010–2014 | The format is messier, so it needs more cleaning. |

## Free, but you have to apply

| Dataset | Households | Resolution | History | Access |
|---|---|---|---|---|
| **CER Smart Metering Project** (Ireland, via ISSDA) | ~4,200 residential, plus SMEs | 30 min | ~1.5 years (2009–2010) | Sign a request form and agree to the terms. Approval usually takes days. It has no location data, so you can't join weather. |
| **SERL** (UK Smart Energy Research Lab, via UK Data Service) | 13,000+ | 30 min | Multi-year, recent | Requires registration and project approval. Some tiers need a secure-access setup. |
| **Pecan Street Dataport** (Texas) | ~1,000+ | 1 to 15 min, with circuit-level data | Multi-year | Free for academics through a university agreement. Commercial use is paid. |

## Things to watch

- **Avoid the UCI "ElectricityLoadDiagrams 2011–2014" set.** It has 370 clients, but they're mostly commercial and industrial, and it's often mislabelled as households.
- **NREL ResStock/ComStock and similar sets are simulated, not metered.** They're fine for stress tests but not for a real-world benchmark.
- **REFIT, UK-DALE and Smart\*** have only a handful of homes, so they're too small for your criteria.
- **Check the year-long history per household.** Many datasets have staggered start and end dates, so you'll need to filter.
- **Day-ahead forecasting needs exogenous data.** You'll want weather and a holiday calendar. GoiEner and London support this best, and CER doesn't.

For a start without paperwork, I'd use GoiEner as the main benchmark and London as a second dataset for cross-checking. If you can wait a few days, adding CER or SERL would give you a more widely cited baseline for comparison.

I can download and profile any of these, for example counting households with at least a year of data and checking for gaps, if you want.