## What I assumed you need

- **R1 (must):** adult ICU time series of vitals and labs.
- **R2 (must):** a time-stamped sepsis onset label, or the data to derive Sepsis-3 onset yourself (SOFA change plus suspected infection).
- **R3 (must):** thousands of patients.
- **R4 (nice to have):** usable within about a week.

I assumed you'll work in Python and don't already hold PhysioNet credentials. If you already have credentials, the timelines below get much shorter.

## Shortlist

All six are hosted on PhysioNet, so one account and one training course cover most of the applications.

| # | Dataset | Access | Licence | Size | Fit | Checked |
|---|---|---|---|---|---|---|
| 1 | [PhysioNet/CinC Challenge 2019 (sepsis)](https://physionet.org/content/challenge-2019/1.0.0/) | **Open download, minutes** | CC-BY-4.0 | 40,336 subjects | Strong | today |
| 2 | [MIMIC-IV](https://physionet.org/content/mimiciv/) | Credentialed, ~1–3 weeks | PhysioNet Credentialed Health Data License | very large | Strong (onset must be derived) | today (size from memory) |
| 3 | [eICU-CRD](https://physionet.org/content/eicu-crd/2.0/) | Credentialed, same process as MIMIC-IV | PhysioNet Credentialed license | multicentre, large | Strong (onset must be derived) | today (size from memory) |
| 4 | [HiRID](https://physionet.org/content/hirid/1.1.1/) | Credentialed plus approval from the data authors | PhysioNet Contributor Review license | ~34k admissions | Strong (onset must be derived) | today |
| 5 | [SICdb](https://physionet.org/content/sicdb/1.0.8/) | Credentialed plus approval from the data authors | PhysioNet Contributor Review license | not confirmed | Partial | today |
| 6 | [NWICU](https://physionet.org/content/nwicu-northwestern-icu/0.1.0/) | Credentialed | PhysioNet Credentialed license | not checked | Partial (contents not checked) | today (access only) |

## Details

**1. Challenge 2019: start here.**
- The page says: "we define sepsis according to the Sepsis-3 guidelines, i.e., a two-point change in the patient's SOFA score and clinical suspicion of infection (as defined by the ordering of blood cultures or IV antibiotics)."
- It gives you hourly vitals and labs with a per-hour sepsis label, and its utility score rewards early predictions and penalizes late ones, so you can reproduce published baselines directly.
- The label is the organisers' approximation, so read their onset convention before you trust the lead times.
- The test set is hidden, so you split the training data yourself.
- It combines two hospital systems. The "adult only" detail is from memory.
- Many sepsis papers use it. One returned by the literature search is an [LSTM-GAT model on this dataset](https://doi.org/10.1136/bmjhci-2025-101762).

**2 and 3. MIMIC-IV and eICU-CRD.** These have no ready-made Sepsis-3 label. You derive onset from SOFA components plus antibiotic and culture times. That derivation is a project in itself, but it is what makes your labels defensible, and it lets you validate across the two datasets. The steps:
1. Create a PhysioNet account.
2. Take the CITI "Data or Specimens Only Research" course. PhysioNet's instructions say to upload the training report, not the certificate, and to affiliate with MIT to avoid fees.
3. Submit the credentialing application. The reviewers are PhysioNet staff, and I don't know their current turnaround (my "1–3 weeks" is from memory).
4. Sign the data use agreement on each project page. MIMIC-IV's page says: "Only credentialed users who sign the DUA can access the files."

Credentialing is done once and covers both datasets. eICU-CRD timestamps are minute offsets from unit admission.

**4 and 5. HiRID and SICdb.** You need credentialing first. After that you submit a request to the data authors with "a specific research question" and sign their agreement. HiRID has 2-minute resolution from a Swiss ICU. Both are good for external validation, but I wouldn't plan the first week around them.

**6. NWICU.** It's a newer US ICU database at version 0.1.0. I only confirmed its access tier. Check its contents before relying on it.

## Known, not confirmed

- **AmsterdamUMCdb.** I recall it as a Dutch ICU database that needs an application form and a signed agreement through Amsterdam UMC. The page I tried returned a 404, so I couldn't confirm that, or its current terms. Search for the current official page before you plan around it.
- **Sizes and the derivation code.** The MIMIC-IV and eICU sizes, and the community SOFA and Sepsis-3 derivation code for MIMIC, are from memory.

## Not recommended, and why

- **Synthetic sepsis datasets** (for example [this figshare record](https://doi.org/10.6084/m9.figshare.32931644)). They contain no real patients, so they're no use for a research baseline.
- **Datasets that only hold mortality or discharge codes.** These came up in the registry noise. They fail R2.

## What I could not find

- The Zenodo and DataCite searches partly failed, so small institutional sepsis datasets may be missing.
- I didn't pull per-dataset usage papers beyond the one literature search.

## Next step

1. **Today:** download Challenge 2019 and build the baseline. This meets the one-week deadline on its own.
2. **Today:** start the PhysioNet account and the CITI course, since credentialing is the long pole.
3. **After approval:** apply for HiRID and SICdb, and derive Sepsis-3 labels on MIMIC-IV and eICU for external validation.

Checked 2026-11-12. Access rules and licences change, so check the pages again before you submit anything.

Interactive page: `/private/tmp/e-fyCGNy/home/cwd/dataset-shortlist.html`