Three datasets fit your needs. Two are easy to get, and the third (Didi) is currently hard to get.

## Recommended

**1. Porto taxis (ECML/PKDD 2015)**
- **Contents:** 442 taxis over July 2013 to June 2014, about 1.7M trips. Each trip has a `POLYLINE` field, a list of WGS84 points sampled every 15 s. I confirmed this on the UCI page.
- **Access:** Free, with no application. Download the 509 MB zip from [UCI](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015), or run `pip install ucimlrepo` and then `fetch_ucirepo(id=339)`. The same data is on the [Kaggle competition page](https://www.kaggle.com/competitions/pkdd-15-predict-taxi-service-trajectory-i/data), which needs a Kaggle login.
- **License:** CC BY 4.0, so you only need to credit it.
- **Caveats:** Timestamps are per trip (start time only). You infer each point's time as start + 15 s × index. Don't use the [figshare version](https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165). It keeps only the source and target points, not the full path.
- **Fit:** This is the best match for you. It's clean, large and openly licensed, and it's widely used for similarity and travel-time work.

**2. T-Drive (Beijing)**
- **Contents:** 10,357 taxis over one week (Feb 2–8, 2008), about 15M points. Each line is `taxi id, datetime, lon, lat`, and each taxi has its own file.
- **Access:** Free, with no application. Use the OneDrive link on the [Microsoft Research page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/). The page asks you to cite the two Yuan et al. papers (KDD '11 and GIS '10) and states no formal license. The [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf) is a separate PDF. There are mirrors on [Kaggle](https://www.kaggle.com/datasets/arashnic/tdriver) and [IEEE DataPort](https://ieee-dataport.org/documents/poetic-tdrive-and-nyc-database).
- **Caveats:** Sampling is sparse, about 177 s or 620 m between points. The data is a continuous log per taxi, so you have to split it into trips yourself. It is also old. Similarity benchmarks work, but travel-time estimation is weaker because the points are so far apart.

**3. Didi Chengdu / Xi'an (GAIA)**
- **Contents:** Ride-hailing trips from Oct–Nov 2016, with points every 2–4 s. It is the densest data of the three, with millions of orders. A 2018 release also exists.
- **Access:** This is the problem. I couldn't resolve `gaia.didichuxing.com`, and the older `outreach.didichuxing.com/research/opendata/en/` page returned a 404. A recent [GitHub issue](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3) says the portal now seems to offer only a synthetic dataset. A recent [MDPI paper](https://www.mdpi.com/2227-7390/14/22/4119) says the data is restricted and must be requested from DiDi for academic research. I couldn't find the application steps, so I can't tell you the process.
- **Third-party copy:** There is a [Kaggle mirror](https://www.kaggle.com/datasets/ash1971/didi-dataset/data) that a 2025 [PLOS ONE paper](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473) cites. I did not open it or verify its contents, licence or provenance. Check those before relying on it.
- **Fit:** Treat it as a possible extra, not your starting point.

## Mentioned but not verified
Search results also named CRAWDAD's SF and Rome taxi sets and Grab-Posisi (Southeast Asia). I didn't open those pages, so I can't confirm access or terms. I'd also skip the LibCity Chengdu sample (1,800 trajectories). It is too small for your scale.

## Suggested plan
Start with Porto. It has enough taxis and dense, timestamp-recoverable paths for both tasks. Add T-Drive if you want a second city or a harder sparse-data case. Only chase Didi if you need 2–4 s sampling.

Sources:
- [UCI: Porto taxi dataset](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [Kaggle: ECML/PKDD 15](https://www.kaggle.com/competitions/pkdd-15-predict-taxi-service-trajectory-i/data)
- [Figshare: Porto source/target only](https://figshare.com/articles/dataset/Porto_taxi_trajectories/12302165)
- [Microsoft Research: T-Drive](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- [T-Drive user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf)
- [Kaggle: T-Drive mirror](https://www.kaggle.com/datasets/arashnic/tdriver)
- [IEEE DataPort: T-Drive and NYC](https://ieee-dataport.org/documents/poetic-tdrive-and-nyc-database)
- [GitHub issue on Didi access](https://github.com/Zhiyang-Z/Traj-Transformer/issues/3)
- [MDPI paper on restricted Chengdu data](https://www.mdpi.com/2227-7390/14/22/4119)
- [PLOS ONE paper citing the Didi Kaggle mirror](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473)
- [Kaggle: Didi mirror](https://www.kaggle.com/datasets/ash1971/didi-dataset/data)