Use NHANES for the US, and ELSA (England, ages 50+) and CHARLS (China, ages 45+) as the comparison surveys. All three have measured blood pressure and a "doctor ever told you" question, and a 2026 paper already runs the hypertension cascade across exactly these three. I checked what I could on 12 November 2026; the HRS and CHARLS sites would not open from here, so their terms rest on search snippets and memory.

## What I assumed you need
- **Must have:** blood pressure measured by a nurse or examiner.
- **Must have:** a question on ever being told by a doctor that you have high blood pressure.
- **Must have:** a nationally representative sample with weights.
- **Nice to have:** all adults (you said middle-aged and older is acceptable).
- **Nice to have (my assumption):** obtainable by a thesis student without an institutional contract.

## Shortlist
| # | Survey | Access | Licence | Sample | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES (US) | Direct download, minutes | NCHS Data User Agreement | All ages, 2-year cycles 1999–2023 | Strong | Today |
| 2 | ELSA (England) | Free UK Data Service account, days | End User Licence | Ages 50+ | Strong | Today; diagnosis item from memory |
| 3 | HRS (US) | Free account, days | HRS Conditions of Use | Ages 51+ | Strong, but interviewer-measured | Search snippets and memory |
| 4 | Health Survey for England | Free UK Data Service account, days | End User Licence | Ages 16+, annual | Strong | Record exists today; contents from memory |
| 5 | KNHANES (Korea) | Free registration, days | KDCA terms, no redistribution | All ages, annual | Strong | Search snippets |
| 6 | CHARLS (China) | Registration plus application, days | CHARLS data use agreement | Ages 45+ | Strong, 2011–2015 only | Partly today, rest from memory |
| 7 | LASI Wave 1 (India) | Request form to IIPS, weeks (my estimate) | IIPS release terms | 72,250 aged 45+ and spouses | Strong | Search snippets of the IIPS form |
| 8 | DHS (selected countries) | Project request, 24–48 h | DHS conditions of use | Varies by country | Partial | Today |

## Details

**1. NHANES** — https://wwwn.cdc.gov/nchs/nhanes/
- **Blood pressure:** the August 2021–August 2023 file (BPXO_L) has "three consecutive blood pressure (BP) and pulse measurements using an oscillometric device", taken by certified examiners.
- **Awareness question:** BPQ020, "ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?"
- **Access:** download the DEMO, BPQ and BPX/BPXO files per cycle, no login. Using the files means you accept the NCHS Data User Agreement (statistical use only, no re-identification).
- **Watch for:** older cycles used physician auscultatory readings and recent ones use oscillometric devices. Check the cut-over before building a trend; I recall it but did not confirm it.
- **Used in:** [Hypertension, Diabetes, and High Cholesterol Awareness Among US Adults (2025)](https://doi.org/10.1001/jamacardio.2025.1536).

**2. ELSA** — https://doi.org/10.5255/ukda-sn-5050-37
- **Blood pressure:** nurse visit files at waves 2, 4, 6 and 8/9, plus a wave 11 nurse file, with three readings each.
- **Awareness question:** doctor-diagnosed high blood pressure in the main interview (from memory; check the wave questionnaire).
- **Access:** register with the UK Data Service, accept the End User Licence and download study 5050. Outside the UK you "apply for a username and then register"; no turnaround time is stated.
- **Watch for:** UKDS says some collections are closed to non-UK users, so check the Access tab of the record. The wave 8 nurse visit covered only part of the sample.
- **Used in:** [the China/US/UK care cascade comparison (2026)](https://doi.org/10.3390/healthcare14040501).

**3. HRS** — https://hrsdata.isr.umich.edu/
- **Blood pressure:** Section I of the public core file. From memory, it is taken by trained interviewers, not nurses, on alternating half-samples since 2006; decide whether that meets your criterion.
- **Awareness question:** "Has a doctor ever told you that you have high blood pressure or hypertension?" (from memory).
- **Access:** free registration, which counts as accepting the Conditions of Use (no re-identification, no redistribution).
- **Used in:** [a four-country hypertension analysis with ELSA, CHARLS and LASI (2023)](https://doi.org/10.1161/jaha.123.030765).

**4. Health Survey for England** — https://doi.org/10.5255/ukda-sn-9469-1 (2022)
- **Why:** the all-adult English counterpart to NHANES, with one study per year.
- **Access:** same UK Data Service route as ELSA.
- **Watch for:** the nurse-visit BP and diagnosis question are from memory, as is the gap in 2020. Check each year's documentation.

**5. KNHANES** — https://knhanes.kdca.go.kr/knhanes/eng/main.do
- **Why:** measured BP and a physician-diagnosis item; this is the source of Korea's official awareness rates.
- **Access:** register on the KDCA site and download yearly files. I could not read the registration page, so the exact steps are unconfirmed.
- **Used in:** [a 2022–2024 care cascade paper](https://doi.org/10.3390/healthcare14193198).

**6. CHARLS** — https://charls.pku.edu.cn/en/ (did not answer today)
- **Blood pressure:** measured "at Waves 1 through 3" (2011, 2013, 2015) only, by trained interviewers.
- **Access:** register, submit an application with your research purpose and accept the agreement. Approval takes a few days, from memory. Derived files may not be redistributed.
- **Help:** the [Gateway to Global Aging page](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d) links step-by-step instructions.

**7. LASI Wave 1** — https://iipsindia.ac.in/content/lasi-wave-i
- **Contents:** three Omron readings, and item HT002 on ever being told of hypertension.
- **Access:** send IIPS the [data request form](https://iipsindia.ac.in/sites/default/files/LASI_DataRequestForm_0.pdf) with a research description of up to 500 words, a study proposal and identity proof.

**8. DHS** — https://dhsprogram.com/data/
- **Why:** an option for a low- or middle-income comparison; only some rounds carry a BP module (Bangladesh 2017–18 and 2022 do).
- **Access:** register, submit a project title and description, and wait for review "within 24 – 48 hours".
- **Used in:** [a Bangladesh hypertension control paper (2026)](https://doi.org/10.5334/gh.1575).

## Known, not confirmed
These fit as far as I recall, but I did not check their contents today:
- **Indonesia Family Life Survey:** the RAND site blocked the tool.
- **WHO SAGE and WHO STEPS surveys:** the pages exist, and STEPS is used for awareness in recent papers.
- **TILDA (Ireland):** the site did not respond.
- **Understanding Society nurse assessment (UK, 2010–2012) and the Scottish Health Survey:** the UK Data Service records exist.

## Not recommended, and why
- **BRFSS and NHIS:** self-report only (from memory).
- **SHARE:** no routine measured BP (from memory).
- **UK Biobank:** a volunteer cohort, not representative.
- **Canadian Health Measures Survey:** I recall the microdata sit in Statistics Canada Research Data Centres, which is slow from outside Canada.
- **Mexican Health and Aging Study:** BP only in subsamples (from memory). Its terms also forbid using LLM or AI tools on the microdata.

## What I could not find
- The registry search returned mostly noise for this topic; the list comes from known surveys, the literature and web search.
- I did not find a harmonised cross-country file that includes measured BP ready-made; the Gateway to Global Aging may have one, but I did not check.

## Next step
Download NHANES today and register with the UK Data Service and CHARLS in parallel, since those two involve waiting. The interactive shortlist is at `/private/tmp/e-FtUsPb/home/cwd/dataset-shortlist.html`.