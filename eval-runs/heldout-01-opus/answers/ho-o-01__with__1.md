Yes. Five datasets clearly meet your needs: three you can download today, and one more after an email request. The Porto taxi dataset is the one to start with. Checked 12 November 2026.

## What I assumed you need
- **R1 (must):** a timestamped sequence of GPS points for each trip, not just the pickup and drop-off.
- **R2 (must):** at least a few hundred vehicles.
- **R3 (nice to have):** trips already split out, or a passenger-on flag so you can split them yourself.
- **R4 (must):** a licence that allows research use. I assumed you don't need commercial use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxis (ECML/PKDD 2015, UCI) | Direct download, minutes | CC BY 4.0 | 442 taxis, 1.71M trips, 509 MB | Strong | today |
| 2 | San Francisco Cabspotting (CRAWDAD epfl/mobility) | Free IEEE account, minutes | Free-account terms, no re-identification allowed | about 536 taxis, 30 days, 91 MB | Strong | today (taxi count from memory) |
| 3 | Grab-Posisi (Singapore, Jakarta) | Request by email, likely days | Research only, no commercial use | 84K trips, 1-second sampling | Strong | today |
| 4 | T-Drive (Beijing) | Direct download (OneDrive), minutes | No licence stated | 10,357 taxis, 1 week | Partial | today |
| 5 | Rome taxis (CRAWDAD roma/taxi) | Free IEEE account, minutes | Free-account terms | about 320 taxis, 30 days, 1.5 GB | Partial | today (taxi count from memory) |
| 6 | Segmented Taxi Trajectories in Bangkok (Zenodo) | Direct download, minutes | CC BY 4.0 | 3 weeks, 34 MB | Unclear: check contents | today |
| 7 | Nanjing ride-hailing, October 2019 (IEEE DataPort) | Paid IEEE DataPort subscription | CC BY 4.0, but behind the paywall | about 400 MB per day | Contents not checked | today |

## Details
1. **Porto**, https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015
   - **Contents:** every trip by all 442 Porto taxis. Each trip is a list of points, one every 15 seconds, plus the trip's start time.
   - **Timestamps:** individual points have no timestamp, but the fixed 15-second interval gives you each point's time.
   - **Fit:** it's the standard benchmark for both trajectory similarity (t2vec, NeuTraj, TrajCL) and travel-time estimation, so you get baselines to compare against.
   - **To get it:** click Download, or run `pip install ucimlrepo` and then `fetch_ucirepo(id=339)`.
   - **Caveats:** some trips have GPS jumps or missing-data flags. The period (July 2013 to June 2014) is from memory; the page doesn't state it.
   - Several copies on figshare and Hugging Face are unofficial, so cite the UCI source.

2. **San Francisco Cabspotting**, https://doi.org/10.15783/C7J010
   - **Contents:** each point has latitude, longitude, an "occupied" flag and a timestamp, so you can cut out passenger trips.
   - **To get it:** create a free IEEE account, log in to IEEE DataPort and download the file. The page says: "Open Access dataset files are accessible to all logged in users."
   - **Caveats:** the data is from May–June 2008, and the sampling interval is roughly a minute (from memory). The terms forbid trying to identify people in the data.

3. **Grab-Posisi**, https://engineering.grab.com/grab-posisi
   - **Contents:** ride-hailing trips from April 2019, one point per second, more than 80M points in total. The densest data here, very good for travel-time labels.
   - **To get it:** email grab.posisi@grabtaxi.com with your name, contact details, institution and intended use.
   - **Terms:** you must cite the SIGSPATIAL 2019 paper, and "You cannot use Grab-Posisi dataset for commercial purposes." The number of drivers isn't stated.

4. **T-Drive**, https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/
   - **Contents:** one week of timestamped points from 10,357 Beijing taxis.
   - **Caveats:** sampling is sparse (about 177 seconds on average, from memory). There's no occupancy flag, so you have to split trips yourself.
   - **Terms:** no licence; the page only asks you to cite two papers.

5. **Rome taxis**, https://doi.org/10.15783/C7QC7M
   - **Contents:** dense traces, roughly one point every 7 seconds (from memory), February–March 2014.
   - **To get it:** same free IEEE DataPort login as Cabspotting.
   - **Caveats:** I believe there's no occupancy flag, so trips have to be inferred. The fleet is close to your minimum.

6. **Bangkok**, https://zenodo.org/records/17003809
   - **Contents:** passenger trips around the Songkran festival (April 2019), with a GPS timestamp field. The description says the trips "combine taxi OD points", so check whether each trip keeps the points in between before relying on it.

7. **Nanjing**, https://doi.org/10.21227/r2ky-gt93
   - **Access:** the page says "This dataset requires an IEEE DataPort Subscription to access."
   - Worth it only if your institution already has a subscription. I didn't check the contents.

## Known, not confirmed
- **DiDi GAIA, Chengdu and Xi'an (2016):** ride-hailing trips with one point every 2–4 seconds and millions of trips (figures from a web search, not the source). It's the main dataset in deep travel-time papers (DeepTTE and later). It used to require free registration at outreach.didichuxing.com. That site timed out for me, so I can't tell whether it still takes applications. Copies on Kaggle are user uploads, and DiDi's terms still apply to them.
- **Harbin (DeepGTT):** the README at https://github.com/boathit/deepgtt links to a Google Drive file of over a million trips from about 13,000 taxis over 5 days. It's widely used for travel-time estimation, but no licence is stated, so ask the authors if you plan to redistribute.
- **Shenzhen, Pingshan district:** a single day in 2019 on ResearchGate. ResearchGate blocked my check, and the size and terms are unknown.

## Not recommended, and why
- **NYC TLC trip records and Chicago Taxi Trips:** pickup and drop-off only (from memory).
- **GeoLife:** 182 people, not taxis.

## What I could not find
- A large, open (CC-licensed) ride-hailing dataset with dense sampling. Grab and DiDi are the closest, and both need a request.
- The literature search was noisy and didn't turn up any further datasets.

## Next step
Download Porto today; it covers both tasks and has published baselines. Email Grab now if you want dense ride-hailing data for travel-time estimation. If you want a second city with a large fleet, add Cabspotting or the Harbin data.

The interactive page with filters and an export of the access plan is at `/private/tmp/e-EV3npE/home/cwd/dataset-shortlist.html`.

Sources: [UCI Porto](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015), [Grab-Posisi](https://engineering.grab.com/grab-posisi), [T-Drive](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/), [DeepGTT repo](https://github.com/boathit/deepgtt), [Kaggle DiDi copy](https://www.kaggle.com/datasets/ash1971/didi-dataset/data), [PLOS ONE Chengdu paper](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656), [DOT paper (Harbin stats)](https://arxiv.org/pdf/2307.03048)