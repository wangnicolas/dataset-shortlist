I'd go with **Porto** first. It's free, already split into trips, has 442 taxis, and is the standard benchmark for trajectory similarity work. Add **DiDi Chengdu/Xi'an** or **Grab-Posisi** if you need dense sampling for travel-time estimation, but getting access to either is less certain.

| Dataset | City / period | Vehicles / scale | Sampling | Split into trips? | How to get it |
|---|---|---|---|---|---|
| **Porto (ECML/PKDD 2015)** | Porto, Jul 2013 – Jun 2014 | 442 taxis, ~1.7M trips | 15 s | Yes, one GPS polyline per trip | Download from the UCI ML Repository ("Taxi Service Trajectory – Prediction Challenge, ECML PKDD 2015") with no login. Or get it from Kaggle's "Taxi Trajectory Prediction" competition (needs a Kaggle account and accepting the rules). |
| **T-Drive (Microsoft Research)** | Beijing, one week in Feb 2008 | ~10,357 taxis, ~15M points | Sparse, ~3 min on average | No | Free download from the Microsoft Research T-Drive page. Cite the Yuan et al. papers. |
| **Cabspotting (CRAWDAD epfl/mobility)** | San Francisco Bay Area, ~30 days, May–Jun 2008 | ~536 taxis | About 1 min | Not directly, but each point has an occupied/empty flag you can split trips on | [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility). The page says you need a DataPort subscription, while papers describe the data as openly available. In practice a free IEEE account login is usually enough, but check. |
| **Rome taxi (CRAWDAD roma/taxi)** | Rome, ~30 days, Feb–Mar 2014 | ~320 taxis | ~7 s | No, and there's no occupancy flag, so you'd have to work out trip boundaries yourself | [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi), same login as above |
| **DiDi GAIA (Chengdu, Xi'an)** | Oct–Nov 2016, later 2018 data too, inside the 2nd Ring Road | Ride-hailing, ~11.75M trips (Chengdu), ~6.72M (Xi'an) | 2–4 s | Yes, points are grouped by order ID | Register on the GAIA portal (gaia.didichuxing.com / outreach.didichuxing.com). It used to be a free registration for academic use. I couldn't confirm it still accepts new users, and recent papers point to a [Kaggle copy](https://www.kaggle.com/datasets/ash1971/didi-dataset/data) instead. That copy may not be an authorised redistribution. |
| **Grab-Posisi** | Singapore and Jakarta, April 2019 | Ride-hailing, 84K trips, ~89M points | 1 s, with speed, bearing and accuracy | Yes | Email Grab with your name, institution and how you'll use the data. The addresses listed are grab-posisi.geo@grab.com (newer) and grab.posisi@grabtaxi.com, so send to both. Non-commercial use only. The program is ~6 years old and may not still respond. |

**How they fit your two tasks:**
- **Trajectory similarity:** Porto, T-Drive and Chengdu/Xi'an are the standard benchmarks, so using them makes your results comparable to published work.
- **Travel-time estimation:** You want dense sampling and clear trip boundaries, which points to DiDi, Grab-Posisi, or Porto. Porto stores only a start timestamp per trip, with points every 15 s after it, so per-point times are implied rather than recorded. T-Drive is too sparse to be good for this.
- **Coordinate conversion:** DiDi coordinates are in China's GCJ-02 system. Convert them to standard WGS-84 GPS coordinates before map-matching against OpenStreetMap (the `eviltransform` package does this).

**Not suitable:** NYC TLC and Chicago taxi data only have pickup and drop-off points. GeoLife is from 182 individual people, not taxis.

Sources:
- [IEEE DataPort – CRAWDAD epfl/mobility](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [IEEE DataPort – CRAWDAD roma/taxi](https://ieee-dataport.org/open-access/crawdad-romataxi)
- [Grab Engineering – Grab-Posisi](https://engineering.grab.com/grab-posisi)
- [Grab-Posisi paper (PDF)](https://engineering.grab.com/files/Grab-Posisi_An_Extensive_Real-Life_GPS_Trajectory_Dataset_in_Southeast_Asia.pdf)
- [Grab-Posisi-L paper](https://yifangyin.github.io/publications/PosisiL.Grab.pdf)
- [PLOS ONE 2025 – uses DiDi Chengdu/Xi'an](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473)
- [PLOS ONE 2019 – DiDi Chengdu trajectories](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656)
- [TRANSFOR19 (DiDi Xi'an, GCJ-02 note)](https://github.com/TRANSFORABJ70/TRANSFOR19)