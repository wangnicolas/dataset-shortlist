Several public datasets fit, and some need no application. I'm going from memory and haven't checked the live pages, so confirm the current terms and sizes before you build on them.

## Direct download, no application

| Dataset | Households | Resolution | History | Notes |
|---|---|---|---|---|
| **GoiEner** (Basque Country/Navarre, Spain; Zenodo) | ~25,000 | Hourly | Up to several years per customer | Probably the best match for your spec. It's recent and large, with metadata such as tariff and postcode. I believe the license is CC-BY. |
| **UKPN Low Carbon London** (London Datastore and Kaggle as "smart meters in London") | ~5,500 | 30 min | Nov 2011 – Feb 2014 | Coverage varies by household, and about 1,100 were on a dynamic time-of-use tariff. Joining weather is easy. |
| **Ausgrid Solar Home** (Ausgrid website) | 300 | 30 min | 3 years | Every home has rooftop PV, so consumption is confounded by solar. It may suit you or not. |
| **IDEAL** (Edinburgh DataShare) | ~255 UK homes | Down to 1 s (aggregate electricity) | ~1 year each | Rich, with sensor data and survey data, but you'd need to resample. |
| **Smart Grid Smart City** (data.gov.au) | ~78,000 | 30 min | 2010–2014 | Large and messy, with varying coverage. |

## Application required

- **Irish CER Smart Metering Project** (ISSDA): ~5,000 homes and SMEs at 30 min for about 500 days. It's free for research, but you sign a request form and agreement, and approval usually takes days. It's the classic forecasting benchmark, but it's slightly under 2 years and mixes in businesses, so filter to residential.
- **Pecan Street Dataport**: homes in Austin and elsewhere at 1-min resolution, with circuit-level data. Academic access is free but needs registration and approval. Commercial use is paid.

## Not a fit

- **UCI ElectricityLoadDiagrams** (370 clients) is mostly commercial.
- **REFIT** and **UK-DALE** have only ~5–20 homes.
- **BDG2** is buildings, not homes.

## Suggestion

Start with **GoiEner** for scale and recency, and add **London** for a second, independent test. Apply to ISSDA in parallel if you want the standard literature benchmark, since the wait is the only cost.

For day-ahead work you'll need to join weather (for example ERA5 or Open-Meteo) and holiday calendars yourself. None of these ships with them, except partly London.

I can fetch and inspect one of these (household counts, gaps, per-home history length) if you'd like me to verify it against your criteria.