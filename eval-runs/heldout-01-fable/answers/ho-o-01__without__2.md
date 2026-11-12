Yes. Four are downloadable today and fit your spec; two well-known ones are gated or effectively gone. I checked the access pages for all six today; Porto's dates and T-Drive's dates and sampling interval are from memory.

| Dataset | Fleet and span | Sampling | What you have to do |
|---|---|---|---|
| **Porto taxi (ECML/PKDD 2015)** | 442 taxis, 1.71M trips, Jul 2013–Jun 2014 | 15 s | Direct download from UCI (about 509 MB zip), no login shown, CC BY 4.0. Also on Kaggle, which needs an account. |
| **T-Drive (Beijing, Microsoft Research)** | 10,357 taxis, about 15M points, one week in Feb 2008 | Irregular, about 3 min on average | Direct download from the Microsoft Research page (OneDrive folder or zip parts). No licence stated; they ask you to cite two papers. |
| **Cabspotting / CRAWDAD epfl/mobility (San Francisco)** | About 500 taxis, 17 May–10 Jun 2008 | Under 10 s on average | Log in to IEEE DataPort with a free IEEE account, then download. CC BY 4.0. |
| **CRAWDAD roma/taxi (Rome)** | About 320 taxis, 1 Feb–2 Mar 2014 | About 7 s | Same as Cabspotting: IEEE DataPort login. CC BY 4.0. |
| **Grab-Posisi (Singapore, Jakarta)** | 84K ride-hailing trajectories, 80M+ pings, April 2019 | 1 s | Email Grab with your name, institution and intended use; non-commercial research only. |
| **DiDi GAIA (Chengdu, Xi'an)** | Ride-hailing orders, Oct–Nov 2016 | 2–4 s | Probably not obtainable now; see below. |

- **Porto:** This is the best starting point for both of your tasks, because it is already split into trips. Each row holds a start timestamp plus a polyline, so per-point times are implied (start + 15 s × index) rather than stored. Trip duration is (points − 1) × 15 s, and there is a flag for rows with missing GPS data.
- **T-Drive:** It has the largest fleet, but it is continuous vehicle traces with no trip boundaries or occupancy flag. The sparse sampling makes it weak for travel-time estimation, though it is common in similarity work.
- **Cabspotting:** Each point has lat, lon, an occupancy flag and a Unix timestamp, so you can cut passenger trips yourself.
- **Rome:** Each point has driver ID, timestamp and position, with no occupancy flag, so trips have to be inferred from stops.
- **IEEE DataPort access:** Both CRAWDAD pages say open-access files are available to any logged-in free account, but also mention a "DataPort Subscription". The wording is inconsistent, so expect the free login to work but confirm when you try.
- **Grab-Posisi:** The contact addresses are grab.posisi@grabtaxi.com (Grab's blog) and grab-posisi.geo@grab.com (paper footnote). The blog post is years old and I could not confirm which is still monitored, so email both. Vehicle IDs are not included, only trajectory IDs, and Jakarta includes motorcycles.
- **DiDi GAIA:** It used to need only free registration on DiDi's outreach portal. A recent GitHub issue reports that only a synthetic dataset remains there, and a November 2026 paper describes the data as available only by request to DiDi. I found no official closure notice and no legitimate mirror.

NYC TLC and Chicago taxi data are pickup/drop-off only, so they do not meet your requirement. Harbin and Shenzhen taxi sets also appear in the literature, but I did not check their current availability.

Sources:
- [Porto taxi, UCI](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [T-Drive, Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- [CRAWDAD epfl/mobility, IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [CRAWDAD roma/taxi, IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)
- [Grab-Posisi, Grab engineering blog](https://engineering.grab.com/grab-posisi)
- [Grab-Posisi paper](https://engineering.grab.com/files/Grab-Posisi_An_Extensive_Real-Life_GPS_Trajectory_Dataset_in_Southeast_Asia.pdf)
- [GitHub issue on DiDi Chengdu/Xi'an access](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3)
- [MDPI paper with DiDi data availability statement](https://www.mdpi.com/2227-7390/14/22/4119)
- [PLOS ONE paper noting earlier free registration for DiDi data](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656)