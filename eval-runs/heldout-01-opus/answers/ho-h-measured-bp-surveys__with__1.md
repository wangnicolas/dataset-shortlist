I'd use **NHANES** as the core US source, with **ELSA (England)** and **CHARLS (China)** or **LASI (India)** for the international comparison. If you want the comparison to line up closely, add **HRS** as the US arm for ages 50+. All of these are free and you can have them within minutes to a few days.

**Where these facts come from:** I checked on 2026-11-12. Facts marked "today" came from the survey's own page or documentation. The rest is from memory, and you should check it in the codebooks before relying on it.

## What I assumed you need
- **Must have:** a national sample (an older-adult sample is fine), blood pressure measured by an examiner, a self-reported "ever told you have high blood pressure" question, antihypertensive medication (so treated people with normal readings still count as hypertensive), and survey weights.
- **Nice to have:** you can get the data within a few weeks with no fee.

## Shortlist
| # | Survey | Who's in it | Access | Checked |
|---|---|---|---|---|
| 1 | **NHANES** (US) | all ages | direct download, minutes | today |
| 2 | **HRS** (US) | 50+ | free account, minutes | today (via HRS documentation) |
| 3 | **ELSA** (England) | 50+ | free UK Data Service account, 1–2 days | today |
| 4 | **CHARLS** (China) | 45+ | registration plus approval, about 3 days | today (via web search) |
| 5 | **LASI** (India) | 45+ | registration through the Gateway to Global Aging Data | today (via web search) |
| 6 | **KNHANES** (South Korea) | all ages | free registration; the site is mostly in Korean | partly |
| 7 | **WHO SAGE** (6 low- and middle-income countries) | 50+ | registration plus a short request | from memory |
| 8 | **WHO STEPS** (many countries) | 18–69 | account plus a request for each country | partly |

## Details and how to get each one

**1. NHANES**: https://wwwn.cdc.gov/nchs/nhanes/
- **Variables (seen today):** BP is measured at the mobile exam centre, in file BPXO_L (`BPXOSY1`, `BPXODI1`, …). The awareness question is in BPQ_L: `BPQ020` asks "Have you ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?" The documentation says you must use the design variables and weights.
- **Steps:** pick a cycle, download the DEMO, BPXO (or BPX) and BPQ `.xpt` files, then merge them on `SEQN`.
- **Licence:** US public domain; cite NCHS.
- **Caveat:** the 2021–23 cycle measured BP with an automatic (oscillometric) device. Earlier cycles used the auscultatory (BPX) method, which matters if you look at trends.
- **Papers using it:** [Gu et al. 2008, AJH](https://doi.org/10.1038/ajh.2008.185) and [Gu et al. 2012, Circulation](https://doi.org/10.1161/circulationaha.112.096156).

**2. HRS**: https://hrs.isr.umich.edu/
- **Content:** since 2006, a random half of the sample gets an enhanced interview with physical measures each wave, including BP. The core interview asks about doctor-diagnosed high BP and medication (from memory).
- **Steps:** register for free, accept the Conditions of Use, and download the core files (Section I) or the RAND HRS longitudinal file.
- **Conditions:** you agree not to try to identify participants and not to pass the data to third parties.
- **Caveats:**
  - Trained interviewers measure BP, not nurses. That's still an objective measurement, but say so in your methods.
  - Each person is measured only every 4 years.
- **Why use it:** it is harmonised with ELSA, CHARLS and LASI through the Gateway to Global Aging Data (g2aging.org), which makes it the cleanest basis for a cross-national comparison.

**3. ELSA**: https://www.elsa-project.ac.uk/accessing-elsa-data
- **Access (seen today):** the ELSA site says "End User Licence level data are available to all via UKDS"; non-UK users "can request a username."
- **Content (from memory):** nurse visits measure BP in waves 2, 4, 6 and 8/9, with diagnosis and medication questions and nurse-visit weights.
- **Steps:** register with the UK Data Service, accept the End User Licence, and download study SN 5050.

**4. CHARLS**: https://charls.pku.edu.cn/en/
- **Content:** interviewers take three BP readings.
- **Steps:** register, sign the data-use agreement, and you get a password by email after about 3 days.
- **Caveat:** measured BP is confirmed for waves 1–3 (2011, 2013, 2015). Check whether 2018 and later waves have it.

**5. LASI**: https://lasi-india.org/data-instructions
- **Content:** wave 1 (2017–18), about 73,000 people.
- **Steps:** access is through the Gateway to Global Aging Data; registration is free with agreement to the data-use conditions.
- **Paper doing exactly your analysis:** [PLOS Med 2021](https://doi.org/10.1371/journal.pmed.1003740).

**6. KNHANES**: https://knhanes.kdca.go.kr
- **Why consider it:** it is the closest equivalent to NHANES outside the US: all ages, examiner-measured BP, free SAS/SPSS files.
- **Not confirmed:** whether foreign users can register without hurdles. The site and codebooks are largely in Korean.

**7 and 8. WHO SAGE and STEPS**
- **SAGE:** the paper on awareness in 6 countries ([IJE 2014](https://doi.org/10.1093/ije/dyt215)) used it, but its data are from 2007–10.
- **STEPS:** many countries, but only ages 18–69, and access depends on the country.

## Known, not confirmed
I couldn't check these today, but as far as I know they have measured BP plus self-report:
- **Health Survey for England:** the HSE site blocked automated access; data are on the UK Data Service.
- **MHAS** (Mexico), **TILDA** (Ireland) and **ELSI-Brazil:** their sites didn't respond.

## Not recommended
- **NHIS and BRFSS:** self-reported hypertension only.
- **SHARE:** no BP measurement.
- **UK Biobank:** volunteers rather than a national sample, and the application is paid.
- **Canadian Health Measures Survey:** fits on content, but you can only use it inside a Statistics Canada Research Data Centre, which takes months.
- **CLSA:** application with a fee, and the sample isn't strictly representative.

## Next step
Which comparator to pick depends on the framing:
- **All adults:** compare NHANES with KNHANES or HSE.
- **Older adults:** compare HRS (plus NHANES restricted to ages 50+) with ELSA and CHARLS or LASI, using the Gateway harmonised files.

[This 2026 BMC Public Health paper](https://doi.org/10.1186/s12889-026-26341-4) looks at gaps in hypertension care across five national ageing cohorts. I haven't checked which cohorts it uses, but it would be worth reading as a template for the older-adult version.

Sources: [CHARLS user guide](https://charls.charlsdata.com/Public/ashelf/public/uploads/document/2011-charls-wave1/application/CHARLS_nationalbaseline_users_guide.pdf), [Gateway: CHARLS](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d), [Gateway: LASI](https://g2aging.org/additional-resources/gateway-blog/a1336913-5fb6-4198-b592-3802ef4729e8), [Gateway harmonised data](https://g2aging.org/harmonized-data/get-data), [HRS 2018 data description](https://hrsdata.isr.umich.edu/sites/default/files/documentation/data-descriptions/1652380440/h18dd.pdf), [HRS public data overview](https://hrs.isr.umich.edu/sites/default/files/biblio/OverviewofHRSPublicData.pdf), [KNHANES profile (IJE)](https://academic.oup.com/ije/article/43/1/69/733063), [JKMS 2025](https://jkms.org/pdf/10.3346/jkms.2025.40.e189)

There's an interactive page where you can compare and filter the surveys and export an access plan: `/private/tmp/e-efRboB/home/cwd/dataset-shortlist.html`