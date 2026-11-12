## Start today (no application)

**PhysioNet/CinC Challenge 2019** is the one to build your week-one baseline on.
- It has about 40k ICU stays from two US hospital systems (training sets A and B). Both are open on PhysioNet with no credentialing.
- Data are hourly vitals, labs, and demographics, with an hourly `SepsisLabel` derived from Sepsis-3.
- Caveat: the label turns positive 6 hours *before* the derived onset time. This was designed for early-prediction scoring, so check that it matches what you mean by "onset."
- The challenge also has a utility-based scoring function you can reuse for evaluation.
- Its limits are a fixed feature set, no raw infection data (cultures and antibiotics), and no ability to re-derive the label differently.

**Demo subsets** (MIMIC-IV Demo and eICU Demo, about 100 patients each) are also open. They are useful for writing your pipeline while credentialing is pending, but they are too small to train on.

## Credentialed access (one PhysioNet application covers several datasets)

You need a PhysioNet account, a completed CITI "Data or Specimens Only Research" course, a signed data use agreement per dataset, and identity and reference details (a supervisor will be asked to vouch for you). Do this today. The CITI course takes a few hours, and approval has typically taken days to a couple of weeks.

| Dataset | Notes for sepsis onset |
|---|---|
| **MIMIC-IV** | The best primary dataset. It has antibiotics, microbiology, labs, and vitals, and `mimic-code` ships a derived Sepsis-3 table. |
| **eICU-CRD** | Multi-center, so it is good for external validation. Infection timing is weaker, and you would have to derive onset yourself. |
| **HiRID** | Bern ICU, high-resolution (about 2-minute) data. It is widely used for sepsis prediction, but onset labels come from published derivations rather than the release itself. |
| **SICdb** | Salzburg ICU. It is newer and less used, so check what its documentation supports for infection and SOFA components. |

## Separate application

**AmsterdamUMCdb** is not through PhysioNet. You apply through Amsterdam Medical Data Science, complete training, and sign a data access agreement, which has generally taken weeks. It is good for external validation, but don't plan your first week around it.

## Harmonization tools

Use these once you have the data.
- **ricu** (R) and **YAIB** (Yet Another ICU Benchmark) harmonize several of these datasets and include sepsis tasks. They save a lot of work and make cross-dataset comparison more defensible.
- **mimic-code** has Sepsis-3 SQL for MIMIC-IV.

## Suggested plan

1. **Today:** start the CITI course and the PhysioNet credentialing, and download Challenge 2019.
2. **This week:** build the baseline (for example gradient-boosted trees on hourly features with carried-forward values) on Challenge 2019, and develop the loaders on the demo sets.
3. **When approved:** move to MIMIC-IV with your own Sepsis-3 labeling, and validate on eICU and HiRID.

Onset definitions differ between datasets (the Challenge's, MIMIC-derived, and eICU-derived), so state which one you use. A model trained on one definition can look much worse or better on another for reasons unrelated to the model.

I'm working from memory here and haven't checked current turnaround times, versions, or access terms. Confirm those on the PhysioNet and Amsterdam pages before you tell your supervisor a date.