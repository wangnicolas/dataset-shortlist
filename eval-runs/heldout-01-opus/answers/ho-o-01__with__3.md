Yes. There are three good taxi datasets you can download today, and a fourth (ride-hailing, sampled every second) that you get by sending an email. I checked all of these on 12 Nov 2026 unless a row says otherwise.

## What I assumed you need
- **R1 (must have):** GPS points with timestamps along each trip, not just the pickup and drop-off.
- **R2 (must have):** at least a few hundred vehicles.
- **R3 (must have):** taxis or ride-hailing cars, with trips already marked or possible to work out.
- **R4 (nice to have):** you can get it quickly. Any city and any year is fine. I didn't assume you need commercial use.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxi (ECML/PKDD 2015) | Direct download, minutes | CC BY 4.0 | 442 taxis, 1.71M trips, a point every 15 s | Strong | today |
| 2 | San Francisco Cabspotting (CRAWDAD epfl/mobility) | Free IEEE account, minutes | CC BY 4.0 | ~500 cabs, 30 days, a point every <10 s on average | Strong | today |
| 3 | Rome taxi (CRAWDAD roma/taxi) | Free IEEE account, minutes | CC BY 4.0 | ~320 taxis, 30 days, a point every 7 s | Partial | today |
| 4 | T-Drive, Beijing | Direct download, minutes | No licence stated; they ask you to cite them | 10,357 taxis, 1 week, ~15M points | Partial | today |
| 5 | Grab-Posisi, Singapore and Jakarta | Email request, likely days | Non-commercial only | ~84K trips, 80M+ points, a point every 1 s | Strong | today |
| 6 | DiDi GAIA, Chengdu and Xi'an | Registration, if the portal still works | Non-commercial (from memory) | Tens of thousands of drivers, a point every 2–4 s | Strong, if you can get it | **portal down today** |
| 7 | Bangkok segmented taxi trips (Zenodo) | Direct download | CC BY 4.0 | Apr 2019, a point every 1 min | Weak | today |

## Details

**1. Porto.** [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- **What's in it:** one row per completed trip. The `POLYLINE` column is the list of [lon, lat] points, "one pair of coordinates for each 15 seconds of trip". Only the trip's start `TIMESTAMP` is stored, so each point's time is the start time plus 15 s for each step.
- **Why it fits:** it is the most widely used benchmark for both of your tasks. My memory says it covers July 2013 to June 2014; I didn't confirm that.
- **How to get it:** download `train.csv.zip` (509 MB). No account needed.
- **Watch out for:** drop rows where `MISSING_DATA` is true, and remove GPS outliers. There are copies on Hugging Face and figshare, but the UCI page is the original source.

**2. San Francisco Cabspotting.** [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- **What's in it:** one file per cab, May–June 2008. Each line is lat, lon, an occupied flag (0 or 1), and a UNIX timestamp. The flag changing from 0 to 1 and back gives you each passenger trip.
- **How to get it:** create a free IEEE account, log in, and download `cabspottingdata.tar.gz` (91 MB). The page says the files are "accessible to all logged in users". It also mentions a "DataPort Subscription", but the open-access files only need a login.
- **Terms:** you may not try to identify the drivers or passengers.

**3. Rome.** [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)
- **What's in it:** each record is `DRIVER_ID;TIMESTAMP;POINT(lat lon)`, for February 2014. Points less precise than 20 m were removed.
- **Catch:** there is no occupied flag, so you have to split whole shifts into trips yourself, for example at stops or gaps. With ~320 taxis it only just meets your minimum.
- **How to get it:** same login as #2. The download is 374 MB, or 1.5 GB unpacked.

**4. T-Drive.** [MSR page](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- **What's in it:** a very large fleet, but points are far apart. From memory, the gap averages about 3 minutes and ~600 m, which is weak for travel-time estimation along road segments.
- **Catch:** there is no trip ID and no occupied flag.
- **How to get it:** the page links a direct OneDrive download and a user-guide PDF. It states no licence and asks you to cite Yuan et al., KDD 2011 and GIS 2010.

**5. Grab-Posisi.** [Grab blog page](https://engineering.grab.com/grab-posisi)
- **What's in it:** one point per second, with lat, lon, UTC timestamp, accuracy, bearing and speed. Each trip is labelled with phone type and whether it was a car or a motorcycle. About 2 GB of Parquet files, from April 2019.
- **Catches:** the real start and end locations were removed. The page doesn't say how many drivers there are, though with 84K trips it is almost certainly more than a few hundred.
- **How to get it:** email grab.posisi@grabtaxi.com with your name and contact details, your institution, and what you will use it for. The page says: "You cannot use Grab-Posisi dataset for commercial purposes." Cite Huang et al., 2019 (SIGSPATIAL PredictGIS).

## Known, not confirmed
- **DiDi GAIA (Chengdu and Xi'an).** This is ride-hailing data, Oct–Nov 2016 plus 2018 releases, with driver and order IDs and points every 2–4 s, already matched to roads. It is widely used in travel-time papers ([PLOS ONE 2019](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0215656), [TrajCogn 2024](https://arxiv.org/pdf/2405.12459)).
  - What happened today: outreach.didichuxing.com refused the connection, so I couldn't tell whether the portal still exists or accepts new users.
  - How access used to work: free registration where you state your purpose. From memory, the terms were non-commercial with no redistribution.
  - A [Kaggle copy](https://www.kaggle.com/datasets/ash1971/didi-dataset/data) exists, but it is unofficial, and a re-upload doesn't change DiDi's terms. Try the portal from your own network first.
- **Raw ITIC Bangkok taxi GPS** ([iticfoundation.org](https://org.iticfoundation.org/)). This is the source behind #7 and is probably much larger, but I didn't check how you get it.
- **Shenzhen Pingshan one-day taxi GPS (2019).** It is listed on ResearchGate, which blocked my check, so I don't know its size or terms.

## Not recommended, and why
- **NYC TLC and Chicago taxi trips:** pickup and drop-off only (from memory).
- **GeoLife:** 182 people using all kinds of transport, not taxis.
- **kraina/porto_taxi on Hugging Face:** Porto squashed into hexagonal grid cells; use the UCI original.

## What I could not find
- No dataset is open, has hundreds of cars, a point every second, and a permissive licence all at once. The only one sampled every second is Grab, which is request-only and non-commercial.
- My literature searches mostly returned off-topic papers. So the evidence that these datasets are used comes from what I know of the field, not from papers I looked up today.

## Next step
Start today with **Porto** (download) and **San Francisco** (free login). They are the usual pair in trajectory-similarity work, and the occupied flag in San Francisco gives you clean trip boundaries. Send the Grab email now so it arrives while you're working; it adds the dense, ride-hailing data that the other two lack.

The shortlist page, where you can filter and compare these, is at `/private/tmp/e-Rqbkfy/home/cwd/dataset-shortlist.html`.