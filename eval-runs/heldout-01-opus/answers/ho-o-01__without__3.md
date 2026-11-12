I'd start with **Porto** for trajectory similarity and **DiDi Chengdu/Xi'an** for travel-time estimation. Those are the usual benchmarks in this area: TrajCL, NeuTraj and DeepTTE-style papers all use them, so your results will be comparable to published work.

| Dataset | City | Vehicles | Trips already split? | Sampling | Size / period |
|---|---|---|---|---|---|
| **Porto (ECML/PKDD 2015)** | Porto, PT | 442 taxis | Yes, one polyline per trip | 15 s | 1.71M trips, Jul 2013–Jun 2014 |
| **DiDi GAIA** | Chengdu and Xi'an, CN | Thousands of ride-hailing drivers | Yes, each point has an order ID | 2–4 s | Oct–Nov 2016 (a 2018 release also exists) |
| **T-Drive** | Beijing, CN | 10,357 taxis | No | About 177 s | 15M points, 2–8 Feb 2008 |
| **Grab-Posisi** | Singapore and Jakarta | Ride-hailing drivers | Yes | 1 s | 84K trips, 88.8M points, Apr 2019 |
| **CRAWDAD roma/taxi** | Rome, IT | About 320 taxis* | No | About 7 s* | About 1 month, Feb–Mar 2014* |
| **CRAWDAD epfl/mobility (Cabspotting)** | San Francisco | About 536 taxis* | Has an occupancy flag, so you can split trips | About 60 s* | About 30 days, May–Jun 2008* |

\*From memory; I didn't confirm these against the dataset pages.

## How to get each one

**Porto.** Easiest of the lot. Download the ZIP (about 509 MB) from [UCI](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015), or in Python run `pip install ucimlrepo` then `fetch_ucirepo(id=339)`. The licence is CC BY 4.0 and no account is needed. Two things to watch for:
- Points don't have their own timestamps. Each trip has a start time, and the points in its `POLYLINE` are 15 s apart.
- Use the training set. The test set's trips are deliberately cut short, and you should drop rows where `MISSING_DATA` is true.

**DiDi GAIA.** Hardest to get. The official route is to register at [outreach.didichuxing.com](https://outreach.didichuxing.com/research/opendata/en/) and request the data for academic research. It used to be a free sign-up, but recent papers (late 2026) describe it as "available upon request" under DiDi's terms, so expect an application and some waiting. A third-party copy is on [Kaggle](https://www.kaggle.com/datasets/ash1971/didi-dataset/data), but its licence status is unclear, so check before publishing anything based on it.

**T-Drive.** Free direct download from [Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/). There's one file per taxi with lines of `id, datetime, lon, lat` ([user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)). The catch is that there are no trip boundaries and the sampling is sparse, so you'll have to split trips yourself using stop and time-gap rules. It's not great for travel-time estimation.

**Grab-Posisi.** Email Grab with your name and contact details, your institution, and how you plan to use the data. Two addresses are in circulation: `grab.posisi@grabtaxi.com` ([Grab blog](https://engineering.grab.com/grab-posisi), [ACM paper](https://dl.acm.org/doi/pdf/10.1145/3356995.3364536)) and `grab-posisi.geo@grab.com` ([paper PDF](https://engineering.grab.com/files/Grab-Posisi_An_Extensive_Real-Life_GPS_Trajectory_Dataset_in_Southeast_Asia.pdf)). Try both. It's for non-commercial use only and comes as Parquet files, about 2 GB. Each point also has speed, bearing and accuracy. One caveat: the vehicle count isn't published, and the data is mixed car and motorbike, so check that it meets your "few hundred cars" requirement.

**Rome and San Francisco (CRAWDAD).** Make a free IEEE account, then download from IEEE DataPort: [roma/taxi](https://ieee-dataport.org/open-access/crawdad-romataxi) and [epfl/mobility](https://ieee-dataport.org/open-access/crawdad-epflmobility). [crawdad.org](https://crawdad.org/) says you don't need an IEEE membership. The roma/taxi page does show a "subscription required" notice, though, so you might hit a paywall prompt. If you do, logging in as an IEEE Society member gets you a free subscription. The licence is CC BY 4.0.

**Doesn't fit:** NYC TLC and Chicago taxi data only have pickup and drop-off points, not trajectories.

## Which to use
- **Trajectory similarity:** Porto, plus T-Drive if you want a second city at a coarser sampling rate.
- **Travel-time estimation:** DiDi Chengdu/Xi'an is the standard choice. Porto works if you can't get DiDi, since a trip's duration is 15 s × (number of points − 1). Grab-Posisi is good if you want 1 s sampling.
- **Something usable today with no application:** Porto, T-Drive, Rome and SF.