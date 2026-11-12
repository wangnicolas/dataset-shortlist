Four datasets fit your criteria. Two are plain downloads, one needs a short application, and one is mostly out of reach for a benchmark. I confirmed the London and Zenodo download details by opening those pages. The ISSDA and Pecan Street access details come from search results only, because the ISSDA page returned a 403 when I tried to open it.

## Download directly (no application)

**1. Low Carbon London (UK Power Networks)**
- **What it covers:** 5,567 London households, half-hourly kWh, November 2011 to February 2014. About 1,100 were on dynamic time-of-use tariffs during 2013, and the rest were on a flat tariff. Each row has a household ID, a timestamp and the ACORN group.
- **Access:** Direct links with no login mentioned. The licence is CC BY 4.0. The full file is a 765 MB ZIP holding one CSV of about 167M rows. There is also a split version (168 CSVs) and a 2013 tariffs spreadsheet.
- **Source:** [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households/)
- **Copies:**
  - [Kaggle "Smart meters in London"](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london) adds weather and bank holidays. It needs a Kaggle account.
  - [Zenodo, forecasting-ready, 5,560 series](https://zenodo.org/records/4656091) is open and CC BY 4.0. The version I opened is the one without missing values.
  - [Zenodo, version with missing values](https://zenodo.org/records/4656072)
- **Caveats:**
  - Many households have only a partial history. Not every home has a full year, so check coverage per household.
  - The Zenodo "without missing values" version forward-fills gaps. Consider whether that suits a benchmark.

**2. GoiEner (Spain)**
- **What it covers:** 25,559 hourly series, November 2014 to June 2022, averaging nearly three years each. Raw and imputed versions are provided, plus metadata.
- **Access:** Open on Zenodo under CC BY 4.0. The raw files are 2.0 GB compressed and 15.1 GB uncompressed.
- **Source:** [Zenodo record](https://zenodo.org/records/7362094), described in [Scientific Data](https://www.nature.com/articles/s41597-023-02846-0).
- **Caveat:** The customers include shops, offices and industrial sites as well as homes. Filter them out using the metadata file before benchmarking on households only.

## Application required

**3. Irish CER Smart Metering Trial (ISSDA)**
- **What it covers:** About 4,200 households, half-hourly, July 2009 to December 2010, which is about 18 months. It also has household surveys and the time-of-use tariff trial design.
- **Access:** Search results say it is now on ISSDA Dataverse (DOI 10.7929/ISSDA/BX59EU). You request access and email a signed data request form to issda@ucd.ie. Once approved, you download it directly.
- **Conditions:** Research or teaching use only, for the named project, with all team members listed. The form must be signed for your organisation, and commercial use isn't allowed.
- **Sources:** [ISSDA access page](https://www.ucd.ie/issda/accessdata/) and [ISSDA FAQs](https://www.ucd.ie/issda/faqs/). I couldn't open the dataset page itself, so check the current terms there.

## Probably not suitable

- **Pecan Street Dataport:** It has 15-minute or finer data, but this is a US dataset and the free university tier is small. Search results say 75 homes, though a 2025 post suggests a larger sample, and the sources don't agree. You need an account approved with proof of university affiliation. Full access costs thousands of dollars. See [licences](https://www.pecanstreet.org/dataport/licenses/).
- **SERL Observatory (UK):** It has half-hourly data, but only through a secure researcher-access setup, so it isn't an open download.
- **Ausgrid Solar Home:** It has 300 homes with half-hourly data and rooftop solar. That is below your "hundreds" threshold and the homes are a solar-only population. See the [Ausgrid page](https://www.ausgrid.com.au/Industry/Our-Research/Data-to-share/Solar-home-electricity-data). I didn't check its current access terms.

## Recommendation

Start with Low Carbon London, filtered to households with at least a year of continuous data. GoiEner is the best second dataset because it is much larger, covers a different country, and some homes have several years of history. If you can wait on paperwork, add the Irish CER trial for a third climate and tariff context. Using several datasets also shows whether your benchmark results generalize.

Sources:
- [London Datastore](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households/)
- [Zenodo London (no missing values)](https://zenodo.org/records/4656091)
- [Zenodo London (with missing values)](https://zenodo.org/records/4656072)
- [Kaggle Smart meters in London](https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london)
- [GoiEner on Zenodo](https://zenodo.org/records/7362094)
- [GoiEner in Scientific Data](https://www.nature.com/articles/s41597-023-02846-0)
- [ISSDA access](https://www.ucd.ie/issda/accessdata/)
- [ISSDA FAQs](https://www.ucd.ie/issda/faqs/)
- [Pecan Street licences](https://www.pecanstreet.org/dataport/licenses/)
- [Ausgrid solar home data](https://www.ausgrid.com.au/Industry/Our-Research/Data-to-share/Solar-home-electricity-data)