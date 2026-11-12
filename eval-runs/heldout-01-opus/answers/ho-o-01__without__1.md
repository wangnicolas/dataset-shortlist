Here are the ones that fit: real timestamped GPS sequences, hundreds of vehicles or more, and free for research. I wrote this from memory and didn't check the sites today. Hosting and access terms change, especially for the Chinese and industry releases, so confirm each one before you plan around it.

## Best fits

**1. Porto Taxi (ECML/PKDD 2015 challenge)**
- **What:** 442 taxis in Porto, Portugal, Jul 2013 to Jun 2014. About 1.7M trips, each a `POLYLINE` of points sampled every 15 s.
- **Why it's good:** It's already split into trips, so you don't have to work out where trips start and end. It's the most common benchmark for both trajectory similarity (t2vec, NeuTraj, TrjSR and others) and travel-time estimation.
- **Watch out for:** No per-point timestamps. You get the trip start time plus a fixed 15 s interval. There's a `MISSING_DATA` flag, and some GPS jumps need cleaning.
- **How to get it:** Download it directly from the UCI ML Repository ("Taxi Service Trajectory – Prediction Challenge, ECML PKDD 2015", CC BY 4.0). It's also on Kaggle ("PKDD 15 Taxi Trajectory Prediction"), where you need an account and have to accept the competition rules.

**2. Didi GAIA: Chengdu and Xi'an**
- **What:** Didi ride-hailing cars, Oct–Nov 2016, sampled every 2–4 s. Points are linked to order IDs, so trips are already separated. There are many thousands of drivers.
- **Why it's good:** It's dense and high quality, and it's the standard TTE benchmark (DeepTTE and later work) alongside Porto.
- **How to get it:** It came out through Didi's GAIA Open Dataset Initiative. You had to register and apply with an institutional or academic affiliation and agree to research-only, no-redistribution terms. The portal has been unreliable or closed to new applicants for stretches, so check whether it's open now. Copies circulate on GitHub and Baidu Pan, but using them breaks the license, so avoid them if you plan to publish.

**3. Grab-Posisi (Singapore and Jakarta, 2019)**
- **What:** About 84k Grab ride-hailing trips sampled at about 1 s, with speed, bearing and accuracy fields. Singapore is cars only. Jakarta mixes cars and motorbikes, so filter by vehicle type.
- **Why it's good:** It's the densest sampling here, it covers Southeast Asian cities, and trips are already separated.
- **How to get it:** Request it through Grab's form (linked from the Grab-Posisi paper, Huang et al. 2019) and agree to research-use terms. It's free, but approval is manual.

**4. T-Drive (Microsoft Research, Beijing)**
- **What:** 10,357 taxis, Feb 2–8 2008, about 15M points.
- **Watch out for:** It's sparse, with one point roughly every 3 minutes (about 600 m). There's no occupancy flag, so you have to split trips yourself using stop and gap heuristics. It's fine for similarity work at scale but weak for TTE.
- **How to get it:** Free direct download from Microsoft Research's T-Drive page. No registration.

**5. San Francisco Cabspotting (EPFL, via CRAWDAD)**
- **What:** About 536 taxis, May–Jun 2008, a point roughly every minute, with an occupancy flag. Occupied stretches give you trips.
- **How to get it:** CRAWDAD moved to IEEE DataPort ("epfl/mobility"). You need a free IEEE account. CRAWDAD datasets are free to download, though DataPort may ask you to log in or accept terms.

## Borderline

- **Rome taxi (CRAWDAD "roma/taxi"):** About 320 taxis, Feb 2014, a point roughly every 7 s. That's just under your vehicle count, and there's no occupancy flag. Available on IEEE DataPort the same way as Cabspotting.
- **Shenzhen and Shanghai taxi sets:** These show up in papers, but there's no stable official download. They're usually shared by authors on request.

## Ones to skip

- **NYC TLC and Chicago taxi data:** Pickup and drop-off only.
- **GeoLife:** Only about 180 people, using mixed transport modes, not taxis.

## My recommendation

Start with **Porto**: it's open, already split into trips, and widely benchmarked, so you can compare against published results right away. Add **Chengdu/Xi'an** if you can get GAIA access, because the TTE literature compares on those. Use **Grab-Posisi** if you want dense sampling or a city outside Europe and China. Use **T-Drive** only for large-scale similarity experiments where sparse sampling is acceptable.

I can check current access status and links for any of these on the web, or write a loader that turns Porto's `POLYLINE` into timestamped point sequences.