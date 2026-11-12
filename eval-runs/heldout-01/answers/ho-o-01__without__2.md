Here are the ones I know that fit your criteria. I'm going from memory and haven't checked the links or terms live, so confirm each before you build on it.

| Dataset | City / scale | Sampling | What you do to get it |
|---|---|---|---|
| **Porto taxi (ECML/PKDD 2015)** | Porto, 442 taxis, about 1.7M trips, 1.5 years | 15 s | Easiest. Download it from the UCI ML Repository (search "Taxi Service Trajectory – Prediction Challenge") with no login, under CC BY 4.0. It's also on Kaggle, where you need an account and have to accept the rules. |
| **T-Drive (Microsoft Research)** | Beijing, 10,357 taxis, about 15M points, one week in Feb 2008 | Irregular, about 3 min on average | Download from the Microsoft Research T-Drive page. Registration is minimal or none, but you must cite their papers. |
| **Didi GAIA Open Data** | Chengdu and Xi'an, Nov 2016, thousands of cars | 2–4 s | Apply through the GAIA portal with your institution and research purpose. Approval is manual and aimed at academics. Access has changed over time, so check that it's still open. |
| **Rome taxi (CRAWDAD `roma/taxi`)** | Rome, 320 taxis, 30 days in Feb 2014 | About 7 s | Create a free CRAWDAD account and accept the data-use agreement. |
| **San Francisco Cabspotting (CRAWDAD `epfl/mobility`)** | SF, about 536 taxis, about 1 month in 2008 | About 1 min, with an occupancy flag | Same CRAWDAD account and agreement. |

**Notes**
- **Porto**: Each trip is a `POLYLINE` of lon/lat pairs. There is only a start `TIMESTAMP`, so point *i* is at start + 15·*i* s. Some rows are empty or have missing-data flags, so filter them. The dataset has `ORIGIN_CALL` and `TAXI_ID` fields, and trips are already split. This makes it the cleanest for travel-time estimation, because trip duration is the polyline length times 15 s.
- **T-Drive and Cabspotting**: These are continuous per-vehicle logs, not trips. You'll have to segment them yourself. Cabspotting's occupancy flag makes that easy, but T-Drive has no such flag, so you'd split on time gaps or stops. T-Drive also has duplicate and noisy points, and you'll probably want to map-match it.
- **Didi**: It has the densest sampling and real ride-hailing behavior. If you only need a fast start, it's the least convenient of the five.
- **Excluded**: NYC TLC and Chicago taxi data give only pickup/drop-off, so they don't meet your requirement. GeoLife has dense GPS but its 182 users aren't taxis.
- **Possibly restricted**: Shanghai SUVnet (about 4,000 taxis) and Grab-Posisi (Southeast Asia) have been available on request or via past challenges. I'm not sure they're currently open.

**Suggestion**: Start with Porto for both tasks, since its fixed sampling interval makes similarity metrics like DTW, Fréchet and EDR simple to run. Then use T-Drive or Didi to test robustness on irregular or denser sampling. If you want, I can write a loader and trip-segmentation script for any of these.