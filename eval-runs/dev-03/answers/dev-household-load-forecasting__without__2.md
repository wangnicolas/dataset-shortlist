I haven't checked any of the links or current access terms. Everything below is from memory, so confirm sizes, licences and URLs on each landing page before you commit.

## Meets your criteria

| Dataset | Homes | Resolution | History | Access |
|---|---|---|---|---|
| **GoiEner** (Basque Country, Spain; Zenodo, Scientific Data paper) | ~25,000 | Hourly | Up to several years per customer | **Direct download**, CC-BY |
| **Low Carbon London** (UK Power Networks; London Datastore and Kaggle mirror) | ~5,500 | 30 min | ~2.25 years total (Nov 2011 to Feb 2014), shorter for some homes | **Direct download**, open licence |
| **Irish CER Smart Metering Project** (ISSDA) | ~4,200 residential, plus SMEs | 30 min | ~1.5 years (2009 to 2010) | **Application required**: a form and a data-use agreement. It's free for research, and approval usually takes days. |
| **SGSC Smart Grid Smart City** (Australia; data.gov.au) | Tens of thousands of customers | 30 min | Up to ~3 years, but coverage varies | **Direct download**. The files are large and messy. |
| **Ausgrid Solar Home** (Sydney) | 300 | 30 min | 3 years | **Direct download** from Ausgrid |

## Caveats for day-ahead benchmarking

- **GoiEner:** Start here if you want no application and the most scale. It's the most recent of these, and it has real metadata such as tariff and postcode area. Check how complete each customer's history is, because lengths vary a lot.
- **Low Carbon London:** About 1,100 homes were on a dynamic time-of-use tariff, with prices signalled a day ahead. That affects load, so filter on the standard-tariff group if you want a clean baseline. Many households also have under a year of data.
- **Irish CER:** It's the classic benchmark, so your results are easy to compare with published ones. Timestamps use an odd day-plus-slot encoding, and the dataset mixes in businesses.
- **Ausgrid:** Every home has rooftop solar. Use the gross-load series if you want consumption rather than net load. You can still use it, but it's a different problem from forecasting ordinary homes.

## Common but not a fit

- **UCI ElectricityLoadDiagrams (370 clients, Portugal, 15 min):** Very common in forecasting papers, but it mixes households and businesses and isn't clearly residential.
- **REFIT, UK-DALE, Smart\*, IDEAL:** These have far fewer homes. REFIT has 20 and UK-DALE has 5. IDEAL has about 255 UK homes and is the largest of the group, but it's sensor-oriented and short per home.
- **Pecan Street Dataport:** It has 1-minute, high-quality data. Only a small free academic tier is available, and larger access needs a paid or negotiated agreement.
- **NREL ResStock / EULP:** The loads are simulated, not measured.

## Suggested plan

1. Start with GoiEner and Low Carbon London, since neither needs an application.
2. Submit the ISSDA request now for the CER data, since approval takes time.
3. Use Ausgrid or SGSC as an extra out-of-distribution check.

Should I check the current download links and licences, or pull one of the open datasets into a working directory?