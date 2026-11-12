Yes: seven datasets fit, and five of them you can download today. Porto is the one to start with, because it is already cut into trips and is the usual benchmark for both of your tasks. Everything below was checked on 11–12 November 2026; anything marked "from memory" was not confirmed on a page.

## What I assumed you need
- **R1 (must):** timestamped GPS points along the route, not just pickup and drop-off.
- **R2 (must):** at least a few hundred taxis or ride-hailing cars, any city.
- **R3 (nice):** trips identifiable by a trip id or occupancy flag, so per-trip travel time is defined.
- **R4 (nice):** obtainable now, without an application. I assumed academic use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxi (ECML/PKDD 2015) | Direct download, minutes | CC BY 4.0 | 442 taxis, 1.71M trips, 15 s | Strong | today |
| 2 | Bangkok taxi probe data (iTIC) | Direct download, minutes | CC BY 4.0 | 2017–2025, about 1 point/min | Partial | today |
| 3 | San Francisco cabs (CRAWDAD epfl/mobility) | Free IEEE DataPort account, minutes | CC BY 4.0 | about 500 taxis, 25 days | Strong | today (login not tested) |
| 4 | Rome taxis (CRAWDAD roma/taxi) | Free IEEE DataPort account, minutes | CC BY 4.0 | about 320 taxis, 30 days, 7 s | Partial | today (login not tested) |
| 5 | Harbin taxis (DeepGTT release) | Google Drive link, minutes | None stated | 13,000+ taxis, 1M+ trips, 5 days | Strong | today (file download not tested) |
| 6 | T-Drive, Beijing | Direct download, minutes | None stated | 10,357 taxis, 1 week, about 15M points | Partial | today (download not tested) |
| 7 | Grab-Posisi (Singapore, Jakarta) | Email request, wait unknown | Research only, no commercial use | 84K trips, 1 s | Partial | today (request route not tested) |

## Details

**1. [Porto taxi](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)**
- **Contents:** each row is one completed trip with a start timestamp and a polyline with "one pair of coordinates for each 15 seconds of trip".
- **Catch:** per-point timestamps are implicit (start + 15 s × index). Drop trips flagged as having missing data before computing travel times.
- **Steps:** open the UCI page and click Download (about 509 MB, no account). The zip link answered today.
- **Used in:** [destination prediction, PLOS ONE 2018](https://doi.org/10.1371/journal.pone.0194629); [trajectory generation, arXiv 2511.16105](https://arxiv.org/abs/2511.16105).

**2. [Bangkok taxi probe data](https://itic.longdo.com/opendata/probe-data/)**
- **Contents:** one CSV per day with vehicle id, lat, lon, timestamp, speed, heading, for-hire light and engine status.
- **Catch:** sampling is one point per minute (three with the engine off), and there is no trip id, so you split on the for-hire light. Fleet size is not stated at the source; papers report roughly 4,200–4,800 taxis.
- **Steps:** download the monthly `PROBE-YYYYMM.tar.bz2` archives you want (0.8–2.7 GB each) and read `README.TXT` for the format. No login.
- **Used in:** [Bangkok metro expansion study, 2024](https://www.nature.com/articles/s44333-024-00020-6).

**3. [San Francisco cabs](https://ieee-dataport.org/open-access/crawdad-epflmobility)**
- **Contents:** one file per cab; each line is lat, lon, occupancy flag, Unix time, covering 17 May to 10 June 2008.
- **Catch:** sampling is roughly one point per minute (from memory).
- **Steps:** create a free IEEE account, log in to IEEE DataPort, download `cabspottingdata.tar.gz` (91 MB), then split on the occupancy flag.
- **Access caveat:** the page also shows a "requires a Subscription" banner, but the [DataPort FAQ](https://ieee-dataport.org/faq/do-i-have-subscribe-ieee-dataport-order-download-datasets-and-tools-ieee-dataport) says Open Access datasets need only a registered account.

**4. [Rome taxis](https://ieee-dataport.org/open-access/crawdad-romataxi)**
- **Contents:** driver id, timestamp and position every 7 seconds, 1 February to 2 March 2014.
- **Catch:** no occupancy flag or trip id, so travel-time labels depend on your own stop-based segmentation.
- **Steps:** same free IEEE DataPort login as San Francisco, then download `taxi_february.tar.gz` (374 MB).

**5. [Harbin taxis](https://github.com/boathit/deepgtt)**
- **Contents:** one HDF5 file per day; each trip has lon, lat and timestamp arrays. It was released for a travel-time estimation paper.
- **Catch:** no licence is stated, it is a subset of the paper's data, and it sits on a personal Google Drive.
- **Steps:** follow the Google Drive link in the README and extract the `.h5` files.

**6. [T-Drive, Beijing](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)**
- **Contents:** per-taxi streams of id, time, lon, lat (field list from memory).
- **Catch:** no occupancy flag or trip id, and sampling averages about 3 minutes (both from memory). It suits similarity on coarse traces, not per-trip travel time.
- **Steps:** use the OneDrive link or the nine zip parts on the page, and cite the two papers listed there.
- **Used in:** [frequent pattern mining comparison, 2022](https://doi.org/10.3390/s22197608).

**7. [Grab-Posisi](https://engineering.grab.com/grab-posisi)**
- **Contents:** trajectory id, lat, lon, UTC timestamp, accuracy, bearing and speed at 1 s, collected April 2019, about 2 GB of Parquet.
- **Catch:** the number of drivers is not stated, real start and end points are removed, and cars are mixed with motorcycles.
- **Steps:** email grab.posisi@grabtaxi.com with your name, contact details, institution and intended use. If it bounces, try grab-posisi.geo@grab.com, the address in Grab's copy of the paper.
- **Access caveat:** the request page dates from 2019 and I could not confirm anyone still answers.
- **Described in:** [Huang et al., 2019](https://doi.org/10.1145/3356995.3364536).

## Known, not confirmed
- **[Shenzhen taxi GPS (UrbanCPS, Rutgers)](https://people.cs.rutgers.edu/~dz220/Data.html):** it has an occupancy flag and is marked "for academic research only"; a paper reports about 14k taxis. The download link on the page returned 404 today, so email the authors.
- **Shanghai SUVnet taxi traces:** papers describe about 4,400 taxis in February 2007, but I found no live download page.
- **Porto via Kaggle:** the two competition pages hold the same data, but need a Kaggle account and acceptance of the rules (from memory; the pages could not be read).

## Not recommended, and why
- **DiDi GAIA Chengdu / Xi'an:** the official portal returned an error today, and a [recent GitHub issue](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3) reports the trajectory sets are gone. Kaggle copies are unofficial re-uploads of data released under DiDi's research terms.
- **[IEEE DataPort "Taxi trajectories"](https://ieee-dataport.org/documents/taxi-trajectories):** New York only, behind a paid subscription, and the two 50 MB spreadsheets look like trip records.
- **[Figshare](https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165) and [Hugging Face](https://huggingface.co/datasets/kraina/porto_taxi) Porto copies:** derived versions (origin–destination only, or hexagon-aggregated). Use the UCI original.
- **NYC TLC and Chicago trip records:** pickup and drop-off only (from memory).

## What I could not find
- No officially downloadable ride-hailing set at DiDi scale; Grab-Posisi is the only ride-hailing option.
- The registry search returned mostly noise, and the paper search covered this field thinly, so the "used in" lists are short and there may be newer sets I missed.

## Next step
Download Porto now, and add San Francisco if you want a second city with clean trip boundaries. Send the Grab-Posisi email today if you want 1-second ride-hailing data, since the wait is unknown.

The interactive version, with filters and an exportable access plan, is at `/private/tmp/e-hKbLAN/home/cwd/dataset-shortlist.html`.