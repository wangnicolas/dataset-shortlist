Four datasets fit what you need. I checked the first two (Porto, T-Drive) against their hosting pages. The other two I could only partly check. For DiDi GAIA, I couldn't open the site from here, so I can't confirm it still works. For Cabspotting, I found no IEEE DataPort page, only a secondary source for the access steps.

## Porto taxis (ECML/PKDD 2015)
- **Contents:** All 442 taxis in Porto, from July 2013 to June 2014. There are about 1.7M complete trips, with a GPS point every 15 seconds in a `POLYLINE` column.
- **Timestamps:** Only the trip start time is stored, as a Unix timestamp. Per-point times are start + 15 s × index. That is fine for travel-time estimation, but some trips have `MISSING_DATA` flagged.
- **Access:** Open and instant, under CC BY 4.0. Download `train.csv.zip` (about 509 MB) from the UCI page, or run `pip install ucimlrepo` and then `fetch_ucirepo(id=339)`. No registration.
- **Fit:** Best default for your use case, because of the fixed sampling rate and the volume.

## T-Drive (Microsoft Research, Beijing)
- **Contents:** 10,357 taxis over one week (Feb 2–8, 2008), about 15M points. Rows are `taxi_id, timestamp, lon, lat`, one file per taxi.
- **Sampling:** Sparse, averaging about 177 s (about 623 m) between points. This is weak for travel-time estimation, but it is widely used as a similarity benchmark. Points are not split into trips, so you segment them yourself.
- **Access:** Open download from the Microsoft page, which links to a OneDrive share and zip files. There is no registration. You are asked to cite the Yuan et al. papers, and the [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf) is linked there.
- **Caveat:** One arXiv paper says six months of data. Microsoft's page says one week, and that is the figure to trust.

## DiDi GAIA Open Data (Chengdu and Xi'an ride-hailing)
- **Contents:** Order IDs, driver IDs, timestamps and lon/lat. The Chengdu data covers Oct–Nov 2016, with a 2018 release at 3 s sampling. The Xi'an data covers Oct–Nov 2016. Both have millions of orders. Papers through 2023 cite it as their source.
- **Access:** Free registration and an application on the GAIA site. A DiDi outreach page names `gaia.didichuxing.com/en` as the "GAIA Open Dataset – Apply Now" page.
- **Problem:** That domain didn't resolve for me, and I found no announcement either way on whether the programme is still running. Check the live site before you plan around it. The terms are likely research-only.

## San Francisco Cabspotting (CRAWDAD epfl/mobility)
- **Contents:** 536 cabs over about 30 days, with timestamped GPS points.
- **Access:** According to Privkit's docs, you log in at IEEE DataPort and click the `cabspottingdata.tar.gz` button. This needs a free account, and CRAWDAD's license terms apply.
- **Not verified:** I didn't confirm the DataPort page itself.

## Rome taxis (CRAWDAD roma/taxi)
This is a possible fourth option. It covers 316 taxis, but sources disagree on the sampling interval (7 s or 15 s) and the duration (25 or 30 days). The IEEE DataPort URL I guessed returned a 404, so I couldn't confirm how to get it. I'd skip it unless you need another city.

## Recommendation
Start with **Porto** for travel-time estimation, since it is open and regular. Add **T-Drive** for similarity benchmarks. The vehicle counts are much higher than your few-hundred minimum. Pursue **DiDi** if you need dense, recent ride-hailing data and can wait on an application.

Sources:
- [UCI Porto dataset](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [T-Drive, Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- [T-Drive user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)
- [DiDi outreach data page](https://outreach.didichuxing.com/SimulationS/data.html)
- [Chengdu DiDi study (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656)
- [Privkit datasets docs](https://privkit.fc.up.pt/privkit.datasets.html)
- [Open Source User Mobility and Activity Datasets (arXiv)](https://arxiv.org/pdf/2110.06382)