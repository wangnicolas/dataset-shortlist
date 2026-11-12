## Datasets to consider

Several datasets fit your criteria: thousands of adults, wrist-worn devices, multi-day wear and linked outcomes. Quick summary:

| Dataset | Device / placement | N with wrist data | Wear | Outcomes | Cost / difficulty of access |
|---|---|---|---|---|---|
| **UK Biobank** | Axivity AX3, dominant wrist, raw 100 Hz | ~100,000 (2013–15) | 7 days, 24 h | Hospital records (HES), death, cancer registries, partial primary care. About 10 years of follow-up | Paid application, moderate effort |
| **NHANES 2011–2014** | ActiGraph GT9X, non-dominant wrist | ~7,000–8,000 adults with valid wear | 7 days, 24 h | Death from the National Death Index (public file, through 2019) | Free, data is public |
| **All of Us** | Fitbit (consumer, own device) | Tens of thousands | Months to years | Electronic health records, surveys, death data being added | Free, needs an institutional agreement |
| **Whitehall II** | GENEActiv, non-dominant wrist | ~4,000 (2012–13) | 9 days, 24 h | Hospital records, death, dementia | Proposal to the study team |
| **MESA Sleep** | Actiwatch Spectrum, wrist | ~2,200 | 7 days | Heart disease events, death | NSRR request, plus MESA for events |
| **MrOS / SOF** | Wrist actigraphs (older devices) | ~3,000 men / ~3,000 women | 3–5 days | Death, fractures, other events | NSRR or the study portals |

### 1. UK Biobank (your main dataset)
- **Why:** It is the largest wrist study with raw data, and most published wrist-based work on activity, sleep and outcomes uses it. That makes comparing your results with other studies easy.
- **Data:** You get raw files plus derived variables: ENMO acceleration, machine-learned activity and sleep classes, and step counts from the Oxford group's models. Outcomes come through linked hospital records, death and cancer registries. Primary care records cover about 45% of participants.
- **Caveats:** Participants are healthier than the general population and mostly white British. The device was worn on the dominant wrist, while NHANES and Whitehall II used the non-dominant wrist. Activity was measured about 5 years after baseline.
- **Access:**
  1. Register on the Access Management System. Your university and you as a researcher both need to be approved, which usually takes days to a couple of weeks.
  2. Submit a short proposal. Approval usually takes a few weeks.
  3. Sign the Material Transfer Agreement, which your institution signs.
  4. Pay the access fee. It is tiered, roughly several thousand pounds for a 3-year project; check the current rates.
- **Analysis environment:** Since 2024, analysis happens only on the cloud Research Analysis Platform (DNAnexus). You can't download data, and you pay compute and storage costs, which add up when processing raw accelerometer files. Separate ethics approval usually isn't needed, because UK Biobank has its own ethics approval, but check with your IRB.

### 2. NHANES 2011–2014 (easiest to get, and US-representative)
- **Data:** Wrist-worn, 24-hour wear for 7 days. Activity is released as MIMS units at minute, hour and day level, with flags for wear, sleep and non-wear. Mortality comes from the public NCHS Linked Mortality File, currently through Dec 31, 2019.
- **Access:** Download it from the CDC website now, no application needed. The restricted mortality file has the exact date of death and more detail; it requires an NCHS Research Data Center proposal, which takes months and has fees.
- **Caveats:** Death is the only outcome; there are no hospital records in the public files. The number of deaths is modest, about 1,000 or fewer in adults depending on the subset. Raw-data processing pipelines like GGIR need to be adapted to MIMS units. The 2003–2006 NHANES waves used a hip-worn device, so leave them out.

### 3. All of Us Research Program
- **Data:** Fitbit records of steps, heart rate, sleep stages and activity minutes, linked to electronic health records. Some participants have years of data, which allows long-term studies of habitual behavior.
- **Caveats:** These are consumer devices and only processed summaries are available, not raw acceleration, so results aren't directly comparable with research-grade studies. People who own Fitbits are a selected group. Outcomes depend on what the health records capture.
- **Access:**
  1. Your university must sign a Data Use and Registration Agreement; many US universities already have.
  2. You verify your identity, complete research ethics training and sign the code of conduct.
  3. Fitbit data is in the Registered Tier. Some detailed health record fields and dates are in the Controlled Tier, which requires extra training.
- **Analysis environment:** Free to use, but analysis happens on the cloud Researcher Workbench with initial credits, then you pay for compute. No IRB review is usually needed, and you must follow their publication and data-display rules.

### 4. Whitehall II (UK civil servants)
- **Data:** About 4,000 people wore GENEActiv devices on the wrist for 9 days in 2012–13. Raw data is available, with about a decade of linked hospital, death and dementia records. It is widely used for sleep, physical activity and dementia studies.
- **Access:** Submit a data-sharing proposal to the Whitehall II team at UCL. Data may come through the Dementias Platform UK portal. Expect a few months and a data-sharing agreement. The cohort is older and mostly male, with office-worker backgrounds.

### 5. Sleep-focused US cohorts via the National Sleep Research Resource (sleepdata.org)
- **MESA Sleep:** Wrist actigraphy plus sleep studies in a multi-ethnic sample. The NSRR provides the actigraphy. Adjudicated heart disease events and deaths may need a separate MESA paper proposal or the NHLBI biobank, BioLINCC.
- **MrOS and SOF:** Older men and women, with death and fracture follow-up. The devices are older, with limited activity information, so these are mainly useful for sleep and rest-activity rhythms.
- **Access:** NSRR asks for an online data access request, a data use agreement signed by your institution, and usually documentation of IRB approval or exemption. It is free and typically takes weeks.

### Others to watch or rule out
- **China Kadoorie Biobank:** About 20,000+ participants wore Axivity devices on the wrist in a recent resurvey, with linked hospital and death records. Check whether the accelerometer data has been released yet through its data access process.
- **Rotterdam Study and Baltimore Longitudinal Study of Aging:** Both have wrist GENEActiv data but smaller samples, and access requires collaborating with the study team.
- **Studies that don't fit:** Women's Health Study and OPACH (hip), NHANES 2003–06 (hip), CARDIA and Framingham (hip), HUNT4 (thigh and back) and the German National Cohort, NAKO (hip).

## Tips for comparability
- **Wrist side:** Record which wrist was used. UK Biobank used the dominant wrist; NHANES and Whitehall II used the non-dominant wrist. This shifts activity intensity estimates somewhat.
- **Processing:** Where you have raw data (UK Biobank, Whitehall II), process it with standard open tools such as GGIR or the Oxford `stepcount` and `asleep` models, and report ENMO or MIMS so other researchers can compare. Results based on MIMS and ENMO need to be harmonized before you pool or compare them.
- **Order of access:** A practical sequence is NHANES first, since you can download it today and use it for US mortality, then UK Biobank as the main analysis, then Whitehall II or All of Us for replication.

The fees, follow-up dates and sample sizes above are from memory. Check them on each program's website before you put them in a grant or IRB application.