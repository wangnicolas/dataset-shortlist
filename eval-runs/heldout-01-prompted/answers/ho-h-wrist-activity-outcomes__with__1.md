You have four datasets worth applying to. UK Biobank is the best fit. NHANES is the quickest to start with. Whitehall II is a smaller wrist-based option with hospital-record linkage. All of Us is the only one that comes with caveats about wrist placement. I checked each by search. The UK Biobank and NSRR (National Sleep Research Resource) pages themselves wouldn't load for me, so some details come from secondary sources, and I flag those below.

## Main candidates

**1. UK Biobank** (wrist, about 100,000 people, hospital and death linkage)
- **Device:** Axivity AX3 worn on the dominant wrist for 7 days at 100 Hz. About 103,700 participants returned data between 2013 and 2015. The raw data are field 90001, and the wear-time and calibration QC fields are listed in the official accelerometer documentation. ([Doherty 2017](https://biobank.ndph.ox.ac.uk/showcase/ukb/docs/acc_plos_0169649.pdf), [UKB protocol PDF](https://biobank.ndph.ox.ac.uk/ukb/ukb/docs/PhysicalActivityMonitor.pdf))
- **Outcomes:** Published work uses it for incident disease and mortality ([npj Digital Medicine](https://www.nature.com/articles/s41746-022-00676-9)). I didn't separately confirm the hospital and death linkage details, but this is how it is normally used.
- **Access:**
  - Register, then submit an application. Your institution must sign a contract (a Material Transfer Agreement), and international applicants are accepted. Once approved, you have 90 days to pay and sign.
  - Data are accessed only through the cloud Research Analysis Platform. Compute is billed separately, with a small starting credit.
  - Reported fees are £3,000 for Tier 1 and £9,000 for Tier 3 (3 years), excluding VAT, payable in GBP. Students anywhere can get access for £500. ([Fees](https://www.ukbiobank.ac.uk/use-our-data/fees/), [FAQ](https://community.ukbiobank.ac.uk/hc/en-gb/articles/28002689502237-Applying-to-UK-Biobank-and-accessing-data-FAQ))
  - UK Biobank's FAQ gives an average of about 15 weeks from submission to data release.
- **Check first:** One secondary source says new applications were paused in mid-2026 during a platform upgrade. I couldn't confirm this on UK Biobank's own pages, so verify before you plan around it.

**2. NHANES 2011–2014** (wrist, US-representative, mortality only)
- **Device:** ActiGraph GT3X+ worn on the wrist for up to 9 days, for ages 6 and up, released in 2020. The data are in MIMS units, so comparability with other brands depends on harmonization.
- **Outcomes:** NCHS public-use linked mortality files give vital status, cause of death and follow-up through 31 Dec 2019. A published analysis of ages 50–80 had 3,653 participants and 416 deaths. ([MSSE paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/), [NCHS linkage](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm))
- **Access:** Both datasets are free to download with no application. The public file covers death only, with no hospital records.

**3. Whitehall II accelerometer sub-study** (wrist, about 4,000 people, mortality and hospital linkage)
- **Device:** GENEActiv on the non-dominant wrist, 9 days, in 2012–13. About 4,000 participants had valid data.
- **Outcomes:** Linked to mortality (about 8 years of follow-up) and to Hospital Episode Statistics. It has also been used for cardiovascular disease incidence. ([Sci Rep 2025](https://www.nature.com/articles/s41598-025-30237-5))
- **Access:** By application through UCL's Whitehall II data-sharing page. It isn't public because of ethics restrictions. The UCL URLs have moved over time, so use the [current page](https://www.ucl.ac.uk/epidemiology-health-care/research/epidemiology-and-public-health/research/whitehall-ii/data-sharing). I didn't find the fee or timeline.
- **Why it's useful:** The cohort is small enough to replicate UK Biobank findings against.

## Use with caveats

**4. All of Us (Fitbit)**
- **Data:** About 59,000 participants with Fitbit data, linked to electronic health records. ([Nature Medicine 2026](https://www.nature.com/articles/s41591-026-04352-3))
- **Wrist placement:** I found no source documenting it, and device model isn't available in the Workbench. That undercuts your comparability goal. Treat it as consumer-tracker data, not research-grade wrist accelerometry.
- **Outcomes:** Death comes from health records and participant status reports, not a national death registry. In the Registered Tier the death dates are shifted and cause is suppressed. ([death data](https://support.researchallofus.org/hc/en-us/articles/10237876482196-How-to-find-participant-death-reports))
- **Access:** Your institution needs a signed Data Use and Registration Agreement. Individual researchers then register, complete ethics training and attest to the data use agreement. Analysis happens in the cloud Workbench, with no downloads. Recent Fitbit papers used the Controlled Tier. ([overview](https://casrai.org/guides/all-of-us-researcher-workbench-tiered-access))

**5. MrOS Sleep Study and Study of Osteoporotic Fractures (SOF)**
- **MrOS:** Older US men, about 3,000 with 3–5 days of wrist actigraphy (Sleepwatch-O), and published mortality analyses exist. ([Paudel](https://pubmed.ncbi.nlm.nih.gov/20370475)) However, the NSRR page states that no actigraphy is included. The actigraphy has to be requested from the MrOS Sleep Study investigators. ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0285703)) NSRR itself uses a request form with a data use agreement and IRB documentation. ([NSRR MrOS](https://sleepdata.org/datasets/mros))
- **SOF:** Older women with wrist actigraphy (at least three 24-hour periods) and mortality follow-up. NSRR lists it with a request button. ([circadian rhythm paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC2938873/), [NSRR SOF](https://sleepdata.org/datasets/sof)) I didn't confirm the sample size or exactly what is released.
- **Limits:** Both are older-adult and single-sex samples, and the actigraphy is from the 2000s, so they are less comparable with modern wrist devices. MrOS's actigraph is single-axis.

## Not confirmed
- **Our Future Health:** My search found nothing on wearable data or access, so I can't recommend it.
- **Women's Health Initiative OPACH:** It used hip-worn ActiGraph devices, so it fails your wrist criterion.

## Suggested plan
Start with NHANES, which needs no application. Apply to UK Biobank in parallel and check its application status first. Whitehall II gives you a second wrist cohort with hospital linkage for replication. If you want, I can look into the Whitehall II and NSRR access steps next, or the NCHS restricted linkage through the Research Data Center, which would add non-fatal outcomes for NHANES. I haven't searched for that.

Sources:
- [UK Biobank accelerometer (Doherty 2017)](https://biobank.ndph.ox.ac.uk/showcase/ukb/docs/acc_plos_0169649.pdf)
- [UK Biobank Physical Activity Monitor documentation](https://biobank.ndph.ox.ac.uk/ukb/ukb/docs/PhysicalActivityMonitor.pdf)
- [npj Digital Medicine: accelerometer and incident disease](https://www.nature.com/articles/s41746-022-00676-9)
- [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)
- [UK Biobank application FAQ](https://community.ukbiobank.ac.uk/hc/en-gb/articles/28002689502237-Applying-to-UK-Biobank-and-accessing-data-FAQ)
- [NHANES and mortality, MSSE](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/)
- [NCHS public-use linked mortality](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm)
- [Whitehall II and UK Biobank, Sci Rep](https://www.nature.com/articles/s41598-025-30237-5)
- [Whitehall II data sharing](https://www.ucl.ac.uk/epidemiology-health-care/research/epidemiology-and-public-health/research/whitehall-ii/data-sharing)
- [All of Us wearables dataset](https://www.nature.com/articles/s41591-026-04352-3)
- [All of Us death data](https://support.researchallofus.org/hc/en-us/articles/10237876482196-How-to-find-participant-death-reports)
- [All of Us tiered access](https://casrai.org/guides/all-of-us-researcher-workbench-tiered-access)
- [NSRR MrOS](https://sleepdata.org/datasets/mros)
- [NSRR SOF](https://sleepdata.org/datasets/sof)
- [MrOS rest/activity and mortality](https://pubmed.ncbi.nlm.nih.gov/20370475)
- [PLOS ONE (MrOS actigraphy access)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0285703)
- [SOF circadian rhythms and mortality](https://pmc.ncbi.nlm.nih.gov/articles/PMC2938873/)