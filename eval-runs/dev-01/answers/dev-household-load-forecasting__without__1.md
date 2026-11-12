Several fit your criteria, and some need no application. This is from memory and I haven't checked the current pages, so confirm sizes, dates and licenses before you commit.

## Direct download, no application

| Dataset | Households | Resolution | History | Notes |
|---|---|---|---|---|
| **GoiEner** (Basque Country, Zenodo) | ~25,000 | Hourly | Up to several years, varying per customer | Largest open one. It includes metadata such as tariff and postcode area, and the license is CC BY. Some customers have rooftop PV. |
| **UK Power Networks "Low Carbon London"** (London Datastore, mirrored on Kaggle) | ~5,500 | 30 min | Nov 2011 to Feb 2014 | Households have different start and end dates. About 1,100 were on a dynamic time-of-use tariff, so filter or flag them. |
| **Ausgrid Solar Home** (Sydney) | 300 | 30 min | 3 years | Every home has rooftop PV. Consumption and generation are separate columns, which is useful but unrepresentative of homes without PV. |
| **IDEAL** (Edinburgh DataShare) | 255 | Fine, down to seconds in the raw files | ~2 years | Smaller, with rich metadata and surveys. |

## Registration or application needed

- **Irish CER Smart Metering Trial** (via ISSDA, Irish Social Science Data Archive): ~5,000 homes and SMEs at 30 min, about 1.5 years from 2009 to 2010. You fill in a request form and sign a data-use agreement, and academic use is typically free. It's the classic benchmark, with survey data to separate residential from business meters.
- **Pecan Street Dataport**: hundreds of homes at 1-minute to 15-minute resolution, with circuit-level data. Academic access is free but needs an application, and commercial use is paid. Coverage and history length vary a lot by home.
- **UK Data Service** (for example, the Energy Demand Research Project): needs registration and has special-license tiers.

## Probably not what you need
- **UCI ElectricityLoadDiagrams (370 clients)**: widely used, but it's mostly businesses and a mix of customers, not clearly homes.
- **REFIT, UK-DALE, Smart\* and similar**: too few homes, typically 5–115.
- **NREL ResStock/EULP**: simulated, not measured.

## Recommendation
Start with **GoiEner** and **London**. Both are large and need no gatekeeping, and they cover different countries, climates and tariff regimes. Add **CER** if you want the standard benchmark, since requests are usually approved within days to weeks.

Some things will affect your benchmark design:
- **Weather and calendar covariates aren't included.** You'll need to join them yourself, for example from Open-Meteo or ERA5 for GoiEner and London.
- **Missing data and varying household histories** mean you should decide how to filter, for example by requiring at least a year of near-complete data.
- **Rooftop PV** in GoiEner and Ausgrid makes net load very different from gross demand, so treat those households as a separate group.
- **Dates are old** for CER and London, so some behavior, like EV charging and heat pumps, is absent.

I can fetch the current landing pages to verify license and access details, or write a loader and filtering script for one of these.