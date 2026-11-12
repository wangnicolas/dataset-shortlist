The best dataset for your question is UK Biobank, but it is not taking new applications right now. NHANES 2011–14 is the one you can download and start on today, though it only links to deaths. All of Us, Whitehall II and China Kadoorie Biobank are the other main options. All of these facts were checked on 12 Nov 2026.

## What I assumed you need
- **R1 (must):** the device was worn on the wrist. I counted consumer trackers like Fitbit as well as research accelerometers.
- **R2 (must):** free-living wear for several days to a week or more.
- **R3 (must):** at least a few thousand adults with device data.
- **R4 (must):** linked follow-up such as hospital records, diagnoses or death registrations.
- **R5 (nice to have, my assumption):** raw or minute-level signal, so you can compute activity and sleep metrics the same way other wrist studies do.
- **R6 (must):** a researcher at a US university can get it. You said waiting for an application is fine.

## Shortlist
| # | Dataset | Access | Wrist device, wear | N | Outcomes | Checked |
|---|---|---|---|---|---|---|
| 1 | **NHANES 2011–14 + public Linked Mortality File** | Open download, minutes | ActiGraph GT3X+, non-dominant wrist, 7 days | ~12,600 (all ages) | Deaths to end of 2019 | today (Medicare linkage from memory) |
| 2 | **UK Biobank accelerometer study** | Fee and application; **new applications closed**, reopening targeted for "late 2026" | Axivity AX3, dominant wrist, 7 days | ~100,000 | Hospital records, primary care, cancer, deaths | today (closure, fees); outcome detail from papers |
| 3 | **All of Us (Fitbit + health records)** | Your institution's agreement plus training, a few days | Fitbit, months to years | ~15,000 (2023); recent studies 29,000–44,000 | Health-record diagnoses; deaths partial | today (tiers); death completeness from memory |
| 4 | **Whitehall II accelerometer study** | Application via Dementias Platform UK, months | GENEActiv, non-dominant wrist, 9 days | ~4,200 valid | Hospital records (from memory) and deaths | today |
| 5 | **China Kadoorie Biobank resurvey 2020–21** | Application plus £2,500, months; may still be closed to outsiders | Axivity AX3, wrist, 7 days | ~20,000 | Hospitalisation and deaths (from memory); short follow-up | partly today |
| 6 | **MESA Sleep (wrist actigraphy)** | Data agreement, days; event data by separate request, weeks | Actiwatch, 7 days | ~2,200 | Confirmed heart events, deaths | today (actigraphy); event route from memory |
| 7 | **MrOS / SOF actigraphy** | Analysis proposal, weeks | SleepWatch-O, 3–5 days | ~3,100 men, ~3,000 women | Fractures, hospitalisations, deaths | from memory |

## Details

**1. NHANES 2011–2014 + Linked Mortality File (start here)**
- **Links:** [PAXMIN_G documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm), [linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm).
- **Data:** about 12,600 participants have minute-level activity data plus day and hour summaries. Adults link to the National Death Index through 31 Dec 2019.
- **Steps:**
  1. Download PAXMIN, PAXDAY, PAXHR and the demographics files for both waves.
  2. Download the `NHANES_2013_2014_MORT_2019_PUBLIC.dat` file and its 2011–12 equivalent from CDC's FTP site.
  3. Merge on the participant ID, `SEQN`.
- **Ready-made step counts:** an [open (CC0) PhysioNet version with minute-level step counts](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/) is also available.
- **Restricted data:** exact death dates or Medicare claims need an application to an NCHS Research Data Center (months, from memory).
- **Limits:** death is the only outcome, follow-up is about 6–8 years, and the public file slightly alters some variables.
- **Papers using it:** a 2024 study found [physical activity was the strongest predictor of death](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/); another used [activity profiles as markers of mortality](https://www.nature.com/articles/s41598-023-36062-y).

**2. UK Biobank**
- **Why it matters:** this is the reference wrist cohort. Linked hospital records, primary care, cancer registry and death data support analyses across hundreds of diseases, for example [MVPA vs 697 diseases](https://doi.org/10.1038/s41746-022-00676-9) and [sleep regularity and mortality](https://doi.org/10.7554/elife.88359.3).
- **Current status (confirmed today):** after an April 2026 data incident, all access was suspended. [UK Biobank's own FAQ](https://community.ukbiobank.ac.uk/hc/en-gb/articles/37284734505117-Can-I-apply-to-use-UK-Biobank-data) says "We are not currently accepting applications for new research projects" and that they aim to reopen in late 2026. When existing projects return, exporting results will be temporarily banned.
- **Steps once it reopens:**
  1. Register yourself and your institution on the Access Management System.
  2. Submit the project application.
  3. Sign the Material Transfer Agreement through your institution.
  4. Pay the [fee](https://www.ukbiobank.ac.uk/use-our-data/fees/): Tier 1 is £3,000 for 3 years, or £500 for students.
  5. Analyse on the cloud platform (UKB-RAP), where compute is billed.
- **Not confirmed:** which fee tier covers the raw accelerometer files. Ask their access team.

**3. All of Us**
- **Data:** wrist Fitbit data on steps, heart rate and sleep stages, often over months, linked to health-record diagnoses ([access tiers](https://www.researchallofus.org/data-tools/data-access/)).
- **Steps:**
  1. Check that your university has a DURA (the program's institutional data-use agreement).
  2. Create a Researcher Workbench account, verify your identity and complete the training.
  3. Get Controlled Tier access. You need it for time-to-event work because the basic (Registered) tier shifts dates randomly.
- **Caveats:**
  - It records consumer-device output, not raw acceleration.
  - There is no wear-time variable.
  - Participants who brought their own devices are a selected group.
  - Reported counts below 20 are not allowed.
- **Papers using it:** [step counts and chronic disease (Nat Med 2022)](https://doi.org/10.1038/s41591-022-02012-w) and [sleep and cardiometabolic disease (2026)](https://doi.org/10.1161/circoutcomes.126.014445).
- **Fit:** useful as a US complement, but less comparable with research-grade wrist studies.

**4. Whitehall II**
- **Data:** 4,880 people were asked in 2012–13 to wear a GENEActiv on the non-dominant wrist for 9 days, and 4,204 have valid data. Published work processes the raw files with the GGIR software.
- **Access:** apply through the [Dementias Platform UK portal](https://data.dpuk.ukserp.ac.uk/cohortdirectory/Item?fingerPrintID=Whitehall+II); the Whitehall II data sharing committee reviews applications, and analysis stays in DPUK's secure environment ([UCL data-sharing page](https://www.ucl.ac.uk/brain-sciences/psychiatry/our-research/mental-health-older-people/whitehall-ii/data-sharing)).
- **To check:** whether outside users can get the linked hospital records through DPUK.
- **Limits:** mostly male, white-collar civil servants.
- **Paper using it:** [mortality in Whitehall II and UK Biobank (2025)](https://doi.org/10.1038/s41598-025-30237-5).

**5. China Kadoorie Biobank**
- **Data:** same device and protocol as UK Biobank ([descriptive paper](https://doi.org/10.1186/s12966-023-01537-8)).
- **Access:** register on their data access system and apply online; approved requests from outside China cost £2,500 ([policy](https://www.ckbiobank.org/data-access/data-2)).
- **To check:** new data are reserved for the study's own researchers for a period first. I could not confirm whether the accelerometer data have been released yet. Look at their data overview and release schedule, or propose a collaboration.

**6. MESA Sleep**
- **Data:** wrist actigraphy downloads from the [National Sleep Research Resource](https://sleepdata.org/datasets/mesa) under its data agreement. Confirmed events and deaths come separately via BioLINCC or the MESA Coordinating Center (from memory).
- **Paper using it:** [sleep regularity and mortality](https://doi.org/10.1111/jsr.14048).
- **Limits:** N is below your target, and Actiwatch counts are not directly comparable with the metrics other wrist studies use.

**7. MrOS / SOF**
- **Data:** the National Sleep Research Resource's MrOS page says actigraphy is not included there. Use MrOS Online, or send an analysis proposal to the San Francisco Coordinating Center.
- **Limits:** older adults only, 3–5 days of wear.

## Known, not confirmed
- **Baltimore Longitudinal Study of Aging:** wrist ActiGraph, about 1,000+ people; probably too small. Access is by proposal ([how to apply](https://www.blsa.nih.gov/how-apply), which blocked my check).
- **Rotterdam Study:** wrist GENEActiv or actigraphy, about 2,000.
- **HCHS/SOL Sueño:** wrist Actiwatch, about 2,000; via the National Sleep Research Resource and BioLINCC.
- **Pelotas 1982 cohort:** about 3,000 adults with wrist GENEActiv, but little disease follow-up.

All of these are from memory; check their size and outcome linkage.

## Not recommended
- **NHANES 2003–06:** hip-worn device.
- **Women's Health Initiative OPACH and Women's Health Study:** hip-worn (from memory).
- **HUNT4, Tromsø, 1970 British Cohort Study:** thigh, back or hip placement (from memory).
- **CAPTURE-24:** wrist and open, but about 150 people with no health outcomes. It is only useful for validating activity classifiers.

## What I could not find
- No openly downloadable wrist dataset linked to hospital records; NHANES only links to deaths.
- Several official sites (UK Biobank, UCL, CKB, sleepdata.org) blocked automated checks, so I took those facts from web-search summaries of the pages or from memory, as marked.
- The registry searches turned up almost nothing relevant; the candidates came from the literature and the web.

## Next step
1. Start on NHANES now.
2. Check this week whether your university has an All of Us DURA, and apply.
3. Register on the UK Biobank and DPUK portals so you can submit once UK Biobank reopens. Whitehall II is useful as a second wrist cohort to replicate your UK Biobank results.

The interactive comparison page is at `/private/tmp/e-IgJsbM/home/cwd/dataset-shortlist.html`.