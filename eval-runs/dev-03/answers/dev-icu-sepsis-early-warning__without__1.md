I'm working from memory and haven't checked current access pages, so confirm the details below before you plan around them.

## Download today, no application

**PhysioNet/Computing in Cardiology Challenge 2019 (Early Prediction of Sepsis)** is open access.
- It has about 40k ICU patients with hourly vitals and labs from two hospital systems (training sets A and B). Each hour carries a `SepsisLabel` derived from Sepsis-3 criteria.
- It comes with the official utility-score evaluator, which rewards early but not too-early predictions, so you get a standard metric and published baselines to compare against.
- Caveats: the label is a challenge-specific implementation, not a clinician-adjudicated one. The variable set is limited, and the third hospital system's test set was never released.
- This is your best fit for a baseline within a week.

## Credentialed access (PhysioNet)

All of these use one PhysioNet credentialing process, so you apply once.

- **What you do:** create an account and complete the CITI "Data or Specimens Only Research" course. Then submit the application with your institutional details and a reference (your supervisor), and sign the data use agreement for each dataset.
- **How long it takes:** often a few days to a couple of weeks, depending on reviewer load. Start now, because it may not land inside your one-week window.
- **Datasets this unlocks:**
  - **MIMIC-IV** (Beth Israel Deaconess, single center): the standard choice. It has no onset column, but the MIMIC-Code repository has a `sepsis3` derived concept (suspected infection from antibiotics plus cultures, combined with SOFA ≥ 2), which gives you onset times.
  - **eICU-CRD** (multicenter US): the same credentials work. You derive Sepsis-3 labels yourself, and it's good for external validation.
  - **HiRID** (Bern, high-resolution): a credentialed PhysioNet dataset. Its sampling is dense, and you also build the labels yourself.
  - **SICdb** (Salzburg): also credentialed on PhysioNet, as far as I recall. Check its page, as it's newer.

## Separate application

- **AmsterdamUMCdb** (Amsterdam UMC) goes through the Amsterdam Data Science / UMC access process. This is typically a data access agreement with institutional sign-off and takes longer, so treat it as a later-stage external validation set, not a week-one option.

## Shortcut for labels

**YAIB (Yet Another ICU Benchmark)** includes harmonized pipelines for MIMIC, eICU, HiRID and AmsterdamUMCdb, with a sepsis prediction task and Sepsis-3-style labels. It still needs the underlying credentialed data, but it saves you from writing the onset-derivation and preprocessing code yourself.

## Suggested plan for the week

1. **Today:** start the CITI course and the PhysioNet application, and download the Challenge 2019 data.
2. **This week:** build your baseline (for example gradient-boosted trees on hourly windows with forward-filled features) on Challenge 2019 and score it with the utility metric.
3. **When credentialing clears:** move to MIMIC-IV with the `sepsis3` concept and validate on eICU.

Sepsis-3 onset definitions vary between implementations, such as the suspected-infection time window and the baseline SOFA assumption. Whichever you use, document your choices, because reviewers will ask.