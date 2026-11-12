## Short answer
Start on the **PhysioNet/CinC 2019 Challenge data** today, and file your **PhysioNet credentialing** application at the same time. That one application unlocks MIMIC-IV, eICU, HiRID and SICdb. This is from memory, so check current version numbers and processing times on the PhysioNet pages.

## Download now, no application
**PhysioNet/CinC Challenge 2019** ("Early Prediction of Sepsis from Clinical Data")
- It has about 40k ICU stays from two US hospital systems, with hourly vitals and labs (about 40 variables).
- It ships with a time-stamped `SepsisLabel` derived from Sepsis-3, so you don't have to build the label yourself.
- It's open access. It also comes with a baseline, a published utility metric and a large set of public entries to compare against.
- Caveats:
  - The label is shifted about 6 hours before the derived onset.
  - The variable set is fixed.
  - The data is a few years old.
  - A third hospital system's test set was never released.
- It's a good fit for a week-one baseline. It's too thin for a full thesis.

## Needs PhysioNet credentialing (one application, several datasets)
| Dataset | Notes for onset labels |
|---|---|
| **MIMIC-IV** (Boston, single center) | This is the main one. The `mimic-code` repo has a `sepsis3` derived concept, with suspected infection from antibiotic and culture timing plus SOFA. |
| **eICU-CRD** (US, multicenter, about 200 hospitals) | You derive onset yourself. Antibiotic and culture timing is patchier, so the labels are noisier. It's valuable for external validation. |
| **HiRID** (Bern, high-resolution) | You derive onset yourself. The Moor et al. sepsis work on HiRID and MIMIC has public label code you can reuse. |
| **SICdb** (Salzburg) | It's newer and has less published sepsis tooling. You'd derive onset yourself. |

**What the application involves:**
1. Create a PhysioNet account with your institutional email.
2. Complete the CITI "Data or Specimens Only Research" course. It takes a few hours, and you upload the completion report.
3. Fill in the credentialing form. As a student you'll need to name a reference, which is usually your supervisor, who gets an email to confirm.
4. Once you're approved, sign the data use agreement for each dataset. This is quick.

Approval often takes a few days but can stretch to a couple of weeks, so file it today.

## Needs a separate, heavier application
**AmsterdamUMCdb** (Netherlands) is granted by the Amsterdam UMC data team and ESICM. It requires a data use agreement and a project description, and it usually takes weeks. It's good for later external validation, but not for your one-week deadline.

## Practical suggestions
- **Use YAIB (Yet Another ICU Benchmark).** It harmonizes MIMIC, eICU, HiRID and AmsterdamUMCdb and includes a sepsis prediction task. That saves a lot of preprocessing and makes cross-dataset comparison easier. Check what sepsis definition it uses before relying on it.
- **Prefer MIMIC-IV over MIMIC-III.** It's newer and larger, and the `mimic-code` tooling targets it.
- **Fix your label definition early.** Sepsis-3 onset labels differ in the infection-window and SOFA-change conventions. Pick one and document it so your results are comparable across datasets.
- **Watch the data use terms.** PhysioNet's credentialed-data agreement restricts sending the data to third-party services, which includes online LLM APIs. If you plan to use AI tools on the data, check their responsible-use policy first.

## Suggested plan for the week
1. **Day 0:** Register, start CITI, and have your supervisor ready for the reference email.
2. **Day 0–1:** Download CinC 2019 and train a gradient-boosted model on hourly features with the challenge utility metric.
3. **When approved:** Move to MIMIC-IV with `sepsis3` labels, then validate on eICU or HiRID.

I can sketch the CinC 2019 baseline pipeline or the MIMIC-IV onset query if you'd like.