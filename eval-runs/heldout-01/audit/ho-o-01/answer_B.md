
## What I assumed you need
- **R1 (must):** timestamped GPS points along each trip or vehicle track, not just pickup and drop-off.
- **R2 (must):** at least a few hundred vehicles, taxi or ride-hailing, any city.
- **R3 (must):** enough points per trip for trajectory similarity and for travel-time labels. Travel time can come from the first and last timestamp of a trip.
- **R4 (nice):** per-trip segmentation, an occupancy flag and a sampling interval of about 15 s or finer.
- **R5 (nice):** a licence that allows publishing results.

I assumed academic use, so I didn't weigh commercial-use clauses heavily.

## Shortlist
| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | Porto taxis (ECML/PKDD 2015) | Direct download, no login | CC BY 4.0 | 442 taxis, 1.71M trips, 1 year | Strong. Trips are already segmented; points every 15 s. | Today (UCI page) |
| 2 | San Francisco cabs (CRAWDAD epfl/mobility) | Free IEEE DataPort login | CC BY 4.0 | ~500 cabs, 30 days, 91 MB | Strong. Points about 10 s apart with an occupied flag, but not split into trips. | Today (IEEE DataPort) |
| 3 | T-Drive (Beijing) | Direct download via OneDrive, no registration | None stated; asks you to cite two papers | 10,357 taxis, 1 week, ~15M points | Good for scale. Sampling is coarse (about 177 s) and tracks aren't split into trips. | Today (Microsoft page) |
| 4 | Grab-Posisi (Singapore, Jakarta) | Email request, research only | No licence named; no commercial use | ~84K trajectories, >80M pings, ~2 GB | Strong. 1 s sampling. Vehicle count isn't stated on the page, so check R2. | Today (Grab page) |
| 5 | Rome taxis (CRAWDAD roma/taxi) | IEEE DataPort subscription | Not confirmed | ~320 taxis, 30 days | Good. Points every 15 s, but not segmented into trips. | Search results only |

## Details
**1. Porto: [UCI page](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)**
- **Contents:** each row is one trip. `POLYLINE` is a list of `[lon, lat]` pairs, one per 15 s. Other fields are `TAXI_ID`, `TIMESTAMP` (trip start) and call type. Per-point times are start time plus 15 s × index.
- **Steps:** click "Download (509.3 MB)" on the UCI page, or run `fetch_ucirepo(id=339)` from the `ucimlrepo` package.
- **Licence:** CC BY 4.0, so attribution only.
- **Use:** Brébisson et al. won the challenge's destination-prediction task ([arXiv 1508.00021](https://arxiv.org/pdf/1508.00021)). I didn't search for similarity or travel-time papers that use it.
- **Caveat:** the timestamps are regular by construction, so they carry no information of their own. Some trips have missing GPS segments; check this before using trip length as a label.

**2. San Francisco: [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-epflmobility)**
- **Contents:** one file per cab, each line `lat, lon, occupied, unix_time`. The occupied flag lets you cut each track into trips. Cab IDs are scrambled.
- **Steps:** create a free IEEE account, log in and download `cabspottingdata.tar.gz`. The page says both "Open Access" and "requires a DataPort subscription." My reading is that the free tier is enough, but I haven't tried the download.
- **Licence:** CC BY 4.0.
- **Caveat:** the old CRAWDAD address (crawdad.org/epfl/mobility/20090224/) now returns 404, so use the IEEE DataPort page. A figshare copy ([San Francisco taxi trajectories](https://doi.org/10.6084/m9.figshare.12302243.v1)) is listed as CC BY 4.0. I haven't checked what's different in it.

**3. T-Drive: [Microsoft Research](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)**
- **Contents:** one file per taxi, each line `taxi_id, datetime, lon, lat`, covering 2–8 Feb 2008. The average gap is about 177 s (~623 m).
- **Steps:** click "Download the Trajectory Data" (OneDrive). Cite Yuan et al. (KDD '11 and GIS '10).
- **Licence:** none stated on the page. Treat it as research use with citation. I couldn't tell whether Microsoft's generic site terms apply.
- **Caveat:** a 3-minute gap is too coarse for precise route similarity unless you map-match. The data suits large-scale similarity benchmarks. Trips aren't segmented, so you would need a stay-point heuristic.

**4. Grab-Posisi: [Grab Engineering](https://engineering.grab.com/grab-posisi)**
- **Contents:** one Parquet file per trajectory with latitude, longitude, UTC timestamp, accuracy, bearing and speed at 1 s. It was collected in April 2019 from ride-hailing drivers' phones, with an Android or iOS label.
- **Steps:** email grab.posisi@grabtaxi.com with your name and contact details, your institution and your intended use. I don't have a typical turnaround; plan for days to weeks.
- **Licence:** research only, and you must cite Huang et al. 2019 ([DOI 10.1145/3356995.3364536](https://dl.acm.org/doi/pdf/10.1145/3356995.3364536)). A published paper counts as research use.
- **Caveat:** the page doesn't say how many distinct drivers contributed. If you need a few hundred vehicles, ask when you email. A companion set, Grab-Posisi-L, has map-matched ground truth for 2,937 trajectories.

**5. Rome: [IEEE DataPort](https://ieee-dataport.org/open-access/crawdad-romataxi)**
- **Contents:** about 320 taxis, 1 Feb–2 Mar 2014, one point every 15 s. A user reports a 1.6 GB file of 21.8M lines. Details come from a search summary; I did not open the page.
- **Steps:** per the search summary, you need an IEEE DataPort subscription, which is free with an IEEE society membership. I did not confirm whether a plain free account is enough.
- **Licence:** not confirmed. The CRAWDAD version is cited as doi:10.15783/C7QC7M.

## Known, not confirmed
- **DiDi GAIA (Chengdu and Xi'an):** this is the best-known ride-hailing set, with driver tracks at 2–4 s sampling, order IDs, and a 2016 and an alternate 2018 release. The portal ([outreach.didichuxing.com/research/opendata/en/](https://outreach.didichuxing.com/research/opendata/en/)) returned HTTP 501 to my checker. From memory and search summaries, access is by registration and an application stating your research plan, with credit to DiDi in publications. A paper citing the portal in January 2026 suggests it was still up, but I found nothing on whether applications are currently open. Open the portal in a browser. If it's closed, use Porto and Grab-Posisi instead.
- **Bangkok taxi trajectories ([Zenodo](https://zenodo.org/records/17003809)):** open, CC BY 4.0, 4–24 Apr 2019, but only 33.5 MB. The page doesn't give the number of taxis, and sampling is 1–3 minutes. Check the vehicle count before relying on it.
- **Other possible sources:** Shanghai SUVnet and several Shenzhen or Shanghai files on figshare. I haven't verified their access or contents.

## Not recommended
- **[NYC telematics (Zenodo 6647220)](https://zenodo.org/records/6647220):** 16 files, about 25 MB, from a single session, with no vehicle count given. It is not a fleet.
- **GeoLife:** I didn't search for it. From memory it holds individual people's tracks rather than taxis, so it doesn't meet R2.
- **Hugging Face trajectory hits:** the HF hits ("Porto_Taxi_Trajectory", "porto_taxi") are third-party copies. Use UCI for Porto.

## What I could not find
- A trip-segmented, high-frequency (≤5 s) taxi set from several hundred vehicles with no application required. Grab-Posisi is the closest but needs an email request. DiDi would also fit but is unconfirmed.
- I didn't search for papers on how each dataset is used for similarity or travel time, beyond the Porto one above. [T-JEPA (arXiv 2406.12913)](https://arxiv.org/pdf/2406.12913) came up in the T-Drive search, but I didn't open it to see which datasets it uses.

## Next step
Download Porto first. It is the only one that is fully open, already split into trips, and large enough. Use it to build and test your similarity and travel-time code. In parallel, email Grab for Grab-Posisi, since it has 1 s sampling and per-trip files, and register for IEEE DataPort to get San Francisco. Open the DiDi portal in a browser to see whether applications are open. Add T-Drive if you need a very large fleet and can accept the 3-minute sampling.

Sources:
- [UCI Porto](https://archive.ics.uci.edu/dataset/339/taxi+service+trajectory+prediction+challenge+ecml+pkdd+2015)
- [T-Drive](https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/)
- [Grab-Posisi](https://engineering.grab.com/grab-posisi)
- [CRAWDAD epfl/mobility](https://ieee-dataport.org/open-access/crawdad-epflmobility)
- [CRAWDAD roma/taxi](https://ieee-dataport.org/open-access/crawdad-romataxi)
- [Zenodo Bangkok](https://zenodo.org/records/17003809)
- [Zenodo NYC telematics](https://zenodo.org/records/6647220)
- [DiDi GAIA portal](https://outreach.didichuxing.com/research/opendata/en/)