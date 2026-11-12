Seven datasets meet your requirements well enough to use, and five of them you can download today (three with no account, two with a free IEEE account). Everything below was checked on 2026-11-12 unless marked "from memory".

## What I assumed you need
- **R1 (must):** a timestamped GPS point sequence along each trip, not just pickup and drop-off.
- **R2 (must):** at least a few hundred taxis or ride-hailing vehicles, any city.
- **R3 (nice):** trips identifiable by trip id or occupancy flag, so travel time has ground truth.
- **R4 (nice):** obtainable now for research, with known terms. I assumed academic, non-commercial use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxi (ECML/PKDD 2015) | Direct download, no account | CC BY 4.0 | 442 taxis, 1.71M trips, 15 s | Strong | today |
| 2 | San Francisco cabspotting (CRAWDAD epfl/mobility) | Free IEEE account, minutes | CC BY | ~500 taxis, 25 days | Strong | today |
| 3 | Rome taxi (CRAWDAD roma/taxi) | Free IEEE account, minutes | CC BY | ~320 taxis, 30 days, 7 s | Strong | today |
| 4 | Harbin taxi (DeepGTT release) | Direct download from Google Drive | None stated | ~13,000 taxis, 1M+ trips, 5 days | Strong | today (file not downloaded) |
| 5 | T-Drive sample (Beijing) | Direct download link; it refused my automated check | None stated, citation requested | 10,357 taxis, 1 week, ~177 s | Partial | page today, link not confirmed |
| 6 | Grab-Posisi (Singapore, Jakarta) | Email request, research only, likely weeks | Non-commercial | 84K trajectories, 1 s | Strong | terms today, mailbox not confirmed |
| 7 | Segmented Taxi Trajectories in Bangkok | Direct download | CC BY 4.0 | 33.5 MB, fleet size not stated | Partial | today |

## Details

**1. Porto taxi** — [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- **Contents:** one row per trip from all 442 Porto taxis, with a polyline of one coordinate pair every 15 seconds.
- **Missing:** there is no timestamp per point, only the trip start. You reconstruct times as start + 15 s × index, and should drop rows flagged `MISSING_DATA`.
- **Steps:** open the page and click Download (509 MB zip). The download URL answered today.
- **Used by:** [taxi destination prediction, PLOS ONE 2018](https://doi.org/10.1371/journal.pone.0194629); [road-network trajectory similarity, MDPI 2026](https://www.mdpi.com/2227-7390/14/22/4119).
- The collection period (July 2013 to June 2014) is from memory; the page does not state it.

**2. San Francisco cabspotting** — [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- **Contents:** one file per taxi; each line is latitude, longitude, occupancy and a UNIX timestamp, from 17 May to 10 June 2008.
- **Why it fits:** the occupancy flag lets you cut the stream into passenger trips with real durations.
- **Missing:** sampling is irregular, roughly 30–60 seconds.
- **Steps:** create a free IEEE account (membership not required), log in, download `cabspottingdata.tar.gz` (90.7 MB).
- The page also says a "DataPort Subscription" is required; for open-access entries it states files are "accessible to all logged in users". Terms forbid re-identifying drivers.

**3. Rome taxi** — [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)
- **Contents:** driver id, timestamp and position every 7 seconds for about 320 taxis, 1 February to 2 March 2014.
- **Missing:** no occupancy flag or trip ids, so trip boundaries are your own heuristic. That weakens it for travel-time ground truth; it is better for similarity.
- **Steps:** same free IEEE login, then download `taxi_february.tar.gz` (374 MB).

**4. Harbin taxi (DeepGTT)** — [GitHub repo](https://github.com/boathit/deepgtt)
- **Contents:** over 1M trips from roughly 13,000 taxis across 5 days, already segmented, with `lon`, `lat` and `tms` per point in one HDF5 file per day.
- **Why it fits:** it was released for travel-time estimation ([DeepGTT paper, WWW 2019](https://xiucheng.org/assets/pdfs/www19-deepgtt.pdf)).
- **Steps:** follow the Google Drive link in the README, extract the `.h5` files, read with `h5py`.
- **Caveats:** no licence is stated, so ask the author before redistributing. The README does not name the city (the repo folder is `harbin`). It sits on a personal Drive; the link answered today but I did not download the file.

**5. T-Drive sample** — [Microsoft Research page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- **Contents:** taxi id, datetime, longitude, latitude for 10,357 Beijing taxis, 2–8 February 2008.
- **Missing:** no trip boundaries or occupancy flag, and points are about 3 minutes apart on average. It is fine for similarity search at scale and weak for travel time.
- **Steps:** open the page in a browser and click "Download the Trajectory Data" (OneDrive); cite the two T-Drive papers named there.
- The OneDrive link returned 403 to my client, so I could not confirm it works. A Kaggle copy (`arashnic/tdriver`) exists but is an unofficial mirror.

**6. Grab-Posisi** — [Grab engineering blog](https://engineering.grab.com/grab-posisi), [paper](https://doi.org/10.1145/3356995.3364536)
- **Contents:** 84K ride-hailing trajectories from April 2019 at 1-second sampling, with trajectory id, position, UTC timestamp, accuracy, bearing and speed (about 2 GB).
- **Missing:** no driver or vehicle ids, and the fleet size is not stated. Jakarta includes motorcycles.
- **Steps:** email grab.posisi@grabtaxi.com with your name, contact details, institution and intended use. If there is no reply, the paper PDF gives grab-posisi.geo@grab.com.
- **Terms:** research only; "You cannot use Grab-Posisi dataset for commercial purposes." The announcement dates from 2019 and I could not confirm the mailbox is still staffed.

**7. Bangkok segmented taxi trajectories** — [Zenodo record](https://zenodo.org/records/17003809)
- **Contents:** taxi probe points from 4–24 April 2019 with vehicle id, per-point timestamp, speed, heading, for-hire light and `trajectory_id`.
- **Missing:** the record does not state the number of taxis, and sampling is 1–3 minutes. Count distinct vehicle ids before relying on it.
- **Steps:** download three zip files (33.5 MB total).

## Known, not confirmed
- **Shenzhen Urban Data Release** ([Rutgers page](https://people.cs.rutgers.edu/~dz220/data.html)): about 14,700 taxis for one day with an occupancy flag, academic use only. The page is live, but all three taxi download links on it returned 404 today. Email the maintainer (Desheng Zhang) if you want it. A one-day file for 664 electric taxis on the same page is still live.
- **Chengdu taxi, August 2014** (14,864 taxis, used by DeepTTE): only an 1,800-trajectory sample is in the [DeepTTE repo](https://github.com/UrbComp/DeepTTE). The full set came from a closed competition, from memory.
- **Shanghai SUVnet 2007** (about 4,000 taxis): papers use it, but I found no official host.

## Not recommended, and why
- **DiDi GAIA Chengdu / Xi'an:** no longer offered. The [DiDi portal](https://outreach.didichuxing.com/opendata/datasets) now lists only a synthetic ride-hailing time series; Kaggle copies are unofficial mirrors of data that, from memory, was released under a signed agreement.
- **NYC TLC and Chicago taxi trips:** pickup and drop-off only (from memory).
- **Figshare "San Francisco / Porto taxi trajectories":** derived copies; the San Francisco one is reduced to start time and endpoints.
- **SZ-taxi (T-GCN):** road-segment speeds, not trajectories.
- **Barcelona vehicular mobility traces (Zenodo):** simulated in SUMO.

## What I could not find
- No openly downloadable real ride-hailing trajectories; Grab-Posisi by email is the only route.
- The literature search tool returned almost nothing relevant, and the ACM 2025 vehicle-trajectory survey refused the fetch, so its dataset table is unread. Less-known datasets may be missing from this list.

## Next step
Start with Porto and the DeepGTT Harbin release today: both are trip-segmented, so they serve similarity and travel time directly. Add San Francisco if you want true per-point timestamps with occupancy, and send the Grab email now, since that is the slow one.

The interactive version, with filters and an exportable access plan, is at `/private/tmp/e-tbltot/home/cwd/dataset-shortlist.html`.

Sources:
- [UCI: Taxi Service Trajectory, ECML PKDD 2015](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [IEEE DataPort: CRAWDAD epfl/mobility](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [IEEE DataPort: CRAWDAD roma/taxi](https://ieee-dataport.org/open-access/crawdad-romataxi)
- [boathit/deepgtt](https://github.com/boathit/deepgtt) and [DeepGTT paper](https://xiucheng.org/assets/pdfs/www19-deepgtt.pdf)
- [Microsoft Research: T-Drive trajectory data sample](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/) and [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)
- [Grab-Posisi blog](https://engineering.grab.com/grab-posisi) and [paper](https://doi.org/10.1145/3356995.3364536)
- [Zenodo: Segmented Taxi Trajectories in Bangkok](https://zenodo.org/records/17003809)
- [Desheng Zhang's data page, Rutgers](https://people.cs.rutgers.edu/~dz220/data.html)
- [DiDi outreach datasets page](https://outreach.didichuxing.com/opendata/datasets)
- [UrbComp/DeepTTE](https://github.com/UrbComp/DeepTTE)
- [MDPI: Road-Network Trajectory Similarity Learning](https://www.mdpi.com/2227-7390/14/22/4119)
- [PLOS ONE: Multi-features taxi destination prediction](https://doi.org/10.1371/journal.pone.0194629)
- [GitHub issue on DiDi Chengdu/Xi'an availability](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3)