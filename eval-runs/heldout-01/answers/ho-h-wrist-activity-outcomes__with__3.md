Several good wrist-worn datasets with linked outcomes exist. One of them (NHANES 2011–2014) you can start on today. I didn't build the interactive shortlist page. The verification step was partial, because the UK Biobank, China Kadoorie Biobank (CKB) and NSRR pages refused my automated fetch (403 or certificate errors). I used web-search summaries for those instead. All checks were done 2026-11-12.

## What I assumed you need
- **Must have:** a wrist-worn device, free-living wear of at least about 5–7 days, at least a few thousand adults, and linked outcomes (death, and ideally hospital or diagnosis records).
- **Access:** application-based is fine, you're at a US university, and I assumed no commercial use.
- **Not required:** a particular device brand. The comparability question is wrist versus hip or thigh, so I note which wrist and which device each study used.

## Shortlist

| # | Dataset | Wrist device | N (accelerometer) | Outcomes | Access | Checked |
|---|---|---|---|---|---|---|
| 1 | NHANES 2011–2014 | ActiGraph GT3X+, non-dominant wrist, up to 9 days | roughly 12,000 examined, fewer with valid wear | Mortality through the public-use linked files | Open download; restricted-use route via NCHS Research Data Center (RDC) | Today (search summaries of CDC pages) |
| 2 | UK Biobank | Axivity AX3, dominant wrist, 7 days, 100 Hz | about 103,700 | Hospital records, cancer and death registries | Application, fee, cloud platform; about 15 weeks | Today (search summaries) |
| 3 | Whitehall II | GENEActiv, non-dominant wrist, 9 days | 3,991 (ages 60–83) | Mortality via the UK Office for National Statistics register | Gated data-sharing request to UCL | Today (search summaries) |
| 4 | SOF and MrOS (via NSRR or the cohorts' own sites) | Wrist actigraphy, 1-minute epochs | MrOS about 2,800; SOF about 3,000 | Mortality; SOF also lists incident breast cancer and stroke | Controlled access request | Partly today |
| 5 | All of Us (Fitbit) | Consumer Fitbit, long-term | more than 59,000 | Linked electronic health records | Free; institution signs an agreement first | Today (search summaries) |
| 6 | China Kadoorie Biobank | Axivity AX3, 7 days | about 21,000–22,500 | Death and disease registries | Not confirmed as released yet | Today, status unclear |

## Details

**1. NHANES 2011–2014 (start here).**
- **Contents:**
  - The ActiGraph GT3X+ was worn on the [non-dominant wrist](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/) and recorded at 80 Hz. The CDC publishes minute-level files ([PAXMIN_G, 2011–12](https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/PAXMIN_G.htm), plus PAXMIN_H for 2013–14) and raw data. [Data-quality flags are here](https://wwwn.cdc.gov/nchs/nhanes/Pam/Default.aspx).
  - A [2024 paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11402588/) used 3,653 adults aged 50–80, with 416 deaths over about 24,000 person-years.
- **Outcome limits:** the [public linked mortality files](https://www.cdc.gov/nchs/data-linkage/mortality-public.htm) give vital status and follow-up time. For certain records, follow-up time and cause of death were replaced with synthetic values. Incident disease and hospital records are not in the public files.
- **Access:**
  1. Download the accelerometer files from the CDC.
  2. Download the mortality files from the CDC FTP site.
  3. Merge on the participant ID (SEQN).
  4. For real cause of death, apply to the NCHS RDC. The restricted and public mortality files can't be combined there.
- **Time:** minutes for the open route.
- **Sample size:** the wear-time and covariate criteria cut the sample hard. Expect a few thousand usable adults at most.

**2. UK Biobank.**
- **Contents:**
  - It's the largest wrist-accelerometer cohort. [About 103,700 participants](https://biobank.ndph.ox.ac.uk/showcase/ukb/docs/acc_plos_0169649.pdf) wore the AX3 for 7 days in 2013–15.
  - Hospital, cancer and death outcomes are, from memory, linked through national registries (the 2026 papers returned by the literature search used incident disease and dementia). I did not confirm the linkage details today.
  - Example uses: [sleep stages and incident disease](https://doi.org/10.1371/journal.pmed.1005213) and [circadian rhythms and dementia](https://doi.org/10.1186/s13195-026-02088-3).
- **Access:**
  1. Register (free); review is aimed within [10 working days](https://www.ukbiobank.ac.uk/use-our-data/fees/).
  2. Submit an application. UK Biobank is open to bona fide health researchers in the public interest.
  3. After approval you have 90 days to pay the fee and sign the material transfer agreement.
  4. Analyse on the UKB Research Analysis Platform. Access is cloud-only, and data can't be redistributed.
- **Time and cost:** about 15 weeks from submission to release on average. Tier 1 is £3,000 and Tier 3 is £9,000 per three years, excluding VAT; students may pay £500. Platform compute costs are extra, and each account starts with £40 of credit.
- **Caveat:** UK Biobank's own [access page](https://www.ukbiobank.ac.uk/enable-your-research/apply-for-access) refused my fetch. The fee and timing figures come from a search summary, so confirm them there.

**3. Whitehall II.**
- **Contents:** 3,991 civil servants aged 60–83 wore the GENEActiv for nine days in 2012–13. Deaths come from the ONS register ([paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11216065/)).
- **Access:** [gated MRC-style data sharing](https://www.ucl.ac.uk/psychiatry/research/mental-health-older-people/whitehall-ii/data-sharing). Send a proposal through the UCL portal. I didn't read the portal, so I don't know the timeline or whether a US institution needs a formal agreement.
- **Use:** the same [paper](https://www.nature.com/articles/s41598-025-30237-5) compares Whitehall II with UK Biobank, which is useful for replication.

**4. SOF and MrOS.**
- **Contents:** both cohorts have wrist actigraphy with mortality follow-up, per [this paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13698916) (MrOS n = 2,844; SOF n = 2,967). Participants are older adults only, and SOF is women only (MrOS is men only).
- **Access:** NSRR needs an account plus an approved request and a data use agreement for each dataset. The current [NSRR MrOS page](https://sleepdata.org/datasets/mros) reportedly lists no actigraphy, so the actigraphy may sit on MrOS Online and SOF Online instead. I couldn't open either page. Check which site holds the actigraphy before you plan around it.
- **Time:** weeks (my estimate, not confirmed).

**5. All of Us.**
- **Contents:**
  - Fitbit data from more than 59,000 participants are in the [Registered Tier](https://researchallofus.org/frequently-asked-questions/). Participants wear their own consumer devices, so wear length, device model and selection differ from a research accelerometer. They are not directly comparable with ActiGraph or Axivity output.
  - Outcomes come from linked electronic health records, not registries.
- **Access:**
  1. Your institution's signing official signs the Data Use and Registration Agreement.
  2. You register, verify your identity, and complete the Responsible Conduct of Research training and the code of conduct.
  3. Describe your project.
- **Cost and time:** the workbench is free ($300 starting credits). Time to access is days to weeks (my estimate).
- **Restriction:** participant-level data can't be linked to other sources without explicit permission from the program.

## Known, not confirmed
- **China Kadoorie Biobank:** 21,400–22,500 participants wore the Axivity AX3 on the wrist for 7 days ([paper](https://link.springer.com/article/10.1186/s12966-023-01537-8)). CKB said it would release the data through its access system after processing and a period of exclusive use by CKB researchers. I found no confirmation that it's released. [CKB's data access page](https://www.ckbiobank.org/data-access/data-2) refused my fetch. Ask CKB directly.
- **From memory, not checked today:** these may have wrist actigraphy with event follow-up, but I didn't verify them.
  - MESA Sleep Ancillary (about 2,000; Actiwatch Spectrum; on NSRR).
  - Rotterdam Study.
  - Rush Memory and Aging Project.
  - Some ARIC visits (I'm unsure whether ARIC used wrist or hip placement).
  - Women's Health Study (I believe it used hip placement).

## Not recommended
- **NHANES 2003–2006:** it has accelerometer data, but the device was worn on the hip. That conflicts with your comparability requirement.
- **Registry search hits** (HAR benchmarks, Parkinson's and sleep-lab sets, PhysioNet small datasets): they have no disease or death follow-up.
- **PhysioNet's [minute-level NHANES step-count set](https://physionet.org/content/minute-level-step-count-nhanes/1.0.2/):** it's a convenient derived copy. Use the CDC files as your primary source.

## What I could not find
- I couldn't confirm Whitehall II's timeline or US eligibility, UK Biobank's current fees from its own site, or NSRR's actigraphy holdings.
- I didn't search outside the US and UK systematically (for example Nordic or Japanese cohorts). The list may be incomplete.

## Next step
1. Start on NHANES 2011–2014 now to build your pipeline, since it needs no application.
2. Apply to UK Biobank in parallel for statistical power and hospital outcomes. Ask your institution's research office about the fee and agreement.
3. Request Whitehall II and the SOF/MrOS actigraphy for replication.
4. Check with your institutional review board early. These datasets are de-identified, but you should confirm the exemption.

I didn't write `dataset-shortlist.html`. Say so if you want it built.