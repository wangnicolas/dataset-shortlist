## What I assumed you need

- **R1 (must):** Wrist-worn accelerometer or tracker worn in daily life for at least several days.
- **R2 (must):** A few thousand adults or more.
- **R3 (must):** Linked follow-up outcomes (hospital records, diagnoses or death registration).
- **R4 (must):** Obtainable by a US university through an application.
- **R5 (nice to have):** Raw or near-raw signal, so results are comparable with other wrist studies.

**What I could and couldn't check (12 Nov 2026).**
- I ran searches on Zenodo, OpenAIRE, PhysioNet and Hugging Face, plus a literature search.
- Registries were mostly noise for this topic, so the useful candidates came from my own recall and the papers.
- The UK Biobank, UCL and China Kadoorie sites blocked automated access. The sleep-research site (sleepdata.org) failed on an SSL error in this sandbox.
- **What I did confirm today:** the NHANES, NCHS, All of Us and PhysioNet pages.
- **Everything else is from memory.** It is labelled that way below, and you should confirm it on the owner's page.

## Shortlist

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | UK Biobank accelerometer substudy | Application, institutional agreement, fee; about weeks | Data access agreement | about 90–100k | Strong | Papers confirmed today; access from memory |
| 2 | NHANES 2011–14 wrist data + NCHS linked mortality | Public download, minutes | US public data | about 7–8k adults | Strong for death; hospital outcomes need a restricted application | Mortality page confirmed today; wrist details from memory |
| 3 | All of Us (Fitbit) | Institutional agreement, training, registration; about weeks | Program terms | tens of thousands (memory) | Partial: consumer device | Access page confirmed today |
| 4 | NSRR: MrOS Sleep, SOF, MESA Sleep | Free account + data use agreement; about days | Per study | about 2–3k each | Strong, but older adults only | From memory |
| 5 | PhysioNet minute-level NHANES | Open, minutes | CC0-1.0 | not checked | Partial: no outcomes | Registry record confirmed today |
| 6 | Whitehall II | Data-sharing request to UCL; months | Unknown | about 4k (memory) | Partial | From memory |
| 7 | China Kadoorie Biobank | Application; months | Unknown | about 25k wearers (memory) | Unknown | From memory |

## Details

**1. UK Biobank**
- **Contents (from memory):** A dominant-wrist Axivity AX3 worn for 7 days in 2013–15. It is linked to hospital inpatient, death and cancer registries, with raw files available.
- **Why it fits:** It is the cohort most wrist-based papers compare against. A 2026 paper in PLOS Medicine used wrist data from 95,559 participants to study incident disease (https://doi.org/10.1371/journal.pmed.1005213).
- **Access (from memory):**
  1. Register on the UK Biobank Access Management System.
  2. Submit a project application.
  3. Have your institution sign the Material Transfer Agreement and pay the access fee. Check the current tariff.
  4. Analyse on the cloud Research Analysis Platform, because data isn't downloaded.
- **Caveats:** The cohort is healthy-volunteer, UK-based and mostly white. Follow-up from the wear date is about 8–10 years.

**2. NHANES 2011–14 plus linked mortality**
- **Contents:** From memory, an ActiGraph GT3X+ on the non-dominant wrist, worn 24 hours a day for 7 days.
- **Access:** The NHANES site loaded today, and I believe the files need no account. The NCHS page confirms public-use linked mortality files: "The linked public-use files contain a limited set of mortality (death) data for adults."
- **Restricted option:** "Restricted-use LMFs can be accessed only through the NCHS Research Data Center (RDC) network for approved projects." You'd need that route for anything beyond death.
- **Caveats:** Public mortality data is deaths only, and some fields are altered for privacy. Follow-up is about 5–8 years.
- **Start here today:** This is the one you can begin on before any application clears. A paper using NHANES wrist data and mortality is https://doi.org/10.1038/s41598-023-36062-y.

**3. All of Us**
- **Access page, confirmed today:** The Registered Tier "includes data from electronic health records (EHRs), wearables, surveys, and physical measurements." You need a "data passport" and work in the Researcher Workbench.
- **Institutional agreement and training:** These are from memory.
- **Caveats:** Fitbit output is vendor-derived minute-level steps, heart rate and sleep summaries, not raw acceleration. It won't compare directly with research-grade wrist studies. Death data are patchy, from memory.
- **Literature:** The search returned a 2025 paper titled "Fitbit Physical Activity and Sleep Data in the All of Us Research Program: Data Exploration and Processing Considerations". I didn't capture its DOI.

**4. NSRR (MrOS Sleep, SOF, MESA Sleep)**
- **Contents (all from memory):** Wrist actigraphy for roughly 5–7 nights, in older adults, with mortality and cardiovascular events. Each cohort has a few thousand people.
- **Access (from memory):** A free account on sleepdata.org, then a data use agreement per dataset, with approval in days.
- **To check:** How many outcomes are in the NSRR release versus held by each parent cohort's coordinating centre.
- **Caveats:** Data are epoch-level actigraphy, not raw. The devices differ from the UK Biobank and NHANES ones.
- **Literature:** An MrOS Sleep paper is https://doi.org/10.5665/sleep.3562.

**5. PhysioNet minute-level NHANES**
- It is open under CC0-1.0, confirmed by the registry (https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/).
- It has no outcomes, so you'd merge the NCHS mortality files yourself.
- It's useful for method development.

## Known, not confirmed

- **Whitehall II:** I recall GENEActiv wrist data in about 4,000 people, with hospital and mortality linkage, and access by a data-sharing request. A 2026 JAMA Neurology paper used it as a validation cohort (https://doi.org/10.1001/jamaneurol.2026.1232). The UCL page blocked me, so confirm access terms and sample size with the study team.
- **China Kadoorie Biobank:** I recall a wrist-accelerometer subsample of about 25,000 people with death and disease registry linkage. The site returned a 403 error, and I'm not sure the accelerometer data are released. Check ckbiobank.org/data-access.

## Not recommended, and why

- **NHANES 2003–06 accelerometer:** From memory, this was hip-worn, so it fails the wrist requirement.
- **Zenodo and Hugging Face hits:** Small or non-cohort files with no linked disease outcomes. An example is the Vanuatu GENEActiv files.

## What I could not find

- I could not confirm the UK Biobank fee, current process or timeline today.
- I could not confirm the NSRR or Whitehall II outcome coverage.
- I didn't search other possible cohorts such as the Rotterdam Study, Our Future Health or Generation Scotland.

## Next step

1. Download NHANES wrist data and the public mortality files this week to prototype your analysis.
2. Start the UK Biobank application in parallel, since it is the main dataset.
3. Request the NSRR datasets for older-adult validation.
4. Ask your institution early whether a human-subjects exemption determination is needed.
5. If you use a hosted AI service on restricted data, check each agreement first. Many forbid sharing data with third parties.

Interactive page: `/private/tmp/e-KFuVNn/home/cwd/dataset-shortlist.html`