Six datasets meet your requirements. The biggest finding is about UK Biobank, the standard reference cohort for wrist-outcome studies: since a data incident in April 2026 **it is not accepting new applications**. Its apply page (seen through web search) says it intends to "accept new applications in late 2026", and no firm date has been announced. You can start on NHANES today, and All of Us within days.

## What I assumed you need
- **Must have:** a wrist-worn accelerometer or tracker, worn in daily life for about 4–7+ days, in a few thousand adults or more, linked to outcomes (hospital, diagnosis or death records), and obtainable from a US university.
- **Nice to have:** sleep measured too, and raw or minute-level signal so you can compute the same metrics as other wrist studies.
- **Assumed:** you are willing to wait weeks to months for an application.

## Shortlist (checked 12 Nov 2026)
| # | Dataset | Access | Wrist data | N | Outcomes | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES 2011–14 + NCHS Linked Mortality File | Open download; restricted extensions need an NCHS Research Data Center (RDC) project | Non-dominant wrist, 7 days, raw 80 Hz + minute-level | ~14,700 wearers (~7,000 adults in mortality analyses) | Deaths (public file); hospital/Medicare via restricted linkage | today |
| 2 | All of Us (Fitbit + electronic health records) | Institutional agreement (DURA) + training, days | Fitbit, months to years, summaries only | ~13–16k sharing Fitbit data; ~53k with a device record | Health-record diagnoses, visits, deaths | today |
| 3 | UK Biobank accelerometer study | Application + fee (£3,000 / 3 yrs; £500 for students), **applications paused** | Axivity AX3, dominant wrist, 7 days, raw | ~100k | Hospital records, cancer, deaths, GP records | today (via search snippets) |
| 4 | Whitehall II, 2012–13 wave | Application via the DPUK portal, weeks; fee possibly £500 | GENEActiv, non-dominant wrist, 9 days, raw | 4,204 | Hospital records + mortality (linkage from memory) | today (via search snippets) |
| 5 | China Kadoorie Biobank accelerometer study | Application, £2,500 per request outside China | Axivity AX3, wrist (2020–21) | ~20,400 | Insurance claims + deaths (from memory); short follow-up | partly; release status unconfirmed |
| 6 | MrOS + SOF actigraphy | Free registration (from memory) | SleepWatch-O, non-dominant wrist, 4–5 days, 1-min counts | ~3,000 men + ~3,000 women, aged 65+ | Deaths, fractures, cardiovascular events confirmed by the studies | sizes/device today; access from memory |

## Details and how to get each one
1. **NHANES 2011–2014** ([PAXMIN_G docs](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/PAXMIN_G.htm), [mortality linkage](https://www.cdc.gov/nchs/linked-data/mortality-files/)).
   - **Data:** about 99% of monitors were on the non-dominant wrist. Files include a minute-by-minute wake/sleep/non-wear prediction (`PAXPREDM`), and the raw 80 Hz data is about 1 TB compressed.
   - **Get it:** download the accelerometer files and the public-use mortality file directly. The public mortality file comes from an earlier linkage and has altered details. Follow-up to 2022 and the Medicare linkage are only in restricted files at an NCHS Research Data Center, which needs a project application.
   - **Extra files:** activity counts and step counts per minute for all 14,693 wearers are on [PhysioNet](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/) (CC0, open).
   - **Example paper:** an [activity fragmentation and mortality study](https://doi.org/10.1186/s12889-026-29778-9) (2026).
   - Use the survey weights.
2. **All of Us** ([access tiers](https://www.researchallofus.org/data-tools/data-access/)).
   - **Get it:** your institution's signing official signs the DURA (many US universities already have). You then register, verify your identity and complete the research conduct training. Controlled-tier data (including deaths) needs extra training.
   - **Caveats:** Fitbit gives proprietary summaries, not raw acceleration, so comparing with raw-signal wrist studies is limited. People who share Fitbit data are a self-selected group. Analysis is cloud-only.
   - **Example papers:** [Nature Medicine 2022 on step counts and chronic disease](https://doi.org/10.1038/s41591-022-02012-w), and [a 2026 Circulation: Cardiovascular Quality and Outcomes paper on sleep](https://doi.org/10.1161/circoutcomes.126.014445).
3. **UK Biobank** ([apply](https://www.ukbiobank.ac.uk/use-our-data/apply-for-access/), [fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)).
   - **Why it matters:** this is the reference dataset most other wrist studies use, so it's the best one for comparability.
   - **Status:** its analysis platform was suspended on 23 April 2026. Reopening reportedly waits on government approval, exporting results files will at first be restricted, and new GP data is being withheld for now.
   - **Get it:** register in the Access Management System now and watch the UK Biobank Community site for the reopening date.
   - **Example papers:** [Doherty 2017](https://doi.org/10.1371/journal.pone.0169649) and [activity and 697 diseases (2022)](https://doi.org/10.1038/s41746-022-00676-9).
4. **Whitehall II** ([data-sharing FAQ](https://www.ucl.ac.uk/brain-sciences/psychiatry/our-research/mental-health-older-people/whitehall-ii/data-sharing/data-sharing-faq)).
   - **Get it:** apply through the DPUK portal. A committee meets monthly, then you sign a data sharing agreement. Sources disagree on whether the £500+VAT fee still applies, so ask whitehall2@ucl.ac.uk.
   - **Caveats:** analysis is probably inside DPUK's secure environment. Participants were aged about 60–83 and mostly white.
   - **Example paper:** [epoch choice and mortality (2025)](https://doi.org/10.1038/s41598-025-30237-5).
5. **China Kadoorie Biobank** ([access policy](https://www.ckbiobank.org/data-access/data-2)).
   - **Why it's useful:** it uses the same AX3 wrist device as UK Biobank.
   - **Unconfirmed:** CKB researchers get exclusive use before data is released, and I couldn't confirm whether the accelerometer data is out yet. Check the data overview page.
   - **Description paper:** [IJBNPA 2023](https://doi.org/10.1186/s12966-023-01537-8).
6. **MrOS / SOF** ([MrOS Online](https://mrosonline.ucsf.edu/)).
   - **Good for:** sleep and rest-activity rhythms.
   - **Limits:** older-device counts aren't comparable with raw-signal metrics. The NSRR copy of MrOS has no actigraphy, so use MrOS Online.
   - **Example paper:** [rest/activity rhythms and mortality (2010)](https://doi.org/10.3109/07420520903419157).

## Known, not confirmed
- **Pelotas 1982/1993 birth cohorts** (GENEActiv wrist, several thousand young adults) and the **Rotterdam Study** (GENEActiv wrist) may fit, but I didn't check their size, outcome linkage or access.
- **Websites I couldn't read directly:** UK Biobank, UCL, CKB and sleepdata.org blocked automated requests. Their terms above come from search-engine snippets of their official pages, so confirm them in a browser.

## Not recommended
- **MESA Sleep:** wrist Actiwatch with confirmed cardiovascular events, but only 2,237 people. Good for replication.
- **HCHS/SOL Sueño:** about 2,200 people with wrist devices; the main study measured activity at the hip.
- **Wrong body placement (from memory):** NHANES 2003–06, WHI OPACH, the Women's Health Study, CARDIA and NAKO used hip devices; HUNT4 and the 1970 British Cohort used thigh or back devices.

## Next step
Download NHANES and the public mortality file now to build your pipeline (e.g. GGIR for raw data). In parallel, check your university's All of Us DURA status and send a Whitehall II application. If you want a US hospital-outcome analysis, plan an NCHS Research Data Center proposal for the Medicare linkage. Register with UK Biobank so you're ready when it reopens.

Files are in `/private/tmp/e-FfWDhk/home/cwd/`:
- dataset-shortlist.html
- dataset-scout/shortlist.json

Sources: [UKB fees](https://www.ukbiobank.ac.uk/use-our-data/fees/), [UKB incident report](https://www.publictechnology.net/2026/07/13/health-and-social-care/uk-biobank-commissions-200k-security-review-after-major-data-incident/), [UKB reopening](https://cypro.co.uk/insights/cyber-bulletins/uk-biobank-breach-research-access-to-reopen/), [All of Us FAQ](https://researchallofus.org/frequently-asked-questions/), [All of Us Fitbit ownership paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13410188/), [Whitehall II policy](https://www.ucl.ac.uk/population-health-sciences/sites/population_health_sciences/files/w2_data_sharing_policy_v30_0.pdf), [CKB FAQ](https://www.ckbiobank.org/data-access/frequently-asked-questions), [MrOS NSRR](https://sleepdata.org/datasets/mros), [MrOS/SOF sleep profiles paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8996026/), [NSRR overview](https://academic.oup.com/jamia/article/25/10/1351/5026200).