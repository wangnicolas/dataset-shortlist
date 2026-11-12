Use NHANES as your US core, and add ELSA (England) and CHARLS (China) as the international comparisons. All three pair measured blood pressure with a "has a doctor ever told you" question and are free. This is from memory rather than checked against the survey sites today, so confirm wave and file details on each site before you commit.

| Survey | Population | Who measures BP | How to get it |
|---|---|---|---|
| **NHANES** (CDC/NCHS) | US civilian non-institutionalised population, all ages | Physicians in the mobile exam centre through 2017–18 (mercury auscultatory), then health technicians with an oscillometric device | Download directly from the NHANES site; no registration or application |
| **ELSA** | England, age 50+ | Nurse visit in waves 2, 4, 6 and 8/9 only | Register with the UK Data Service, add ELSA (study number 5050) to a project and accept the End User Licence; open to non-UK academics |
| **CHARLS** | China, age 45+ | Trained interviewers, in the 2011, 2013 and 2015 waves | Register on the CHARLS site (Peking University) and submit a short data-use application; approval usually takes days |

**NHANES**
- Merge the demographics (`DEMO`), blood pressure exam (`BPX`, or `BPXO` for oscillometric readings) and blood pressure questionnaire (`BPQ`) files on `SEQN`.
- The awareness item is `BPQ020`: ever told by a doctor or other health professional that you had hypertension, also called high blood pressure.
- Use the exam weights (`WTMEC2YR`), not the interview weights, with the design variables `SDMVSTRA` and `SDMVPSU`.
- The 2019–20 cycle was cut short by COVID and is only released combined as 2017–March 2020, with its own weight.
- The change from auscultatory to oscillometric measurement matters if you report trends.

**ELSA and CHARLS**
- The Gateway to Global Aging Data (g2aging.org, free registration) provides harmonised versions of both, built to match the RAND HRS file.
- After baseline, both surveys ask about new diagnoses since the last interview, so "ever told" has to be carried forward across waves. The harmonised "ever had high blood pressure" variable already does this.
- Use the nurse-visit or biomarker weights, not the main interview weights.

**Other options**
- **HRS (US, 50+)**: add this if you want a like-for-like US match to ELSA and CHARLS. Interviewers have measured blood pressure on a rotating half-sample each wave since 2006; access is free with registration on the HRS site.
- **Health Survey for England**: the closest all-adult analogue to NHANES, with a nurse visit and the same UK Data Service route as ELSA.
- **KNHANES (South Korea)**: also all-adult and examiner-measured, free after registration with the Korean disease control agency.
- **LASI (India, 45+)**: has measured blood pressure, but only one wave (2017–19), requested from IIPS.

**Surveys to avoid**
- BRFSS and NHIS are self-report only.
- SHARE (Europe) has no measured blood pressure in its main waves.
- The Canadian Health Measures Survey has measured blood pressure, but the microdata are only available through Statistics Canada's Research Data Centres.

**Comparability**
Protocols differ in device, number of readings and who takes them, so state these in your methods. Fix one definition across surveys: hypertension as mean measured BP at or above 140/90 or current antihypertensive medication, and unaware as hypertensive with no reported diagnosis. Run 130/80 as a sensitivity analysis if you want the newer US threshold.