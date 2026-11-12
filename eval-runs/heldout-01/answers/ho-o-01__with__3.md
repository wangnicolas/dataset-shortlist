The best fit is the Porto taxi dataset: 442 taxis with a GPS point every 15 seconds along every trip, and you can download it today. Four more have full point sequences from a few hundred vehicles or more: T-Drive, DiDi GAIA, San Francisco and Rome. Grab-Posisi also has them but isn't a taxi dataset (see its row). The registries (Zenodo, DataCite, OpenAIRE, Hugging Face) mostly returned noise, so the datasets below come from web search. I did not build the interactive shortlist page.

I checked these on 2026-11-11. "Confirmed" means I read it today from the source named. "Memory" means I believe it but didn't confirm it.

## What I assumed you need
- **R1 (must):** timestamped GPS points along each trip, not only pickup and drop-off.
- **R2 (must):** at least a few hundred vehicles, taxi or ride-hailing, any city.
- **R3 (nice):** a sampling interval fine enough for travel-time estimation and similarity measures.
- **R4 (nice):** downloadable today. I assumed you're doing academic, non-commercial work.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxi (ECML/PKDD 2015) | Direct download | CC BY 4.0 (memory; UCI page's licence text didn't load) | 442 taxis, 1.71M trips, 1 year, point every 15 s | Strong | Today (contents); licence from memory |
| 2 | CRAWDAD epfl/mobility (San Francisco cabs) | Free IEEE DataPort account | Not stated on the page; no-deanonymisation clause | ~500 cabs, 25–30 days, ~11M points | Strong | Today |
| 3 | CRAWDAD roma/taxi (Rome) | Free IEEE DataPort account | Not stated on the page; no-deanonymisation clause | ~320 taxis, ~30 days, 15 s | Strong | Today (access); contents from search |
| 4 | T-Drive (Beijing) | Download link on Microsoft Research page | Not confirmed; citation requested | 10,357 taxis, 1 week, ~15M points, ~177 s average gap | Partial: sparse sampling | Today (page); details from search |
| 5 | DiDi GAIA (Chengdu, Xi'an) | Application and approval (memory) | DiDi's terms (memory) | Millions of orders, ~3 s sampling (per papers) | Strong if you get it | Not confirmed: official site returned HTTP 501 |
| 6 | Grab-Posisi (Singapore, Jakarta) | Email request, a few days to weeks | Non-commercial | ~84K trajectories, 80M+ pings, 1 s | Strong | From search results only |

## Details

**1. Porto.** All trips are in one CSV, one row per completed trip. Each row has a `POLYLINE` of GPS points, taxi ID, start timestamp, and call type.
- **Access:** take it from the [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015). The challenge's own page is at geolink.pt, and Kaggle has a copy of the competition data. The UCI page confirms 442 taxis, 1,710,671 trips and 2013-07-01 to 2014-06-30. The 15 s sampling interval came from a web search summary, not from the page itself.
- **Travel time:** trip duration is (number of points − 1) × 15 s, so it needs no separate label.
- **Caveats:** UCI says the data has missing values. Some papers report missing GPS updates, so filter trips with too few points.
- **Papers using it:** [first-place neural-network solution](https://arxiv.org/pdf/1508.00021) and [BlueTaxi](https://arxiv.org/pdf/1509.05257), which also covers trip-time prediction.
- **Don't use the figshare "Porto taxi trajectories" record.** It keeps only the origin and destination of each trip (checked in its record). The Hugging Face copies are unofficial and I didn't check them.

**2. San Francisco (Cabspotting).**
- **Access:** create a free IEEE DataPort account, log in at [the dataset page](https://ieee-dataport.org/open-access/crawdad-epflmobility), and download `cabspottingdata.tar.gz` (about 91 MB). I confirmed this today. The DOI is 10.15783/C7J010.
- **Contents:** one file per cab, with latitude, longitude, an occupied flag and a Unix timestamp. These details are from search results.
- **Licence:** the page states no licence. It asks you not to try to re-identify people.
- **Don't use the figshare "San Francisco taxi trajectories" record.** It is also origin/destination only.

**3. Rome.**
- **Access:** same route as San Francisco, using a free IEEE DataPort login on [the roma/taxi page](https://ieee-dataport.org/open-access/crawdad-romataxi). I confirmed the login requirement today. The DOI is 10.15783/C7QC7M.
- **Contents:** about 320 taxis in central Rome, roughly February to March 2014, with taxi ID, timestamp, latitude and longitude (from search results, not confirmed).
- **Licence:** none stated. The same no-deanonymisation clause applies.

**4. T-Drive.**
- **Access:** use the "Download the Trajectory Data" link on the [Microsoft Research page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/). I saw the link there today. The [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf) asks you to cite the two Yuan et al. papers.
- **Licence:** I couldn't confirm any licence terms.
- **Why partial:** the average gap is about 3 minutes and about 600 m. That is too coarse for good point-level similarity or segment-level travel times. It is fine for coarse similarity benchmarks.
- **Don't trust the six-month claim.** One arXiv paper says six months, but Microsoft's page says one week (2–8 February 2008).

**5. DiDi GAIA.**
- **What it holds:** ride-hailing trajectories and orders for Chengdu (November 2016) and Xi'an (October to November 2016), with later 2018 releases, sampled about every 3 s. That comes from papers, not the official page.
- **Access:** the data is on DiDi's Open Data portal, `outreach.didichuxing.com/research/opendata/`. Older papers describe free registration. A January 2026 GitHub note says you now apply and agree to DiDi's terms. Expect an application and approval step, but I couldn't confirm the wait or the licence.
- **Status:** the official page returned HTTP 501 to me, and I found no announcement of a shutdown. Confirm it's live before you plan around it. Don't use mirrors of this data.
- **Papers using it:** the [Annals of GIS floating-car study](https://www.tandfonline.com/doi/full/10.1080/19475683.2023.2166109) and [RouteKG](https://arxiv.org/pdf/2310.03617).

**6. Grab-Posisi.**
- **Access:** email grab.posisi@grabtaxi.com with your name, institution and intended use. The [dataset page is here](https://engineering.grab.com/grab-posisi) and the [paper is here](https://dl.acm.org/doi/10.1145/3356995.3364536).
- **Terms:** non-commercial use only.
- **Contents:** one Parquet file per trajectory, about 2 GB in total, with 1 s pings that include speed and bearing. This is Southeast Asian ride-hailing data from search results.
- **What I didn't confirm:** whether the programme is still answering requests.

## Known, not confirmed
- **Shanghai taxi data:** the [TaxiSH figshare record](https://doi.org/10.6084/m9.figshare.31481464.v2) is CC BY 4.0, but it's an aggregated 1 km grid of flows derived from 2.16 billion GPS records. It is not raw trajectories, so I'd skip it.
- **Pingshan District, Shenzhen:** [one day of taxi GPS trips](https://doi.org/10.13140/rg.2.2.20676.80007), hosted on ResearchGate. No licence or access terms are stated, and I couldn't confirm the contents.
- **Bangkok:** [segmented taxi trajectories](https://zenodo.org/records/17005200) on Zenodo, CC BY 4.0, open, from the ITIC Foundation's taxi probe data. I didn't check the sampling or fleet size. The ITIC original may offer more.
- **Shanghai SUVnet taxi traces:** from memory, these are available only by application to the Shanghai Jiao Tong University group. I didn't search for them.

## Not recommended
- **GeoLife:** it records walkers and cyclists, not taxis.
- **NYC TLC trip records:** they have pickup and drop-off only.
- **Uber Movement:** it publishes aggregated travel times, with no points.
- **Zenodo "NYC telematics data":** it comes from instrumented research cars on 15 to 30 minute drives, not a taxi fleet.

## What I could not find
- A clean official-page confirmation of the Porto licence.
- Any licence terms for T-Drive, San Francisco or Rome.
- Whether DiDi GAIA and Grab-Posisi are accepting requests today.

## Next step
Start with Porto, which is open and well suited to both of your tasks. Add San Francisco and Rome the same day with a free IEEE DataPort login. Email Grab and apply to DiDi now, since those two take time.