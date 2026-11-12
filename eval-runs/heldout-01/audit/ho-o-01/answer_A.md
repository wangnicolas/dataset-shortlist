I'm answering from memory and haven't checked the links or access terms this session. Check each landing page before you build on it, since hosting and access rules change.

| Dataset | City / scale | Sampling | What you do to get it |
|---|---|---|---|
| **Porto (ECML/PKDD 2015)** | Porto; 442 taxis, about 1.7M trips, Jul 2013–Jun 2014 | One point every 15 s, stored per trip | Download it from the UCI ML Repository with no signup. It's also on Kaggle, where you need a free account and have to accept the competition rules. |
| **T-Drive (Microsoft Research)** | Beijing; 10,357 taxis, about 15M points, one week in Feb 2008 | Irregular, about 3 min on average | Download it from the Microsoft Research page. It's a free direct download, and the page asks you to cite the T-Drive papers. |
| **DiDi GAIA Open Data** | Chengdu and Xi'an, Oct–Nov 2016; Haikou has also been listed | About 2–4 s | Apply on the DiDi Gaia research portal with an institutional affiliation and a stated research purpose. Approval is manual and usually restricted to non-commercial use. Access has been inconsistent over time. |
| **San Francisco Cabspotting (CRAWDAD `epfl/mobility`)** | San Francisco; about 536 taxis, about 30 days in May 2008 | About 1 min | Register with CRAWDAD and accept its license. The archive has moved hosts over the years, so look for the current location. It includes an occupancy flag. |
| **Rome taxi (CRAWDAD `roma/taxi`)** | Rome; about 320 taxis, 30 days in Feb 2014 | A few seconds to tens of seconds | Same CRAWDAD registration and license as above. |
| **Grab-Posisi** | Southeast Asia (Singapore, Jakarta) | Varies | It was released for a Grab research challenge. I'm not sure it's still available, so check before planning around it. |

NYC TLC and Chicago taxi data are the well-known ones, but they only have pickup and drop-off, so they don't fit your needs.

**Which to use**
- **Travel-time estimation:** Porto. Trips are already segmented, so you get a ground-truth duration (points × 15 s) and a start timestamp, taxi ID, and day type. It's the standard benchmark for this task.
- **Trajectory similarity:** Porto and T-Drive are both common. T-Drive's sparse, irregular sampling makes it a good robustness test. DiDi Chengdu/Xi'an is the dense option if you get approved.

**Caveats**
- **Porto:** The timestamp field is only the trip start. You reconstruct per-point times from the 15 s interval, and some trips have missing points or are very short.
- **T-Drive:** Each file is one taxi's continuous stream, with no trip boundaries or occupancy flag. You have to segment trips yourself, for example by time gaps.
- **CRAWDAD:** Its licenses generally bar redistributing the data, so you can't republish it.

I can pull the current download pages and confirm the access steps and licenses if you want.