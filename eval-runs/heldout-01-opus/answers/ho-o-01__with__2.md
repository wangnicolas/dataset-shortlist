There are good options. You can download three of them right now: **Porto (ECML-PKDD 2015)** is the standard benchmark for both of your tasks, **iTIC Bangkok** is the largest and most recent, and **T-Drive Beijing** covers the most taxis. All of this was checked on 2026-11-12.

## What I assumed you need
- **R1 (must):** a sequence of GPS points for each trip, or a continuous stream that can be split into trips.
- **R2 (must):** at least a few hundred vehicles.
- **R3 (must):** a timestamp on every point, or a fixed sampling interval.
- **R4 (must):** an individual researcher can get it. I assumed commercial use doesn't matter. Tell me if it does, because that rules out Grab.

## Shortlist
| # | Dataset | Access | Licence | Scale | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxi (ECML-PKDD 2015) | Direct download, minutes | CC BY 4.0 | 442 taxis, 1.71M trips, 15 s sampling | Strong | today |
| 2 | iTIC Bangkok raw taxi probe data | Direct download, minutes | CC BY (from a search result) | thousands of taxis, 2017 onward | Strong | today (link) |
| 3 | T-Drive Beijing (Microsoft Research) | Direct download, minutes | none stated | 10,357 taxis, 1 week, ~3 min sampling | Partial | today |
| 4 | San Francisco cabspotting (CRAWDAD epfl/mobility) | Free IEEE account, minutes | DataPort terms, no re-identification | ~536 taxis, ~25 days | Strong | today |
| 5 | Rome taxi (CRAWDAD roma/taxi) | Free IEEE account, minutes | same | ~320 taxis, Feb 2014, ~7 s | Partial | today |
| 6 | Grab-Posisi (Singapore and Jakarta) | Email request, days | research only, no commercial use | ~84k trips, 1 s sampling | Strong | today |
| 7 | Segmented Bangkok taxi trips (Zenodo) | Direct download, minutes | CC BY 4.0 | 3 weeks, Apr 2019 | Partial | today |

## Details
1. **Porto** ([UCI](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)): each row is one finished trip, and its `POLYLINE` field holds a point every 15 s. Points have no timestamps of their own. You calculate them from the trip start time plus 15 s per point. Trips have a `MISSING_DATA` flag, and you'll see GPS outliers. The UCI page confirms CC BY 4.0. It's the same data as the Kaggle competition.
2. **iTIC Bangkok** ([archive](https://itic.longdo.com/opendata/probe-data/), [foundation page](https://iticfoundation.org/en/open-data-sharing/)): the archive is a plain directory listing that opens without a login. Each record has taxi ID, timestamp, coordinates, speed, heading and **taxi-meter status**, so you split trips on meter on/off yourself. One study counted 4,781 taxis in Sep–Dec 2021. A year of daily files is about 16 GB. The CC BY licence comes from a Longdo blog post I found in search results. I didn't find a licence statement on the archive itself, so confirm it before you publish.
3. **T-Drive** ([Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)): the page confirms "one-week trajectories of 10,357 taxis" and has a direct download link. Points are about 3 minutes apart and there's no occupied flag. That's fine for similarity work at scale but too coarse for detailed travel-time estimates. No licence is stated, so cite the T-Drive papers.
4. **San Francisco** ([IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)): the page says "Open Access dataset files are accessible to all logged in users". The file is 90.7 MB. Each point has latitude, longitude, an occupied flag and a timestamp, so trips split cleanly. The terms forbid re-identifying drivers. The taxi count and ~1 min sampling are from memory.
5. **Rome** ([IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)): same login rule, about 1.5 GB of text. Sampling is dense, but there's no occupancy flag, so you'd have to infer trips from stops.
6. **Grab-Posisi** ([Grab page](https://engineering.grab.com/grab-posisi)): the page says to email `grab.posisi@grabtaxi.com` with the details it lists, and that "You cannot use Grab-Posisi dataset for commercial purposes." It's the densest set here (1 s sampling, plus speed, bearing and accuracy). The trip count and city details are from memory.
7. **Bangkok segmented** ([Zenodo](https://zenodo.org/records/17003809)): 34 MB, already split into trips with passengers, and each point has a timestamp (GMT+7). It covers only the Songkran festival period, when traffic is unusual.

## Known, not confirmed
- **DiDi GAIA Chengdu / Xi'an (2016):** content-wise it would be ideal: ride-hailing trajectories every 2–4 s, roughly 11.75M trips in Chengdu and 6.72M in Xi'an, and many recent papers still use it. But `gaia.didichuxing.com` didn't resolve from here and the [outreach portal](https://outreach.didichuxing.com/research/opendata/en/) timed out. That may be my sandbox's network rather than the site, so try it in a browser. Free registration used to be enough. A [2025 PLOS ONE paper](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473) points to a Kaggle copy instead. That's unofficial, so DiDi's original terms still apply to it.

## Not recommended, and why
- **NYC TLC and Chicago taxi trips:** pickup and drop-off only.
- **Figshare "Porto taxi trajectories" and "San Francisco taxi trajectories" (2020):** despite the names, they keep only the start and end points.
- **GeoLife:** 182 people using mixed transport modes, not a taxi fleet.
- **Shenzhen and Harbin taxi sets seen in papers:** mostly available only by asking the authors.

## What I could not find
I found no open, recent, already-split ride-hailing dataset at Porto's scale other than the Bangkok sources. figshare and ResearchGate blocked my automated checks.

## Next step
Download Porto today; it's the standard baseline for both trajectory similarity and travel-time estimation. Add iTIC Bangkok if you want scale or recent data. Send the Grab email now, since it's the only one that needs a wait. If you want a second dense city, try the DiDi GAIA portal yourself.

Sources: [UCI Porto](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015), [MSR T-Drive](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/), [IEEE DataPort SF](https://ieee-dataport.org/open-access/crawdad-epflmobility), [IEEE DataPort Rome](https://ieee-dataport.org/open-access/crawdad-romataxi), [Grab-Posisi](https://engineering.grab.com/grab-posisi), [iTIC open data](https://iticfoundation.org/en/open-data-sharing/), [Longdo blog on licence](https://map-blog.longdo.com/thailand-its-open-data/), [Bangkok metro study (Nature)](https://www.nature.com/articles/s44333-024-00020-6), [Zenodo Bangkok](https://zenodo.org/records/17003809), [PLOS ONE on DiDi](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331473), [industry-datasets list](https://github.com/rawatpranjal/industry-datasets)

The interactive shortlist, where you can filter datasets and export an access plan, is at `/private/tmp/e-jxVaXU/home/cwd/dataset-shortlist.html`.