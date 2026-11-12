The short version is that you can start on the PhysioNet/CinC 2019 Challenge data today, and the other useful datasets need one credentialing step. I'm answering from memory and didn't check live pages, so confirm current versions and processing times on each dataset's page.

## Download now, no application

**PhysioNet/Computing in Cardiology Challenge 2019, "Early Prediction of Sepsis from Clinical Data"**
- It has about 40k ICU patients from two hospital systems (training sets A and B), with hourly vitals, labs, and demographics.
- It includes a per-hour `SepsisLabel` derived from Sepsis-3 criteria. This is the only open dataset with a ready-made time-stamped onset label, so it's your week-one baseline.
- Two caveats:
  - The label is shifted about 6 hours before the Sepsis-3 onset time. That was a challenge design choice, so be careful comparing numbers with papers that don't use that shift.
  - It has only about 40 variables and no raw antibiotic or culture timestamps, so you can't re-derive onset with a different definition.
- Use the official utility score alongside AUROC and AUPRC, since prior work reports it.

The eICU demo (100 patients) is also open, but it's only useful for testing your pipeline.

## Needs credentialing (one application, several datasets)

PhysioNet credentialing is a one-time step. After it, each dataset only needs a data use agreement (DUA) signed on its page.

1. Create a PhysioNet account.
2. Complete the CITI "Data or Specimens Only Research" course, which takes a few hours.
3. Submit the credentialing form with a reference. Your supervisor is a natural choice, and they'll get an email to confirm.
4. Wait for approval. In my experience that's days to a couple of weeks, and your reference's response speed is the usual bottleneck. Start this today.
5. Sign the DUA for each dataset.

Datasets this unlocks:
- **MIMIC-IV** (single center, BIDMC) is the standard choice. The MIT-LCP `mimic-code` repo has a derived `sepsis3` table (suspected infection from antibiotics plus cultures, with SOFA ≥ 2), so you get Sepsis-3 onset times without writing the logic yourself.
- **MIMIC-III** is older. It's mostly useful for comparing against earlier papers.
- **eICU-CRD** is multi-center US (200+ hospitals), which is good for external validation. Its culture and antibiotic timing is much weaker, so Sepsis-3 onset derivation is noisier.
- **HiRID** (Bern) has high-resolution data at about 2-minute intervals. It has no official sepsis label, so you'd derive onset yourself.
- **SICdb** (Salzburg) is also on PhysioNet, I believe under the same credentialing. Check its page.

## Separate application

**AmsterdamUMCdb** is run by Amsterdam UMC. It involves a request form and a signed data sharing agreement with the institution, and it takes longer than PhysioNet. I'd treat it as a later-stage external validation set, not a week-one option.

## Tools that save time once you have access

- **ricu** (R package) harmonizes MIMIC, eICU, HiRID, and AmsterdamUMCdb into common concepts and includes a Sepsis-3 implementation.
- **YAIB** (Yet Another ICU Benchmark) has a sepsis prediction task across those datasets with preprocessing and baselines.

Both give you a consistent cohort and label definition across datasets, which matters because onset definitions differ between papers.

## Suggested plan for the week

1. **Today:** Download the Challenge data and start CITI and credentialing.
2. **Days 1–3:** Build the baseline on the Challenge data, for example gradient-boosted trees on lagged and windowed features, then a sequence model.
3. **When approved:** Sign the MIMIC-IV DUA, derive Sepsis-3 onset with `mimic-code`, and rerun your pipeline. Use eICU later for external validation.

## One compliance note

PhysioNet's DUAs generally prohibit sending the data to third-party services, including hosted LLM APIs, unless the service is covered by an approved arrangement. Check this before using any AI assistant on credentialed data, including me.