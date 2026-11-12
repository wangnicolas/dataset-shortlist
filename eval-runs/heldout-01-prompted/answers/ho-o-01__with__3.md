Four datasets fit what you need. Three of them I confirmed on their hosting pages. The fourth, DiDi GAIA, I could not confirm is still open.

## Recommended

**1. Porto taxi (ECML/PKDD 2015): best starting point**
- **Contents:** 442 taxis, 1 Jul 2013 to 30 Jun 2014, with 1,710,671 completed trips. Each trip's `POLYLINE` field is a list of `[lon, lat]` points, one every 15 seconds. The start time is in `TIMESTAMP`, so you can reconstruct a timestamp for every point. The trip's travel time is therefore (number of points − 1) × 15 s.
- **Access:** Free, with no registration. Click Download on the [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015) or run `fetch_ucirepo(id=339)` from the `ucimlrepo` package. The zip is about 509 MB (`train.csv.zip`).
- **License:** CC BY 4.0, so cite the dataset.
- **Gotcha:** The [figshare copy](https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165) keeps only the start and end points. Don't use it for your task.

**2. T-Drive (Beijing)**
- **Contents:** 10,357 taxis, 2–8 Feb 2008, about 15 million points. Each line is `taxi_id, datetime, lon, lat`, with one file per taxi. The sampling is sparse, averaging about 177 s and 623 m between points. That is fine for similarity work, but travel-time estimation will be coarser than with Porto.
- **Access:** No registration. The [Microsoft Research page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/) has a OneDrive download link and zip parts. There is also a [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf).
- **License:** The page states no formal license. It asks you to cite the two Yuan/Zheng papers (KDD '11 and GIS '10).
- **Mirrors:** [Kaggle](https://www.kaggle.com/datasets/arashnic/tdriver) and [IEEE DataPort](https://dx.doi.org/10.21227/rgbn-cw81). I only saw these in search results and did not open them.

**3. Cabspotting (San Francisco, CRAWDAD `epfl/mobility`)**
- **Contents:** About 500 taxis over 30 days (17 May to 10 Jun 2008), as 536 files. Each row is lat, lon, an occupancy flag and a Unix timestamp. The occupancy flag lets you separate paid trips from empty cruising.
- **Access:** You must log in to [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility) and download `cabspottingdata.tar.gz`. CRAWDAD's license requires you to sign a nonexclusive, non-transferable data license agreement. Cite doi:10.15783/C7J010.
- **Caveat:** The search results I found don't state the sampling rate, so check it after downloading. The login-gated download is also not something I could test.

## Uncertain: DiDi GAIA (Chengdu and Xi'an)
- **Contents:** Ride-hailing GPS traces from Oct–Nov 2016, with driver ID, order ID, timestamp, lon and lat. Reported sampling is about 2–4 s, which would be excellent for your task.
- **Access:** Application only, for academic use under DiDi's terms. Third-party repositories don't redistribute it.
- **What I couldn't confirm:** The URL I tried, `outreach.didichuxing.com/research/opendata/en/`, returned a 404. Recent papers and a January 2026 GitHub project still point to `outreach.didichuxing.com/research/opendata/`, but I couldn't check whether applications are open. Papers also disagree on date ranges and sizes. Try that site yourself and expect approval to take time. I would not make it your only data source.

## What I'd do
Start with Porto, which has the most vehicles, the densest regular sampling and the easiest access. Add T-Drive as a second city for generalization. GeoLife is not a taxi dataset, so I left it out.

Sources:
- [UCI Porto taxi](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [Porto on figshare](https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165)
- [T-Drive, Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- [T-Drive user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)
- [CRAWDAD epfl/mobility on IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [DiDi GAIA usage example (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656)
- [DiDi processing repo (GitHub)](https://github.com/neardws/Vehicular-Trajectories-Processing-for-Didi-Open-Data)