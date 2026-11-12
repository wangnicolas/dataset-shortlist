Four datasets fit what you described, and three of them you can download today. Each has full timestamped point sequences from at least several hundred vehicles. I checked them on 2026-11-12, and the sources are noted per dataset.

## What I assumed you need
- **R1 (must):** timestamped GPS point sequences along each trip, not just pickup and drop-off.
- **R2 (must):** at least a few hundred vehicles, in any city.
- **R3 (must):** usable for trajectory similarity and travel-time estimation. That means a fixed trip start and end, or enough points to cut trips yourself.
- **R4 (nice):** downloadable now, with a licence that allows research use.

## Shortlist

| # | Dataset | Access | Licence | Size | Checked |
|---|---|---|---|---|---|
| 1 | Porto taxi trajectories (ECML/PKDD 2015) | Direct download, no account stated | CC BY 4.0 | 442 taxis, 1.71M trips, one point every 15 s | Today, UCI page |
| 2 | T-Drive, Beijing | Download from a Microsoft Research page (hosted on OneDrive) | None stated; citation requested | 10,357 taxis, about 15M points, one week in Feb 2008, about 177 s between points | Today |
| 3 | Rome taxi (CRAWDAD roma/taxi) | Free IEEE DataPort account | CC BY 4.0 | About 320 taxis, 30 days, about 374 MB compressed | Today, partly |
| 4 | Didi GAIA, Chengdu and Xi'an | Registration or application to Didi | Didi terms of use | Chengdu has about 1.1M drivers, Nov 2016 | Partly, from search results |

## Details

**1. Porto.** This is the safest start. Each trip is one row with a `POLYLINE` of `[lon, lat]` pairs and a `TIMESTAMP`. The sampling is regular at 15 s, so each point's time is trip start plus 15 s times its index. Trip start and end are explicit.
- **Access:** download `train.csv.zip` (about 509 MB) from the [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015), or run `pip install ucimlrepo` and call `fetch_ucirepo(id=339)`. The page shows only an optional login link.
- **Mirrors:** there are copies on [Hugging Face](https://huggingface.co/datasets/Davidham3/Porto_Taxi_Trajectory) (Apache-2.0, ungated) and [figshare](https://doi.org/10.6084/m9.figshare.12302165.v1) (CC BY 4.0). The UCI copy is the original, so use that one.
- **Caveats:** `MISSING_DATA` flags gaps in some trips. The data has trip-level timestamps and fixed 15 s spacing rather than per-point times.
- **Use:** it is the standard benchmark for travel-time and destination prediction, and I recall (not checked today) that it is common in trajectory-similarity papers.

**2. T-Drive.**
- **Contents:** one text file per taxi, with lines of `taxi_id, datetime, lon, lat`.
- **Access:** the [Microsoft Research page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/) has a "Download the Trajectory Data" link. The page states no registration and no licence, only a request to cite the KDD '11 and GIS '10 papers. The [user guide](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/User_guide_T-drive.pdf) may say more, and I didn't read it.
- **Caveats:** there are no trip boundaries, so you have to split trips yourself. The long gaps between points (about 177 s) are poor for fine-grained similarity. That is also why it is a good test of sparse-trajectory methods.
- **Copies to avoid:** some secondary descriptions of this dataset (6 months, 30,000 taxis) don't match Microsoft's own description. The [TIB record](https://doi.org/10.57702/enayhf6y) returned a 404. The [IEEE DataPort "POETIC – Tdrive and nyc"](https://doi.org/10.21227/rgbn-cw81) copy needs a subscription.

**3. Rome.** Lines look like `DRIVER_ID;TIMESTAMP;POINT(lat lon)`, sorted by time. The data was originally on CRAWDAD and is now on [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi). The page says open access but also that a logged-in account is needed, and one line mentions a "subscription". A free IEEE account is probably enough, but confirm this when you download.
- **Caveats:** there are no trip IDs, so you have to segment trips. The sampling interval is inconsistent between sources (the page says 7 s, another source says 15 s). Check this against the data.

**4. Didi GAIA (Chengdu and Xi'an, Oct/Nov 2016).** This is the largest source and the closest to ride-hailing. Records have driver ID, order ID, timestamp, lon and lat. It is the only one here that is ride-hailing rather than taxi data.
- **Access:** the portal is [outreach.didichuxing.com/research/opendata/en](https://outreach.didichuxing.com/research/opendata/en/). My fetch returned HTTP 501, so I could not read the form.
- **What I found:** a PLOS ONE paper says you can access it after free registration. A 2026 MDPI paper says it is available from Didi for academic research under their terms, and that derived data can only be shared with Didi's permission.
- **Before you plan around it:** confirm today whether the portal is still accepting requests, how long approval takes, and whether the terms restrict redistribution.

## Known, not confirmed
- **San Francisco Cabspotting.** I recall about 500 taxis with timestamped GPS from the original CRAWDAD epfl/mobility trace. There is a [figshare copy](https://doi.org/10.6084/m9.figshare.12302243.v1) with a CC BY 4.0 record, but I couldn't open the landing page. Its terms may differ from the original's, so check them before relying on it.
- **Shenzhen and Shanghai taxi datasets** (for example [Pingshan, Shenzhen](https://doi.org/10.13140/rg.2.2.20676.80007), [Shanghai taxi demand/flow](https://doi.org/10.6084/m9.figshare.31481464.v2)). The DOIs are real but both landing pages blocked me. The Shanghai one may be aggregated flows rather than raw points. The Pingshan one covers a single day. I haven't checked either one's size or fit.
- **Bangkok taxi trajectories on Zenodo** ([tourist trajectories](https://zenodo.org/records/17005200) and [segmented trips](https://zenodo.org/records/17003809)). Both are open under CC BY 4.0 (confirmed). They look like derived subsets, and I didn't check the vehicle count.

## Not recommended
- **IEEE DataPort "Taxi trajectories"** ([10.21227/rxw4-1r28](https://doi.org/10.21227/rxw4-1r28)): it needs a paid subscription, and the file names look like NYC 2015 taxi data, which is pickup and drop-off only.
- **NYC TLC trip records:** pickup and drop-off only.
- **GeoLife:** about 180 users, not taxis.
- **The [NYC telematics Zenodo record](https://zenodo.org/records/6647220):** I verified that it exists but not its contents, so I left it out.

## What I could not find
- **Several searches returned nothing relevant.** The "ride-hailing GPS" query returned nothing useful from DataCite, OpenAIRE and Zenodo.
- **Pages I couldn't open.** Didi's portal gave a server error, and the original CRAWDAD page returned 404. Neither Didi's current terms nor T-Drive's user-guide terms were read.
- **No evidence-of-use check.** I did not run the step that finds papers using each dataset. The literature search returned only generic surveys, so I can't point you to similarity or ETA baselines from this session.
- **No HTML shortlist page.** I skipped it because this reply covers the same content.

## Next step
1. Start with Porto, since it is clean and open and has a known benchmark setup.
2. Add Rome or T-Drive for a second city with a different sampling rate.
3. Apply to Didi now if you want ride-hailing data, because approval may take time.