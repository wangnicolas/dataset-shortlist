I'm going from memory rather than live-checking the pages, so confirm the links, license terms and sizes before you commit to one. Hosting for older datasets (CRAWDAD especially) has moved over the years.

## Easiest to get, no approval needed

| Dataset | Scale and sampling | What you have to do |
|---|---|---|
| **Porto taxi (ECML/PKDD 2015)** | 442 taxis, about 1.7M trips, July 2013 to June 2014. One GPS point every 15 s, stored as a `POLYLINE` of lon/lat per trip. | Download it from the UCI ML Repository, which needs no login. The Kaggle copy needs a Kaggle account and acceptance of the competition rules. |
| **T-Drive (Microsoft Research, Beijing)** | 10,357 taxis, one week in Feb 2008, about 15M points. Sampling is sparse, around 3 minutes on average. | Download it from the Microsoft Research page, which is free. They ask you to cite the T-Drive papers. |

## Registration or a request required

| Dataset | Scale and sampling | What you have to do |
|---|---|---|
| **San Francisco "epfl/mobility" (Cabspotting)** | 536 taxis, about 30 days in May 2008. Points arrive roughly every minute, with an **occupancy flag**. | It's hosted via CRAWDAD. Create an account, accept the data-use terms, and download. Check whether it has moved to IEEE DataPort. |
| **Rome taxi (CRAWDAD `roma/taxi`)** | 320 taxis, 30 days in Feb 2014, about 7 s sampling. | Same CRAWDAD process as above. |
| **Didi GAIA Open Data (Chengdu and Xi'an)** | Ride-hailing cars, Oct to Nov 2016. Sampling is about 2 to 4 s, so very dense. | Apply on the GAIA site with your institution and project description. Approval is manual, and you agree not to redistribute. Availability has been inconsistent, so check it's currently accepting applications. |
| **Shanghai taxi (SUVnet)** | Several thousand taxis. | Email the SJTU group that maintains it and state your academic purpose. Response times vary. |

## Which to use

- **Trajectory similarity:** Porto and T-Drive are the standard benchmarks, so your results will be comparable with published work.
- **Travel-time estimation:** Porto is the practical choice. Trip duration is (number of points − 1) × 15 s, and trips are already segmented. Didi is better if you can get it, because its dense sampling supports finer-grained road-level work.

## Caveats

- **Porto:** some trips have `MISSING_DATA=True`, and others have GPS jumps. Filter these first. It has no map-matching, so you'll need OSM plus something like Valhalla or FMM if you want road segments.
- **T-Drive:** it's continuous per-taxi logs with no trip boundaries or occupancy flag. You'd have to segment trips yourself. The sampling is also too sparse for fine-grained similarity.
- **San Francisco:** the occupancy flag lets you split trips cleanly, but the sampling is coarse.

**Skip** NYC TLC, Chicago and Uber Movement. They only have pickup/drop-off or aggregated speeds, not point sequences. GeoLife has real trajectories but comes from 182 people, mostly walking and transit, not taxis.

Porto alone meets your "few hundred vehicles" bar, so I'd start there. Add T-Drive or Didi for cross-city generalization. I can write a loader and cleaning script for Porto if that would help.