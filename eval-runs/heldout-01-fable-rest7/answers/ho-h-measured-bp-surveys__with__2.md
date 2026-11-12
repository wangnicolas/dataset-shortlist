Use **NHANES** as your US core, **HRS** if you want a US 50+ estimate, and **ELSA** (England 50+) plus either **Health Survey for England** or **KNHANES** as the international comparators. All of these are free and need at most an online registration. Checked on 12 November 2026.

## What I assumed you need
- **R1 (must):** blood pressure measured by a nurse or trained examiner.
- **R2 (must):** a question on ever being told by a doctor that they have high blood pressure.
- **R3 (must):** a nationally representative adult sample; 45+/50+ is acceptable outside the US.
- **R4 (nice to have):** obtainable by a thesis student without an institutional contract. This is my assumption.

## Shortlist
| # | Survey | Country, ages | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES | US, all adults | Direct download, no account | NCHS data user agreement (statistical use only, no re-identification) | Strong | Today |
| 2 | HRS | US, 51+ | Free registration, minutes to a day | HRS conditions of use | Strong | Access from search results; the HRS site blocks automated readers |
| 3 | ELSA | England, 50+ | UK Data Service registration, minutes to days | End User Licence, non-commercial | Strong | Access today; nurse-wave detail from memory |
| 4 | Health Survey for England 2019 | England, 16+ | UK Data Service registration, minutes to days | End User Licence, non-commercial | Strong | Mostly today |
| 5 | CHARLS | China, 45+ | Free registration with approval, days | CHARLS data use agreement | Strong | Via Gateway to Global Aging; the CHARLS site was down |
| 6 | LASI Wave 1 | India, 45+ | Request form plus photo ID, 24–48 h review | Academic research only | Strong | Today |
| 7 | KNHANES | South Korea, all ages | Free download after accepting terms | KDCA terms | Strong | Access from memory |
| 8 | CHMS | Canada, 6–79 | Secure Research Data Centre only, months | Statistics Canada research agreement | Partial | Today |

## Details

**1. NHANES** — https://wwwn.cdc.gov/nchs/nhanes/
- **Blood pressure:** certified examiners take three readings 60 seconds apart with an Omron HEM-907XL in the mobile examination centre (August 2021–August 2023 cycle).
- **Awareness item:** BPQ020, "ever been told by a doctor or other health professional that you had hypertension, also called high blood pressure?", asked of ages 16+.
- **Steps:** download the DEMO, BPXO and BPQ files for each cycle, merge on SEQN, and use the examination weights. There is no account or fee.
- **Caveats:** auscultatory (mercury) readings stopped after 2017–2018 and later cycles are oscillometric, which matters for trends. From memory, a combined 2017–March 2020 pre-pandemic file also exists.
- **Used in:** [care-cascade comparison of China, the US and the UK](https://doi.org/10.3390/healthcare14040501) (NHANES, CHARLS, ELSA).

**2. HRS** — https://hrs.isr.umich.edu/data-products
- **Blood pressure:** measured in the home by trained interviewers, not nurses, since 2006. It sits in section I of the public core files, not in the sensitive-health tier.
- **Awareness item:** from memory, "Has a doctor ever told you that you have high blood pressure or hypertension?"; check section C of the questionnaire.
- **Steps:** register at hrsdata.isr.umich.edu, accept the conditions of use, and download the core files plus the Tracker file for the physical-measures weights.
- **Caveats:** a random half of the sample gets the in-person visit each wave, so pool adjacent waves. The conditions of use reportedly now include a policy on AI and language-model tools; read it before using hosted tools on the data.
- **Used in:** [HRS blood pressure control study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8824637/); [five-cohort hypertension care cascade in adults 50+](https://doi.org/10.1186/s12889-026-26341-4).

**3. ELSA** — https://doi.org/10.5255/ukda-sn-5050-37 (UK Data Service SN 5050)
- **Why:** it is the sister study of HRS, so it gives the cleanest comparison with a US 50+ estimate.
- **Blood pressure:** from memory, nurse visits with blood pressure are in waves 2, 4, 6 and 8/9 and are in the standard files. I could not confirm this today because the UK Data Service catalogue is not machine-readable.
- **Steps:** register with the UK Data Service (request a username if your university is not in the UK login federation), accept the End User Licence, add SN 5050 to a project with a short statement of intended use, and download.
- **Caveats:** England only; non-commercial use; no onward sharing.

**4. Health Survey for England 2019** — https://doi.org/10.5255/ukda-sn-8860-1 (SN 8860)
- **Why:** an all-adult annual cross-section with a nurse visit, the closest non-US analogue to NHANES.
- **Blood pressure:** the catalogue records list it among the nurse-collected measurements.
- **Awareness item:** doctor-diagnosed high blood pressure questions are in the interview, from memory.
- **Steps:** same UK Data Service route as ELSA.
- **Caveats:** since 2015 the standard release is the individual file only, and some variables moved to the Special Licence version (SN 8962). Check that the blood pressure variables you need are in SN 8860. The 2021 and 2022 surveys exist, but I did not confirm they had a full nurse visit.

**5. CHARLS** — https://charls.pku.edu.cn/en/ (site unreachable today)
- **Blood pressure:** measured in waves 1–3 (2011, 2013, 2015).
- **Awareness item:** a doctor-diagnosed hypertension question, from memory.
- **Steps:** register on the CHARLS site with your institution and purpose, accept the agreement, wait for approval (a few days, from memory), then download. The [Gateway to Global Aging page](https://g2aging.org/additional-resources/gateway-blog/05a8df66-b9ab-47de-879e-b0bde672798d) links step-by-step instructions.

**6. LASI Wave 1** — https://www.iipsindia.ac.in/content/LASI-data
- **Blood pressure:** three readings in the biomarker module.
- **Awareness item:** "Has any health professional ever told you that you have high blood pressure or hypertension?"
- **Steps:** follow the LASI Wave 1 Dataset link to the IIPS data portal, submit the request form with government-issued ID, and wait for review (24–48 working hours).
- **Caveat:** one wave only (2017–19, from memory).

**7. KNHANES** — https://knhanes.kdca.go.kr/knhanes/eng/main.do
- **Blood pressure:** three readings by a trained nurse.
- **Awareness item:** self-reported physician diagnosis.
- **Steps:** from memory, open the raw-data section, enter an email, accept the terms, and download the yearly SAS/SPSS files. The English page did not show these steps today, so confirm in a browser.
- **Used in:** [awareness trends in South Korea, 1998–2021](https://www.nature.com/articles/s41598-023-49055-8).

**8. CHMS** — https://crdcn.ca/data/canadian-health-measures-survey/
- **Blood pressure:** six oscillometric readings at a mobile centre.
- **Access:** microdata are analysed only inside Statistics Canada Research Data Centres, after a project proposal and security screening. In practice this needs a Canadian affiliation.
- **Alternative:** for a comparison figure, cite the published estimates in [Health Reports 2019](https://www150.statcan.gc.ca/n1/pub/82-003-x/2019002/article/00002-eng.pdf).

## Known, not confirmed
- **NSHAP** (US, older adults; Round 4 2021–23 at https://doi.org/10.3886/icpsr39511.v1): the record exists. Measured blood pressure, a hypertension-diagnosis item and download with a free ICPSR account are all from memory.
- **DHS Program** (https://dhsprogram.com/data/): "Datasets are available for free after a simple registration process." Only some country surveys include measured blood pressure; papers found today used Bangladesh 2017–18 and 2022 and Tanzania 2022.
- **WHO STEPS surveys** (https://extranet.who.int/ncdsmicrodata/index.php/catalog): the catalogue exists and a Sri Lanka 2021 analysis turned up today. Per-country access terms were not checked.
- **TILDA** (Ireland, 50+): withdrawn from ICPSR at the producer's request. It is now available only through TILDA/ISSDA to non-commercial applicants, with an application form and fees listed. I did not confirm that blood pressure is in the public file.
- **Add Health, IFLS, MHAS:** all have measured blood pressure from memory; I checked neither access nor fit.

## Not recommended, and why
- **NHIS and BRFSS:** self-reported hypertension only, with no measured blood pressure (from memory).
- **SHARE:** no measured blood pressure in the main waves (from memory).

## What I could not find
- The HRS, UK Data Service and CHARLS pages could not be read by machine today, so open each in a browser to confirm the terms.
- The exact wording of the ever-told item is confirmed only for NHANES and LASI.
- The general data registries returned nothing useful, because these surveys are published on agency and archive sites.

## Next step
Download NHANES today and start the US analysis. In parallel, register with the UK Data Service and HRS; both are short forms. Before pooling cycles or countries, fix one definition of hypertension (threshold, and whether medication use counts), because the awareness denominator depends on it. Also ask your institution whether secondary analysis of these files needs an ethics exemption.

The interactive shortlist with filters and an exportable access plan is at `/private/tmp/e-pzWgGy/home/cwd/dataset-shortlist.html`.