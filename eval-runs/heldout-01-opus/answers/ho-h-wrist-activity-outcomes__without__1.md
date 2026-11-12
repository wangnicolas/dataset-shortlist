For a US-based study of wrist accelerometry predicting later outcomes, the three main options are **UK Biobank** (largest, best outcome linkage), **NHANES 2011–2014** (free, US, linked to deaths) and **All of Us** (US, Fitbit plus medical records). After those come several smaller cohorts that are still useful. I wrote this from what I already know and didn't look anything up during this session. Treat fees, sample sizes and follow-up end dates as approximate, and check them on each study's site before you plan around them.

## Main options

### 1. UK Biobank accelerometer sub-study (best overall fit)
- **Device and wear:** Axivity AX3 on the **dominant wrist**, about 7 days of continuous wear, collected 2013–2015. Roughly 100,000 participants aged about 43–79. Raw 100 Hz data and processed summaries (activity, sleep and sedentary measures, ENMO) are both available. A few thousand participants also did repeat wears across seasons.
- **Outcomes:** linked hospital records for England, Scotland and Wales, national death and cancer registries, and GP records for part of the cohort. That gives roughly 8–10 years of follow-up after the wear week, so even fairly uncommon diseases have enough cases to study. This is the reference dataset most wrist-accelerometry outcome papers use.
- **Access:**
  1. Register yourself and your university on UK Biobank's Access Management System.
  2. Submit a research proposal. Approval usually takes weeks.
  3. Your institution signs a Material Transfer Agreement.
  4. Pay a tiered access fee, typically a few thousand pounds for three years, with reductions for students and early-career researchers.
- **Practical point:** analysis now happens only on UK Biobank's cloud platform (the Research Analysis Platform on DNAnexus). Data can't be downloaded, so budget for compute and storage, which matters if you reprocess the raw files. US universities apply routinely.

### 2. NHANES 2011–2014 (free, nationally representative US sample)
- **Device and wear:** ActiGraph GT3X+ on the **non-dominant wrist**, 7 days around the clock. About 7,000–9,000 adults have valid data. Minute-level summaries (in MIMS units) are public, and NCHS has also released the raw 80 Hz files.
- **Outcomes:** the public-use Linked Mortality Files connect participants to the National Death Index, including underlying cause of death. The most recent public follow-up I know of runs to the end of 2019, so check whether a newer one has been released. Medicare claims and the more detailed restricted mortality file are only available through an NCHS Research Data Center.
- **Access:** the public data has no application at all; you just download it. The Research Data Center route requires a proposal, a fee and work in a secure enclave.
- **Limitations:** mortality is the only outcome without the Research Data Center, follow-up is shorter, and the number of deaths is moderate. Use the survey weights. The older NHANES 2003–2006 accelerometer data was worn on the **hip**, so don't combine it with the wrist data.

### 3. All of Us Research Program (US, consumer trackers plus medical records)
- **Device and wear:** participants' own Fitbits (wrist-worn), plus devices the program has handed out. Tens of thousands of people have Fitbit data, often covering months to years. Measures include steps, heart rate, sleep stages and active minutes.
- **Outcomes:** electronic health records (diagnoses, procedures, labs) and surveys. Some mortality data exists. Check what the current release includes.
- **Access:**
  1. Your university signs a Data Use and Registration Agreement (many already have one).
  2. You verify your identity and complete the required ethics training.
  3. You work in the cloud Researcher Workbench. Data access is free; compute is paid, with starter credits provided.
- **Limitations:** Fitbit uses its own unpublished algorithms and there's no raw acceleration, so results are harder to compare with research-grade devices. Participants who share Fitbit data are a self-selected group. Medical records only cover care at participating health systems, so outcomes will be missed. Also, wear-time and data-quality rules work differently for long-term consumer data than for a fixed 7-day protocol.

## Smaller cohorts worth adding (useful for replication or pooling)

| Study | Wrist device and wear | Size | Outcomes | Access |
|---|---|---|---|---|
| **Whitehall II** (UK civil servants) | GENEActiv, non-dominant wrist, about 9 days, 2012–13, raw data | About 4,000, aged 60–83 | Linked UK hospital records and death registry; dementia | Proposal to the study team at UCL, or through the Dementias Platform UK data portal |
| **MrOS Sleep** (older US men) | Wrist actigraph (Ambulatory Monitoring SleepWatch-O), about 5 days, 2003–05, activity counts | About 3,000 | Expert-reviewed deaths, fractures and cardiovascular events over long follow-up | Free registration on MrOS Online; actigraphy also on the National Sleep Research Resource (NSRR) |
| **SOF** (older US women) | Wrist actigraph, about 3–5 days, 2002–04 | About 3,000 | Expert-reviewed deaths and fractures | Through the SOF/MrOS team at UCSF and NSRR |
| **MESA Sleep** (multi-ethnic US cohort) | Actiwatch Spectrum, wrist, 7 days, 2010–13 | About 2,200 | Expert-reviewed cardiovascular events and deaths | Actigraphy through NSRR (data use agreement, free); event data through NHLBI's BioLINCC repository or the MESA coordinating center |
| **China Kadoorie Biobank** | Axivity AX3, wrist, at the 2020–21 resurvey | About 20,000+ | Linked hospital insurance records and death registry | Through CKB's data access process; check whether the accelerometer data has been released yet |

MrOS, SOF and MESA are better suited to sleep and daily activity rhythms than to activity intensity. Their older devices record counts rather than raw signals.

## Why these studies may not match even though they're all wrist-worn
- **Which wrist:** UK Biobank used the dominant wrist. NHANES, Whitehall II and MESA used mostly the non-dominant wrist. The dominant wrist registers somewhat more movement, so check how much this shifts your cut-points.
- **Units:** UK Biobank and Whitehall II record raw g, usually summarised as ENMO. NHANES reports MIMS units. The older actigraphs record proprietary counts. To get comparable measures, reprocess the raw data with one pipeline where you can, such as GGIR or the Oxford `stepcount`/biobankAccelerometerAnalysis tools. Where only summaries exist, use rank-based or standardised exposures.
- **Not wrist-worn, despite being large:** the Women's Health Study, NHANES 2003–06, the German National Cohort (NAKO) and CARDIA used the hip, and HUNT4 used the thigh and back.

## What I'd suggest
1. Make UK Biobank your main analysis.
2. Replicate in NHANES 2011–14, which is quick and free.
3. Add Whitehall II, or MrOS/MESA if sleep is the focus, for checks in independent cohorts.

Treat All of Us as a separate consumer-device analysis rather than pooling it with the others. Start the UK Biobank and All of Us institutional paperwork early, because the agreements your university has to sign usually take the longest.