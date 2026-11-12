## What I assumed you need

- **R1 (must):** adult ICU patients with time series of routinely charted vitals and labs.
- **R2 (must):** a time-stamped sepsis onset label (Sepsis-3 or close), or the data to derive one: SOFA inputs plus evidence of suspected infection (cultures, antibiotics).
- **R3 (must):** something you can have within days for a first baseline.
- **R4 (nice to have):** thousands of stays, ideally more than one centre so you can validate externally.

## Shortlist

| # | Dataset | Access | Licence | Fit | Checked |
|---|---|---|---|---|---|
| 1 | PhysioNet/CinC Challenge 2019 | Open download, no account | CC BY 4.0 | Strong. Labels are ready-made. | today |
| 2 | MIMIC-IV (v3.1) | Credentialed, days to weeks | PhysioNet Credentialed DUA | Strong. You derive onset yourself. | today (access); size and tables from memory |
| 3 | eICU-CRD (v2.0) | Credentialed, same account as MIMIC | PhysioNet Credentialed DUA | Strong for validation. Onset must be derived. | today (access); contents from memory |
| 4 | HiRID (v1.1.1) | Credentialed plus data-owner approval, weeks | PhysioNet Contributor Review DUA | Strong. Onset must be derived. | today (access); contents from memory |
| 5 | SICdb (v1.0.8) | Credentialed plus contributor approval, weeks | PhysioNet Contributor Review DUA | Partial. Onset must be derived. | today (access); contents from memory |
| 6 | MIMIC-III (v1.4) | Credentialed, same as MIMIC-IV | PhysioNet Credentialed DUA | Partial. Superseded by MIMIC-IV. | today (access) |
| 7 | MIMIC-IV Demo | Open download | ODbL-1.0 | Weak. Only 100 patients. | today |

## Details

**Start today: Challenge 2019** ([page](https://physionet.org/content/challenge-2019/1.0.0/))
- It has 40,336 ICU stays from two hospital systems, in training sets A (20,336) and B (20,000).
- Each stay is a pipe-delimited file with one row per hour. There are 40 variables: 8 vitals, 26 labs and 6 demographic/administrative columns.
- `SepsisLabel` is Sepsis-3 (SOFA rise of at least 2 plus suspected infection). For septic patients it is 1 from t_sepsis − 6 h onward.
- The download is about 42 MB, so you can have a baseline running this afternoon.
- **Caveat:** the 6-hour shift is built into the label. You can't get the raw onset time back, and the data don't support other prediction horizons exactly. The challenge's hidden test hospital isn't released.
- It's the dataset most sepsis-prediction papers benchmark on, so your baseline will be comparable to published work.

**Credentialed datasets (MIMIC-IV, eICU, HiRID, SICdb, MIMIC-III)**
- **Account and credentialing.** All of these go through PhysioNet. You create an account, then apply for credentialing.
  - The CITI course "Data or Specimens Only Research" is required, and you upload the completion report, not the certificate.
  - The application asks about you and your research. The search results I got didn't say whether a reference is required, so check the application form.
- **Per-dataset agreement.** After credentialing you sign a data use agreement for each dataset. For HiRID and SICdb you also give a specific research question, and the data owners approve you separately.
- **Time.** I found no official processing time. A university guide says "several business days", with warnings of delays. Plan for 1–2 weeks and start the application today.
- **MIMIC-IV** ([page](https://physionet.org/content/mimiciv/))
  - There is no ready-made sepsis label. The standard route is to derive Sepsis-3 onset from SOFA and the antibiotic and culture timing. MIT-LCP's `mimic-code` repository has concept code for this, from memory and not checked today.
  - It's single-centre, from Beth Israel Deaconess.
- **eICU-CRD.** It's multi-centre, which makes it the natural external validation set. Culture and antibiotic data are thinner than in MIMIC, so a Sepsis-3 derivation is noisier.
- **HiRID** is high-resolution data from a Swiss ICU. The extra approval step makes it the slowest of the PhysioNet datasets.
- **SICdb** is from Salzburg and has a similar contributor-approval step.
- **MIMIC-III** is only worth it if you're reproducing an older paper.
- **Data use agreement.** The agreements restrict passing the data to third-party services, which can include online LLM tools. Read this before you paste any records into an AI service.

**Practice data: MIMIC-IV Demo** ([page](https://physionet.org/content/mimic-iv-demo/2.2/)). It has the same schema as MIMIC-IV with 100 patients. Use it this week to write and test your Sepsis-3 labelling code while credentialing is pending. It's too small for training.

## Known, not confirmed

**AmsterdamUMCdb** (Amsterdam UMC, Netherlands) is not registry-verified. The address I tried returned HTTP 404.
- A web search found the [GitHub repo](https://github.com/AmsterdamUMC/AmsterdamUMCdb) and the [Amsterdam Medical Data Science site](https://amsterdammedicaldatascience.nl/).
- Access is free but personal. You complete a training course such as CITI DSOR. You also submit an access request form and end user licence agreement, signed by you and an intensivist reference. After approval you get the data from DANS EASY or Google BigQuery.
- That process comes from search summaries and may have changed. Confirm it on the site.
- There is also a [Sepsis-3 implementation paper](https://gigabytejournal.com/articles/45) and a [PLOS ONE paper on Sepsis-3 epidemiology](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0304133) for this database. The paper is cited in the search results, but I haven't read it.

## Not recommended, and why

- **Hugging Face, Zenodo and figshare "sepsis" records.** These are mostly third-party copies of the 2019 Challenge, or small mortality and biomarker cohorts. Use the official PhysioNet source.
- **Transcriptomic sepsis cohorts** (for example SepsisTensor). They are omics data, not charted vitals and labs.

## What I could not find

- Apart from the 2019 Challenge and the MIMIC-IV demo, I found no open dataset that needs no application.
- I read no PhysioNet processing-time statistics, so "1–2 weeks" is my planning estimate.
- Sizes and table contents for the credentialed datasets are from memory.
- The literature search returned mostly reviews and conference abstracts. I haven't yet attached a specific baseline paper to each dataset, so find those yourself. The [2021 systematic review](https://doi.org/10.3389/fmed.2021.607952) is a place to start.

## Next step

1. **Today:** download the Challenge 2019 data and train your first baseline on it.
2. **Today:** start the CITI course and create your PhysioNet account.
3. **Today:** submit the credentialing application, and ask your supervisor early if you need a reference.
4. **This week:** prototype your Sepsis-3 labelling on the MIMIC-IV demo.
5. **Once approved:** request MIMIC-IV first, then eICU for external validation.
6. **If you want a European cohort:** request HiRID, SICdb or AmsterdamUMCdb in parallel, since those take longer.

All of this was checked on 2026-11-11 and 2026-11-12. Access rules and licences change, so recheck them before you rely on them. The interactive page is at `/private/tmp/e-06RH04/home/cwd/dataset-shortlist.html`.