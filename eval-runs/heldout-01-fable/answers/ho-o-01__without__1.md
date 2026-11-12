Yes, there are six worth knowing: three you can download today, two that sit behind a login or an email request, and one widely used benchmark whose official source has gone. I checked the access pages today but did not download any of the files.

| Dataset | Fleet and period | Sampling | Trip structure | How to get it |
|---|---|---|---|---|
| **Porto taxi** (ECML/PKDD 2015) | 442 taxis, Jul 2013 – Jun 2014, 1.71M trips | 15 s | One row per trip, with the point sequence | Direct download from UCI (509 MB, CC BY 4.0), no account needed |
| **T-Drive** (Beijing, Microsoft Research) | 10,357 taxis, 2–8 Feb 2008, ~15M points | ~177 s average | None: one continuous stream per taxi, no occupancy flag | OneDrive link on the Microsoft Research page; no licence stated; cite the two T-Drive papers |
| **Shenzhen taxi** (Rutgers Urban Data Release) | Reportedly ~14k taxis, one day (22 Oct 2013) | ~20 s reported | Stream per taxi with an occupancy flag | Direct download links on Desheng Zhang's Rutgers page |
| **San Francisco cabspotting** (CRAWDAD epfl/mobility) | 536 taxis, 17 May – 10 Jun 2008, ~11M points | ~30–60 s | Stream per taxi with an occupancy flag | IEEE DataPort login, 91 MB, CC BY |
| **Rome taxi** (CRAWDAD roma/taxi) | ~320 taxis, 30 days, Feb–Mar 2014 | ~7 s (from memory) | Stream per taxi, no occupancy flag | IEEE DataPort login |
| **Grab-Posisi** (Singapore, Jakarta) | 84K trajectories, Apr 2019, ~80M pings | 1 s | One trajectory per ride, with speed, bearing and accuracy | Email request to Grab; non-commercial only |
| **DiDi GAIA** (Chengdu, Xi'an) | Ride-hailing, Oct–Nov 2016 | 2–4 s | Order IDs per trip | Apparently no longer on DiDi's portal; unofficial copies only |

What to know before choosing:

- **Porto:** This is the best starting point because it is already split into trips and is a standard benchmark for both of your tasks. Only the trip start time is stored, so you derive each point's timestamp as start + 15 s × index. Drop rows flagged `MISSING_DATA`.
- **T-Drive:** The fleet is large, but the sparse sampling and lack of trip boundaries make it weak for travel-time work. You would have to segment trips yourself from stops.
- **Shenzhen and San Francisco:** The occupancy flag lets you cut the streams into passenger trips with real start and end times. Shenzhen covers only one day.
- **IEEE DataPort (San Francisco and Rome):** The page contradicts itself. It says open-access files are available to any logged-in user with a free IEEE account, and also says a DataPort subscription is required (free for IEEE Society members). Try a free account first.
- **Grab-Posisi:** Send your name, institution and intended use. Two contact addresses are published (grab.posisi@grabtaxi.com and grab-posisi.geo@grab.com), so email both. The release has trajectory IDs rather than vehicle IDs, so your "few hundred vehicles" requirement can't be checked directly. I couldn't confirm that requests are still being answered.
- **DiDi:** A recent GitHub issue reports that only a synthetic dataset remains on outreach.didichuxing.com. Recent papers point to a Kaggle copy (`ash1971/didi-dataset`), whose contents and licensing I did not check. Treat redistribution rights as unclear if you plan to publish.

NYC TLC and Chicago taxi data are pickup and drop-off only, so they don't fit.

Sources:
- [Porto taxi – UCI](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [T-Drive – Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/) and [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)
- [Shenzhen – Rutgers Urban Data Release](https://www.cs.rutgers.edu/~dz220/data.html)
- [CRAWDAD epfl/mobility – IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [CRAWDAD roma/taxi – IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)
- [Grab-Posisi blog post](https://engineering.grab.com/grab-posisi) and [paper](https://engineering.grab.com/files/Grab-Posisi_An_Extensive_Real-Life_GPS_Trajectory_Dataset_in_Southeast_Asia.pdf)
- [DiDi availability – GitHub issue](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3) and [PLOS ONE paper citing the Kaggle copy](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473)