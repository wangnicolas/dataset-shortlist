Start with the PhysioNet/CinC Challenge 2019 data on day one. Apply for MIMIC-IV and eICU in parallel, because both need credentialing. This is from memory and I haven't checked the current pages, so confirm turnaround times and versions on each site.

## Download now (no application)

**PhysioNet/CinC Challenge 2019, "Early Prediction of Sepsis from Clinical Data"**
- It has about 40k ICU stays from two hospital systems (training sets A and B), with hourly vitals and labs and 40 variables.
- It comes with a ready-made time-stamped `SepsisLabel`, derived using Sepsis-3 criteria. That makes it a first baseline you can run this week.
- The label is deliberately shifted: it turns positive 6 hours before the computed onset. Account for that when you compare against other datasets.
- The test set (set C) is hidden, so you'll cross-validate or split across A and B.
- It doesn't include antibiotic or culture timestamps, so you can't re-derive onset under a different definition.
- The eICU and MIMIC demo subsets are also open, but at about 100 patients they're only good for testing code.

## Credentialed (PhysioNet)

These all share one process:
1. Make a PhysioNet account.
2. Complete CITI "Data or Specimens Only Research" training and upload the certificate.
3. Submit a credentialing application, which needs a reference (your supervisor, usually).
4. After approval, sign a separate data use agreement for each dataset.

Credentialing review typically takes from several days to a couple of weeks. The CITI course takes a few hours. Start today, because this is the step most likely to eat your week.

| Dataset | Notes for sepsis onset |
|---|---|
| **MIMIC-IV** | The best second dataset. It has antibiotic, culture, and SOFA inputs, and the `mimic-code` repo has a `sepsis3` derived concept (suspected infection plus SOFA ≥ 2) that gives onset times. |
| **eICU-CRD** | Multicenter, about 200 US hospitals. Good for external validation, but derivation is messier because medication and culture timing are less clean. |
| **HiRID** | A high-resolution Swiss ICU dataset. You derive onset yourself. |
| **SICdb** | An Austrian ICU dataset. You derive onset yourself. |

If you'd rather not write the Sepsis-3 derivation yourself, look at the **YAIB (Yet Another ICU Benchmark)** codebase. It has a sepsis task with a harmonized pipeline across MIMIC, eICU, HiRID, and AmsterdamUMCdb, which saves a lot of time.

## Separate application

**AmsterdamUMCdb** is not on the PhysioNet credentialing path. It goes through Amsterdam Medical Data Science, with a data use agreement and institutional sign-off. Expect a few weeks. It's worth doing later as an external-validation set, not for the first week.

## Suggested plan

- **Today:** download Challenge 2019, and start the CITI training and PhysioNet credentialing.
- **Days 1–5:** build the baseline on Challenge 2019, for example gradient-boosted trees on hourly windowed features, evaluated with the Challenge utility score as well as AUROC.
- **Once approved:** add MIMIC-IV with the `sepsis3` concept, then eICU or HiRID for external validation.

PhysioNet's MIMIC and eICU terms restrict sending the data to external LLM APIs, so use opt-out or private deployments if you use AI tools on it. Check each dataset's current policy.

If you'd like, I can look up the current application pages and turnaround times, or sketch the MIMIC-IV onset derivation.