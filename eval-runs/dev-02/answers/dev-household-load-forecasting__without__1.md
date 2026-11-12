I'm answering from memory and didn't check the current links or licenses, so confirm those on each landing page. Here are the datasets that fit your criteria (individual households, hundreds or more, at least a year, hourly or finer):

| Dataset | Households | Resolution | Span | Access |
|---|---|---|---|---|
| **GoiEner** (Basque Country, Spain) | about 25,000 | hourly | several years | **Direct download** from Zenodo (CC-BY). It's the largest open option and has metadata such as tariff and postcode. |
| **London Smart Meters** (UK Power Networks, Low Carbon London) | about 5,500 | 30 min | Nov 2011 to Feb 2014 | **Direct download** from the London Datastore and Kaggle. About 1,100 households were on a dynamic time-of-use tariff, which you'd need to handle. Many households have gaps or start late. |
| **Ausgrid Solar Home** (Sydney) | 300 | 30 min | 3 years | **Direct download** from Ausgrid's site. All homes have rooftop PV, so net and gross load differ, which matters for forecasting. |
| **Smart Grid Smart City** (Australia) | tens of thousands | 30 min | about 2012 to 2014 | **Direct download** from data.gov.au. The data is messy, and coverage varies by customer. |
| **CER Irish Smart Metering Trial** | about 4,000 homes (plus about 1,000 SMEs) | 30 min | about 1.5 years (2009 to 2010) | **Application required** through ISSDA. It's free for research, but you sign a data-use agreement, and approval can take days. |
| **Pecan Street Dataport** (US) | hundreds to thousands | 1 min to 15 min, including circuit-level | varies by home | **Application required**. Academic access is free, and commercial use is paid. A small sample is open. |

**Practical notes**
- **Fastest start:** GoiEner is the best match for your criteria and needs no application. London is the most widely used benchmark, so it gives you the most published results to compare against. The CER data is a common benchmark but requires an application.
- **Datasets that look like matches but aren't:**
  - The UCI *ElectricityLoadDiagrams* data (370 clients, Portugal) is mostly commercial and industrial customers, not homes.
  - REFIT, UK-DALE and Smart* have only about 5 to 20 homes each.
  - ResStock and Buildings-900K are simulated, not measured.
- **Weather and calendar features:** none of these ship with weather data. You'll need to join it yourself, for example from ERA5, Met Office or Bureau of Meteorology data. Day-ahead benchmarks usually need temperature and holiday calendars.
- **Representativeness:** the datasets cover different countries, years and tariffs, and Ausgrid is PV-only. Using two or three of them would make your benchmark more robust.

I can check the current download links and licenses, or write a loader that puts these into one common schema.